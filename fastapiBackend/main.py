"""
FastAPI + MongoDB (Beanie ODM) backend for SmartEdu

Includes:
- Full domain models:
  users: Institution, ClassGroup, User
  lectures: Course, Lecture, Quiz, Question, Option, etc.
  marketplace: ProductCategory, Product, Redemption, PointTransaction
- JWT authentication:
  POST /auth/register/
  POST /auth/login/
  POST /auth/refresh/
  GET  /auth/me/

Run:
    uvicorn app:app --reload
"""

from datetime import datetime, date, timedelta
from typing import Optional, List

from beanie import Document, Link, init_beanie
from bson import ObjectId
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, HttpUrl, Field


# -------------------------------------------------
# DB CONFIG
# -------------------------------------------------

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "smartedu_db"

# JWT CONFIG
SECRET_KEY = "change-this-secret-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=True)


# -------------------------------------------------
# USERS DOMAIN
# -------------------------------------------------

class Institution(Document):
    name: str
    code: str = Field(..., description="Short unique code used for joining, e.g. GRIET2025")
    address: Optional[str] = ""

    logo: Optional[str] = None          # store URL/path
    banner_image: Optional[str] = None  # store URL/path
    website: Optional[HttpUrl] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

    institution_type: Optional[str] = Field(
        default=None,
        description="school | college | university | training",
    )

    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "institutions"


class ClassGroup(Document):
    institution: Link[Institution]
    name: str
    grade: Optional[str] = ""

    section: Optional[str] = None
    academic_year: Optional[str] = None
    room_number: Optional[str] = None
    avatar_theme: Optional[str] = None
    class_teacher_name: Optional[str] = None
    description: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "class_groups"


class UserRole:
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Document):
    """
    User with password hash for auth + profile fields.
    """
    username: str
    email: Optional[EmailStr] = None

    role: str = Field(default=UserRole.STUDENT)
    institution: Optional[Link[Institution]] = None
    class_group: Optional[Link[ClassGroup]] = None

    wallet_address: Optional[str] = Field(
        default=None,
        description="Blockchain wallet address (0x...)",
    )

    # Profile fields
    mobile_number: Optional[str] = None
    profile_image: Optional[str] = None  # store URL/path
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None

    # Auth
    hashed_password: str
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"


# -------------------------------------------------
# LECTURES DOMAIN
# -------------------------------------------------

class Course(Document):
    title: str
    description: Optional[str] = ""

    teacher: Optional[Link[User]] = None

    institution: Optional[Link[Institution]] = None
    class_group: Optional[Link[ClassGroup]] = None

    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "courses"


class LectureVisibility:
    PUBLIC = "public"
    INSTITUTION = "institution"
    CLASS = "class"


class DeliveryType:
    VIDEO = "video"
    VR = "vr"
    AR = "ar"
    HYBRID = "hybrid"


class Lecture(Document):
    course: Link[Course]

    title: str
    description: Optional[str] = ""

    teacher: Optional[Link[User]] = None

    visibility: str = Field(default=LectureVisibility.PUBLIC)
    institution: Optional[Link[Institution]] = None
    class_group: Optional[Link[ClassGroup]] = None

    delivery_type: str = Field(default=DeliveryType.VIDEO)

    video_url: Optional[HttpUrl] = None
    resource_link: Optional[HttpUrl] = None

    vr_scene_id: Optional[str] = None
    ar_experience_id: Optional[str] = None

    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None

    is_live: bool = False
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "lectures"


class Quiz(Document):
    lecture: Link[Lecture]
    title: str
    description: Optional[str] = ""

    time_limit_seconds: Optional[int] = None
    is_active: bool = True
    shuffle_questions: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "quizzes"


class QuestionType:
    MCQ_SINGLE = "mcq_single"
    MCQ_MULTIPLE = "mcq_multiple"
    TRUE_FALSE = "true_false"
    SHORT_TEXT = "short_text"


class Question(Document):
    quiz: Link[Quiz]
    text: str
    question_type: str = Field(default=QuestionType.MCQ_SINGLE)
    marks: float = 1.0
    order: int = 0

    class Settings:
        name = "questions"


class Option(Document):
    question: Link[Question]
    text: str
    is_correct: bool = False

    class Settings:
        name = "options"


class QuizSubmission(Document):
    quiz: Link[Quiz]
    student: Link[User]

    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    score: float = 0.0
    max_score: float = 0.0

    points_awarded: int = 0
    points_tx_hash: Optional[str] = None

    class Settings:
        name = "quiz_submissions"


class SubmissionAnswer(Document):
    submission: Link[QuizSubmission]
    question: Link[Question]

    selected_option_ids: List[ObjectId] = Field(
        default_factory=list,
        description="List of Option IDs selected (for MCQ).",
    )

    text_answer: Optional[str] = ""

    is_correct: bool = False
    marks_obtained: float = 0.0

    class Settings:
        name = "submission_answers"


class LectureAttendance(Document):
    lecture: Link[Lecture]
    student: Link[User]

    joined_at: datetime = Field(default_factory=datetime.utcnow)
    left_at: Optional[datetime] = None

    total_duration_seconds: int = 0

    points_awarded: int = 0
    points_tx_hash: Optional[str] = None

    class Settings:
        name = "lecture_attendance"


class ResourceType:
    NOTE = "note"
    PDF = "pdf"
    EBOOK = "ebook"
    SLIDES = "slides"
    ASSIGNMENT = "assignment"
    LINK = "link"
    OTHER = "other"


class LearningResource(Document):
    course: Optional[Link[Course]] = None
    lecture: Optional[Link[Lecture]] = None

    title: str
    description: Optional[str] = ""

    resource_type: str = Field(default=ResourceType.PDF)

    file_path: Optional[str] = Field(
        default=None,
        description="Path/URL to uploaded file (PDF, notes, etc.)",
    )
    external_url: Optional[HttpUrl] = None

    is_public: bool = True
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "learning_resources"


# -------------------------------------------------
# MARKETPLACE DOMAIN
# -------------------------------------------------

class ProductCategory(Document):
    name: str
    slug: str
    description: Optional[str] = ""
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "product_categories"


class ProductType:
    EBOOK = "ebook"
    PDF = "pdf"
    COURSE = "course"
    MOCK_TEST = "mock_test"
    VOUCHER = "voucher"
    PHYSICAL = "physical"
    OTHER = "other"


class Product(Document):
    category: Optional[Link[ProductCategory]] = None

    name: str
    description: Optional[str] = ""

    product_type: str = Field(default=ProductType.EBOOK)

    points_price: int = Field(..., ge=0)
    stock: Optional[int] = Field(
        default=None,
        description="None = unlimited (digital)",
    )

    is_digital: bool = True

    digital_file_path: Optional[str] = None
    external_url: Optional[HttpUrl] = None

    thumbnail: Optional[str] = None

    metadata: Optional[dict] = None

    is_active: bool = True
    featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "products"

    @property
    def is_unlimited(self) -> bool:
        return self.stock is None


class RedemptionStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Redemption(Document):
    user: Link[User]
    product: Link[Product]

    quantity: int = 1
    points_spent: int

    status: str = Field(default=RedemptionStatus.PENDING)
    tx_hash: Optional[str] = None

    delivery_email: Optional[EmailStr] = None
    delivery_notes: Optional[str] = None

    shipping_address: Optional[str] = None
    contact_phone: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "redemptions"


class TxType:
    EARN = "earn"
    SPEND = "spend"
    ADJUST = "adjust"


class TxSource:
    QUIZ = "quiz"
    ATTENDANCE = "attendance"
    REDEMPTION = "redemption"
    MANUAL = "manual"
    OTHER = "other"


class PointTransaction(Document):
    user: Link[User]

    tx_type: str  # "earn" | "spend" | "adjust"
    source: str = Field(default=TxSource.OTHER)

    amount: int = Field(..., ge=0)
    description: Optional[str] = None

    on_chain_tx_hash: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "point_transactions"


# -------------------------------------------------
# AUTH HELPERS
# -------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_from_token(token: str, expected_type: str) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        if token_type != expected_type:
            raise credentials_exc
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = await User.get(user_id)
    if user is None or not user.is_active:
        raise credentials_exc
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    token = credentials.credentials
    return await get_user_from_token(token, expected_type="access")


# -------------------------------------------------
# Pydantic Schemas for Auth & Simple CRUD
# -------------------------------------------------

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    role: Optional[str] = UserRole.STUDENT


class UserOut(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    role: str
    wallet_address: Optional[str] = None

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenPair(BaseModel):
    access: str
    refresh: str


class TokenRefreshRequest(BaseModel):
    refresh: str


class InstitutionCreate(BaseModel):
    name: str
    code: str
    address: Optional[str] = None


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    teacher_id: Optional[str] = None


# -------------------------------------------------
# FASTAPI APP + INIT
# -------------------------------------------------

app = FastAPI(title="SmartEdu FastAPI + MongoDB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    await init_beanie(
        database=db,
        document_models=[
            Institution,
            ClassGroup,
            User,
            Course,
            Lecture,
            Quiz,
            Question,
            Option,
            QuizSubmission,
            SubmissionAnswer,
            LectureAttendance,
            LearningResource,
            ProductCategory,
            Product,
            Redemption,
            PointTransaction,
        ],
    )


# -------------------------------------------------
# AUTH ENDPOINTS  (Django SimpleJWT-compatible shapes)
# -------------------------------------------------

@app.post("/auth/register/", response_model=UserOut, status_code=201)
async def register_user(data: UserCreate):
    existing = await User.find_one(User.username == data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=data.username,
        email=data.email,
        role=data.role or UserRole.STUDENT,
        hashed_password=hash_password(data.password),
    )
    await user.insert()

    return UserOut(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role,
        wallet_address=user.wallet_address,
    )


@app.post("/auth/login/", response_model=TokenPair)
async def login_user(payload: LoginRequest):
    user = await User.find_one(User.username == payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    claims = {"sub": str(user.id), "username": user.username}
    access = create_access_token(claims)
    refresh = create_refresh_token(claims)
    return TokenPair(access=access, refresh=refresh)


@app.post("/auth/refresh/", response_model=dict)
async def refresh_access_token(data: TokenRefreshRequest):
    user = await get_user_from_token(data.refresh, expected_type="refresh")
    claims = {"sub": str(user.id), "username": user.username}
    access = create_access_token(claims)
    return {"access": access}


@app.get("/auth/me/", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        wallet_address=current_user.wallet_address,
    )


# -------------------------------------------------
# SIMPLE SAMPLE DOMAIN ENDPOINTS
# (you can attach auth requirements later as you wish)
# -------------------------------------------------

@app.post("/institutions", response_model=Institution)
async def create_institution(data: InstitutionCreate):
    existing = await Institution.find_one(Institution.code == data.code)
    if existing:
        raise HTTPException(status_code=400, detail="Institution code already exists")

    inst = Institution(
        name=data.name,
        code=data.code,
        address=data.address or "",
    )
    await inst.insert()
    return inst


@app.get("/institutions", response_model=List[Institution])
async def list_institutions():
    return await Institution.find_all().to_list()


@app.post("/courses", response_model=Course)
async def create_course(data: CourseCreate, current_user: User = Depends(get_current_user)):
    teacher = None
    if data.teacher_id:
        teacher = await User.get(data.teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
    else:
        # default to current user if they are teacher
        teacher = current_user

    course = Course(
        title=data.title,
        description=data.description or "",
        teacher=teacher,
    )
    await course.insert()
    return course


@app.get("/courses", response_model=List[Course])
async def list_courses():
    return await Course.find_all().to_list()
