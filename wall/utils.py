from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/9219391e394640a4b989b88a733ebd53'))
    address = '0xe9a099F38E270d7f1d101b1cB24EcC57F465B6fc'
    privateKey = '0xb2bda96fda35ff35cad5ccd2389539d2572ca96d40af48e2c9da5742a32215fa'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice = gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value = value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId

def checkForWord(form, word):

    if form.is_valid():
        fields_to_check = ['title', 'description', 'content']
        for field in fields_to_check:

            if word in form.cleaned_data.get(field).lower().split():

                return True

        return False

    else:
        return True