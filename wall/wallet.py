'''Only one time initially to obtain wallet credentials'''
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/9219391e394640a4b989b88a733ebd53'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address: {address}\nYour key: {privateKey}")