import os
import sys
import django
import yt_dlp  # Replace pytube with yt-dlp

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from lectures.models import Course, Lecture
from django.core.exceptions import ObjectDoesNotExist

def get_video_info(url):
    """Helper to extract metadata using yt-dlp."""
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'No Title'), info.get('description', '')

def add_lectures_from_file():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webfrontend', 'frontend', 'public', 'anatomy.txt')

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    courses_data = content.strip().split('\n\n')

    for course_data in courses_data:
        lines = course_data.strip().split('\n')
        course_name = lines[0].strip()
        lecture_links = lines[1:]

        # Get or create the course
        course, _ = Course.objects.get_or_create(title__iexact=course_name, defaults={'title': course_name})
        print(f"Course: {course.title}")

        for link in lecture_links:
            link = link.strip()
            if not link:
                continue
            try:
                # Use yt-dlp instead of pytube to avoid 400 errors
                lecture_title, lecture_description = get_video_info(link)
                
                # Save to your Lecture model
                lecture, created = Lecture.objects.get_or_create(
                    course=course,
                    video_url=link,
                    defaults={
                        'title': lecture_title, 
                        'description': lecture_description,
                        'delivery_type': 'video' # Matches your model choices
                    }
                )
                if created:
                    print(f"  Added: {lecture_title}")
                else:
                    print(f"  Exists: {lecture_title}")
            except Exception as e:
                print(f"  Error processing {link}: {e}")

if __name__ == "__main__":
    add_lectures_from_file()