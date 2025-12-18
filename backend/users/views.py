# users/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.blockchain import get_live_balance

from .serializers import UserProfileUpdateSerializer, UserSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    """
    GET /api/auth/me/
    Returns current logged-in user's details.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
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