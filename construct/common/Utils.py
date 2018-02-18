from boa.code.builtins import concat, list, range, take, substr
from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader, GetBlock

from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments


def generate_uid(ref=''):
    height = GetHeight()

    # header = GetHeader(height)
    # header.Timestamp
    
    block = GetBlock(height)
    timestamp = block.Timestamp
    tx = block.Transactions[0]
    tx_hash = tx.Hash
    
    time_hash = concat(timestamp, tx_hash)

    return concat(time_hash, ref)

def claim():
    storage = StorageManager()
    attachments = get_asset_attachments()
    
    print('attachments.receiver_addr')
    print(attachments.receiver_addr)

    claim_amount = storage.get_double('CLAIM', attachments.receiver_addr)

    if claim_amount == attachments.gas_attached:
        return True
    
    return False

def claim_clean(addr):
    storage = StorageManager()
    attachments = get_asset_attachments()
    
    storage.put_double('CLAIM', attachments.sender_addr, 0)