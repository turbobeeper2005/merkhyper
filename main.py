from web3 import Web3
from abi import MERKLY_ABI
import time
import random
from constants import chain_info, contract_addr, bsc_gas

def get_base_gas():
    try:
        web3 = Web3(Web3.HTTPProvider(chain_info['ethereum']['rpc']))
        gas_price = web3.eth.gas_price
        gwei_gas_price = web3.from_wei(gas_price, 'gwei')
        return gwei_gas_price
    except Exception as error:
        return get_base_gas()

def wait_gas():
    while True:
        current_gas = get_base_gas()
        if current_gas > MAX_GWEI:
            print(f'current_gas : {current_gas} > {MAX_GWEI}')
            time.sleep(60)
        else:
            break


def mint_and_bridge(private_key: str, from_chain: str, to_chain: str):
    from_rpc = chain_info[from_chain]['rpc']
    to_id = chain_info[to_chain]['chain_id']

    web3 = Web3(Web3.HTTPProvider(from_rpc))
    pub_address = web3.eth.account.from_key(private_key).address
    print(pub_address)
    contract = web3.eth.contract(address=Web3.to_checksum_address(contract_addr[from_chain]), abi=MERKLY_ABI)
    fee = contract.functions.fee().call()
    amount_to_mint = random.randint(1, 5)
    try:
        wait_gas()
        transaction = contract.functions.mint(pub_address, amount_to_mint).build_transaction({
            'from': pub_address,
            'gas': 0,
            'gasPrice': 0,
            'value': fee * amount_to_mint,
            'nonce': web3.eth.get_transaction_count(pub_address),
        })

        transaction['gasPrice'] = bsc_gas if from_chain == 'bsc' else int(web3.eth.gas_price * random.uniform(1.01, 1.02))

        pluser = [1.05, 1.07]
        gasLimit = web3.eth.estimate_gas(transaction)
        transaction['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))

        signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        tx_hash = web3.to_hex(transaction_hash)
        print("Mint transaction hash:", tx_hash)

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        '''
        if from_chain == 'Polygon':
            mint_id_hex = receipt.logs[1].topics[3]
        elif len(receipt.logs) == 2:
            mint_id_hex = receipt.logs[1].topics[3]
        else:
            mint_id_hex = receipt.logs[0].topics[3]

        mint_id = int.from_bytes(mint_id_hex, byteorder='big')
        print("Mint ID:", mint_id)'''

        quote = contract.functions.quoteBridge(to_id).call()

        transaction = contract.functions.bridgeHFT(to_id, amount_to_mint * (10**18)).build_transaction({
            'from': pub_address,
            'gas': 0,
            'gasPrice': 0,
            'value': quote,
            'nonce': web3.eth.get_transaction_count(pub_address),
        })

        transaction['gasPrice'] = bsc_gas if from_chain == 'bsc' else int(web3.eth.gas_price * random.uniform(1.01, 1.02))

        pluser = [1.05, 1.07]
        gasLimit = web3.eth.estimate_gas(transaction)
        transaction['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))

        signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        tx_hash = web3.to_hex(transaction_hash)
        print("Bridge transaction hash:", tx_hash)

    except Exception as error:
        print(error)

if __name__ == '__main__':
    '''
    "optimism"
    "celo"
    "avalanche"
    "zkevm"
    "bsc"
    "moonbeam"
    "gnosis"
    "arbitrum"
    "polygon"
    "base"
    "scroll"
    "ethereum"
    '''
    MAX_GWEI = 50
    from_chain = ['base']
    to_chain = ['celo']
    with open('./wallets.txt', 'r') as file:
        wallets = [line.strip() for line in file]

    for wallet in wallets:
        DELAY = random.randint(10, 15)
        mint_and_bridge(wallet, random.choice(from_chain), random.choice(to_chain))
        print(f'Sleep for {DELAY} seconds')
        time.sleep(DELAY)
