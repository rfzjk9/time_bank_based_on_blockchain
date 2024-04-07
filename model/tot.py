from web3 import Web3
import json

admin_address = "0x1862EB3030659e2c3c029197835c3d8710b4D10a"
contract_address = "0xca7aC98C551b6B9c4395E54fdAE58EA24d172c60"
admin_key = "0xd9d4365e6115144d5ad50ad5af7eb348b991b2e2d9a857d2c0ff074b8b6d86f0"

# 读取abi
with open("./model/abi.json") as file:
    abi = json.load(file)["abi"]

# 连接测试链 Ganache
provider_url = "HTTP://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(provider_url))

# 配置合约地址
cont = w3.eth.contract(address = contract_address, abi=abi)


def np_transfer(_to_addr, _value):
    return private_transfer(admin_address, _to_addr, _value, admin_key)


def get_balance(_addr):
    try:
        _balance = cont.functions.balanceOf(_addr).call()
    except ValueError as e:
        print("Error:", e)
        return -1
    else:
        return _balance


def create_account():
    acct = w3.eth.account.create()
    return acct


def _get_raw_transaction(_from_addr, _to_addr, _value):
    nonce = w3.eth.get_transaction_count(_from_addr)
    txn = cont.functions.transfer(
        _to_addr,
        _value,
    ).build_transaction(
        {
            "from": _from_addr,
            "chainId": w3.eth.chain_id,
            "gas": 53000,
            "gasPrice": w3.to_wei("15", "gwei"),
            "nonce": nonce,
        }
    )
    return txn


def private_transfer(_from_addr, _to_addr, _value, _key):
    txn = _get_raw_transaction(_from_addr, _to_addr, _value)
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=_key)
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    except ValueError as e:
        print("Error:", e)
        return False
    else:
        return True


