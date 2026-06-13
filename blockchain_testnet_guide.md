# SmartEdu: Testnet Blockchain Deployment Guide

This guide provides step-by-step instructions for deploying your SmartEdu smart contracts (`EduToken` and `Marketplace`) to a public EVM testnet (such as Sepolia or Edu Chain Testnet) and connecting your FastAPI backend to it.

---

## 1. Setup Deployer Wallet

You need an EVM-compatible wallet (like MetaMask) to act as the contract deployer and administrator.

1. **Get a Private Key**:
   - Create a new wallet in MetaMask (do not use your main personal account with real funds).
   - Export the private key of this account.
2. **Fund the Wallet (Get Faucet Tokens)**:
   - For **Sepolia**: Get free testnet ETH from a Sepolia faucet (e.g., [Google Cloud Sepolia Faucet](https://cloud.google.com/application-development/faucets/sepolia) or [Alchemy Sepolia Faucet](https://sepoliafaucet.com/)).
   - For **Edu Chain Testnet (Open Campus Codex)**: Get free testnet EDU tokens from the [Open Campus Faucet](https://drand.open-campus-codex.gelato.digital/faucet) or search for Open Campus Codex Discord faucet.

---

## 2. Hardhat Network Configuration

Your smart contracts are located in the `blockchain/student-reward-system` directory.

### Add Networks to `hardhat.config.ts`

Open `blockchain/student-reward-system/hardhat.config.ts`. The `sepolia` network is already defined. If you want to deploy to **Edu Chain Testnet**, add the `educhain` network configuration inside the `networks` block:

```typescript
    educhain: {
      type: "http",
      chainType: "l1",
      url: "https://rpc.open-campus-codex.gelato.digital",
      accounts: [configVariable("DEPLOYER_PRIVATE_KEY")],
    },
```

---

## 3. Set Hardhat Config Variables

Hardhat 3 uses Configuration Variables to securely store keys instead of exposing them in plain text config files.

Open your terminal, navigate to the `blockchain/student-reward-system` folder, and run the following commands:

### For Sepolia Deployment:
```bash
npx hardhat vars set SEPOLIA_RPC_URL "<your-infura-or-alchemy-rpc-url>"
npx hardhat vars set SEPOLIA_PRIVATE_KEY "<your-deployer-private-key>"
```

### For Edu Chain Deployment (if configured as above):
```bash
npx hardhat vars set DEPLOYER_PRIVATE_KEY "<your-deployer-private-key>"
```

---

## 4. Compile and Deploy Smart Contracts

Run the following commands inside `blockchain/student-reward-system`:

1. **Compile the Contracts**:
   ```bash
   npx hardhat compile
   ```
   This will generate JSON ABIs under `artifacts/contracts/`.

2. **Deploy via Hardhat Ignition**:
   Deploy the `EduSystem.ts` module, which deploys `EduToken` first and then deploys `Marketplace` linked to it.

   * To deploy to **Sepolia**:
     ```bash
     npx hardhat ignition deploy ignition/modules/EduSystem.ts --network sepolia
     ```
   * To deploy to **Edu Chain Testnet**:
     ```bash
     npx hardhat ignition deploy ignition/modules/EduSystem.ts --network educhain
     ```

3. **Record Contract Addresses**:
   Upon successful deployment, Hardhat will print the addresses in the terminal:
   ```text
   Deployed Addresses:
   EduSystem#EduToken - 0x... (EduToken Address)
   EduSystem#Marketplace - 0x... (Marketplace Address)
   ```
   Save these two addresses.

---

## 5. Configure FastAPI Backend Environment Variables

To point your new FastAPI backend to the public testnet, you need to configure the `.env` file in `fastapiBackend/` (or `backend/.env` if you share configuration).

Create or update the `.env` file with the following variables:

```ini
# Blockchain Network URL (E.g. Infura Sepolia RPC or open-campus rpc)
RPC_URL="https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID" # or https://rpc.open-campus-codex.gelato.digital

# Smart Contract Addresses (Pasted from deploy step)
EDU_TOKEN_ADDRESS="0x_YOUR_DEPLOYED_EDU_TOKEN_ADDRESS"
MARKETPLACE_ADDRESS="0x_YOUR_DEPLOYED_MARKETPLACE_ADDRESS"

# Admin Account (The wallet that deployed the contracts and owns them)
ADMIN_PRIVATE_KEY="0x_YOUR_DEPLOYER_PRIVATE_KEY"

# MongoDB Database Configuration
MONGO_URI="mongodb://localhost:27017"
DB_NAME="smartedu_db"

# Gemini API Key for chatbot and quiz generation
GEMINI_API_KEY="AIzaSy..."
```

---

## 6. Run and Verify Your Setup Locally

1. **Start MongoDB**: Make sure MongoDB is running on your machine on port `27017`.
2. **Install FastAPI Dependencies**:
   Navigate to `fastapiBackend/` and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Uvicorn**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. **Launch the Frontend**:
   Navigate to `webfrontend/frontend/` and run:
   ```bash
   npm run dev
   ```
5. **Testing the User Flow**:
   - Register a student user.
   - Go to profile, configure wallet address and private key (use a MetaMask account funded with faucet tokens).
   - Attend quizzes to see tokens automatically minted to your wallet on the real testnet!
   - Shop in the marketplace and watch the transactions get processed in real-time.
