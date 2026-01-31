# users/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.blockchain import get_live_balance
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Institution
from .serializers import (
    InstitutionSerializer,
    UserProfileUpdateSerializer,
    UserSerializer,
    RegisterSerializer,
)


class InstitutionByCodeView(generics.RetrieveAPIView):
    """
    GET /api/institutions/<code>/
    Returns institution details by its unique code.
    """

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "code"




class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Registers user AND returns JWT tokens (auto-login).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 🔐 Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user, context={"request": request}).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class MeView(APIView):
    """
    GET /api/auth/me/
    Returns current logged-in user's details.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class UserWalletInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.wallet_address:
            return Response({"balance": 0, "address": None})
            
        balance = get_live_balance(user.wallet_address)
        return Response({
            "address": user.wallet_address,
            "balance": balance,
            "symbol": "EDU"
        })