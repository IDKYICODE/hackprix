import os
import django
from web3 import Web3
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from utils.blockchain import award_edutokens, execute_marketplace_purchase, get_live_balance, w3, get_token_contract, MARKET_ADDR

def run_test():
    # Account #1 from Hardhat for testing
    raw_address = "0xbcd4042de499d14e55001ccbb24a551f3b954096"
    student_address = Web3.to_checksum_address(raw_address)
    student_pvt_key = "0xf214f2b2cd398c806f84e317254e0f0b801d0643303237d97a22a48e01628897"

    print(f"--- DEMO START: Student {student_address} ---")
    print(f"Student Balance: {get_live_balance(student_address)} EDU")
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