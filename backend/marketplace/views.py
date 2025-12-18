from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from utils.blockchain import execute_marketplace_purchase, get_live_balance

class BuyItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        # In a real app, you'd get this from request.data
        item_id = request.data.get('item_id')
        item_cost = 100 # Fixed cost for demo
        
        if not user.wallet_address:
            return Response({"error": "No wallet linked"}, status=400)

        # 1. Check Blockchain balance before trying to buy
        current_balance = get_live_balance(user.wallet_address)
        if current_balance < item_cost:
            return Response({"error": "Insufficient EDU balance"}, status=400)

        # 2. Execute Admin-Mediated Purchase
        tx_hash, error = execute_marketplace_purchase(user.wallet_address, item_cost)

        if not error:
            # Here you would typically create a 'PurchaseHistory' record in Django
            return Response({
                "message": "Item purchased successfully!",
                "tx_hash": tx_hash
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Purchase failed: {error}"}, status=500)