import json
from pathlib import Path
from web3 import Web3
from django.conf import settings

# Connect to Hardhat Local Node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

def award_edutokens(student_wallet_address, amount):
    """
    Calls the awardStudent function on the local EduToken contract.
    """
    if not student_wallet_address:
        return None, "No wallet address provided"

    # 1. Contract Configuration
    # Use the address you got from the Hardhat Ignition deployment
    contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3" 
    
    # Path to your Hardhat ABI (adjust path if needed)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent # Goes up to /hackathon/
    
    abi_path = BASE_DIR / 'blockchain' / 'student-reward-system' / 'artifacts' / 'contracts' / 'EduToken.sol' / 'EduToken.json'
    with open(abi_path) as f:
        abi = json.load(f)['abi']

    contract = w3.eth.contract(address=contract_address, abi=abi)

    # 2. Admin Credentials (Account #0 from npx hardhat node)
    # REPLACE WITH THE ACTUAL PRIVATE KEY FROM YOUR TERMINAL
    admin_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    admin_address = w3.eth.account.from_key(admin_private_key).address

    try:
        # 3. Build & Sign Transaction
        nonce = w3.eth.get_transaction_count(admin_address)
        tx = contract.functions.awardStudent(student_wallet_address, amount).build_transaction({
            'from': admin_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, admin_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return tx_hash.hex(), None
    except Exception as e:
        return None, str(e)