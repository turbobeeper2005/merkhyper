MERKLY_ABI = '''[
  {
    "type": "function",
    "name": "fee",
    "constant": true,
    "stateMutability": "view",
    "payable": false,
    "inputs": [],
    "outputs": [
      {
        "type": "uint256",
        "name": "fee"
      }
    ]
  },
  {
    "type": "function",
    "name": "mint",
    "constant": false,
    "stateMutability": "payable",
    "payable": true,
    "inputs": [
      {
        "type": "address",
        "name": "_to"
      },
      {
        "type": "uint256",
        "name": "amount"
      }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "name": "quoteBridge",
    "constant": true,
    "stateMutability": "view",
    "payable": false,
    "inputs": [
      {
        "type": "uint32",
        "name": "_destination"
      }
    ],
    "outputs": [
      {
        "type": "uint256",
        "name": "nativeFee"
      }
    ]
  },
  {
    "type": "function",
    "name": "bridgeHFT",
    "constant": false,
    "stateMutability": "payable",
    "payable": true,
    "inputs": [
      {
        "type": "uint32",
        "name": "_destination"
      },
      {
        "type": "uint256",
        "name": "_Id"
      }
    ],
    "outputs": [
      {
        "type": "bytes32",
        "name": "messageId"
      }
    ]
  }
]'''