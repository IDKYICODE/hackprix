import json
import os
from pathlib import Path
from web3 import Web3

# 1. Initialize Connection to Hardhat Node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 2. Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BLOCKCHAIN_DIR = BASE_DIR / 'blockchain' / 'student-reward-system'

# 3. Contract Addresses 
EDU_TOKEN_ADDR = Web3.to_checksum_address("0x5FbDB2315678afecb367f032d93F642f64180aa3")
MARKET_ADDR = Web3.to_checksum_address("0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")

# 4. Admin Credentials
ADMIN_PVT_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ADMIN_ADDR = w3.eth.account.from_key(ADMIN_PVT_KEY).address

# --- UTILS ---

def ensure_checksum(address):
    """Helper to convert any address to checksum format to prevent Web3 errors."""
    if not address:
        return None
    try:
        return Web3.to_checksum_address(address)
    except ValueError:
        return None

# --- CONTRACT LOADERS ---

def get_token_contract():
    abi_path = BLOCKCHAIN_DIR / 'artifacts' / 'contracts' / 'EduToken.sol' / 'EduToken.json'
    with open(abi_path) as f:
        abi = json.load(f)['abi']
    return w3.eth.contract(address=EDU_TOKEN_ADDR, abi=abi)

def get_market_contract():
    abi_path = BLOCKCHAIN_DIR / 'artifacts' / 'contracts' / 'Marketplace.sol' / 'Marketplace.json'
    with open(abi_path) as f:
        abi = json.load(f)['abi']
    return w3.eth.contract(address=MARKET_ADDR, abi=abi)

# --- CORE BLOCKCHAIN FUNCTIONS ---

def award_edutokens(student_wallet_address, amount):
    """
    Admin pays gas to award tokens to a student.
    """
    address = ensure_checksum(student_wallet_address)
    if not address:
        return None, "Invalid or missing student wallet address."

    contract = get_token_contract()
    try:
        tx = contract.functions.awardStudent(address, amount).build_transaction({
            'from': ADMIN_ADDR,
            'nonce': w3.eth.get_transaction_count(ADMIN_ADDR),
            'gas': 150000,
            'gasPrice': w3.eth.gas_price
        })
        signed_tx = w3.eth.account.sign_transaction(tx, ADMIN_PVT_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex(), None
    except Exception as e:
        return None, str(e)

def execute_marketplace_purchase(student_wallet_address, cost):
    """
    Admin processes the purchase. Tokens are pulled from student, Admin pays gas.
    """
    address = ensure_checksum(student_wallet_address)
    if not address:
        return None, "Invalid or missing student wallet address."

    market = get_market_contract()
    try:
        tx = market.functions.processPurchase(address, cost).build_transaction({
            'from': ADMIN_ADDR,
            'nonce': w3.eth.get_transaction_count(ADMIN_ADDR),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        signed_tx = w3.eth.account.sign_transaction(tx, ADMIN_PVT_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex(), None
    except Exception as e:
        return None, f"Blockchain execution failed: {str(e)}"

def get_live_balance(student_wallet_address):
    """
    Fetches the actual EDU balance from the blockchain.
    """
    address = ensure_checksum(student_wallet_address)
    if not address:
        return 0
        
    try:
        contract = get_token_contract()
        balance_wei = contract.functions.balanceOf(address).call()
        return balance_wei / 10**18 
    except Exception:
        return 0