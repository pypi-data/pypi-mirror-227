from web3 import Web3

# Connect to the Goerli testnet using Infura (replace YOUR_INFURA_PROJECT_ID)
w3 = Web3(Web3.HTTPProvider(
    'https://goerli.infura.io/v3/d33e360b492d47d5a817092a3798ce37'))

# Check if connected
if w3.is_connected():
    print("Connected to Ethereum!")
else:
    print("Not connected!")

# Contract ABI (from Remix or your deployment tool)
ABI = [
    {
        "inputs": [],
        "name": "get",
                "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "x",
                                "type": "uint256"
            }
        ],
        "name": "set",
        "outputs": [],
        "stateMutability": "nonpayable",
                "type": "function"
    }
]

# Contract address (from deployment on Goerli)
contract_address = '0xe4007dF4b0E06df5F9A5A5F1705715FCc3a7Ac86'

# Create contract object
contract = w3.eth.contract(address=contract_address, abi=ABI)

# Interact with the contract
# For instance, call the 'get' function
result = contract.functions.get().call()
print(f"Stored value: {result}")
