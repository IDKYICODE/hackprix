import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from utils.blockchain import award_edutokens, execute_marketplace_purchase, get_live_balance, w3, get_token_contract, MARKET_ADDR

def run_test():
    # Account #1 from Hardhat for testing
    student_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    student_pvt_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

    print(f"--- DEMO START: Student {student_address} ---")

    # 1. Earn points from Quiz
    print("\n[Admin] Awarding 200 EDU Tokens for passing Quiz...")
    award_edutokens(student_address, 200)
    print(f"Student Balance: {get_live_balance(student_address)} EDU")

    # 2. Student gives Marketplace permission to take points
    # (In React/Privy, this will be a 'Confirm' popup)
    print("\n[Student] Signing approval for Marketplace...")
    token = get_token_contract()
    tx_app = token.functions.approve(MARKET_ADDR, 100 * 10**18).build_transaction({
        'from': student_address,
        'nonce': w3.eth.get_transaction_count(student_address),
        'gas': 100000,
        'gasPrice': w3.eth.gas_price
    })
    signed_app = w3.eth.account.sign_transaction(tx_app, student_pvt_key)
    w3.eth.send_raw_transaction(signed_app.raw_transaction)
    print("✅ Marketplace Approved.")

    # 3. Buy an item
    print("\n[Admin] Sponsoring purchase of Item (Cost: 100 EDU)...")
    tx_buy, err = execute_marketplace_purchase(student_address, 100)
    
    if err:
        print(f"❌ Failed: {err}")
    else:
        print(f"✅ Purchase Success! TX: {tx_buy}")
        print(f"New Student Balance: {get_live_balance(student_address)} EDU")

if __name__ == "__main__":
    run_test()