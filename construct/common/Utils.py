from boa.code.builtins import concat, list, range, take, substr
from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader, GetBlock

class Utils():
    """
    utility class containing helper functions
    """
    @staticmethod
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

