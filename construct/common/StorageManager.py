from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import concat

class StorageManager():
    """
    Wrapper for the storage api
    """
    ctx = GetContext()

    def get(self, key):
        return Get(self.ctx, key)
    
    def get_type(self, key_type, key):
        storage_key = concat(key_type, key)
        return self.get(storage_key)

    def put(self, key, value):
        Put(self.ctx, key, value)
    
    def put_type(self, key_type, key, value):
        storage_key = concat(key_type, key)
        return self.put(storage_key, value)

    def delete(self, key):
        Delete(self.ctx, key)

    def delete_type(self, key_type, key):
        storage_key = concat(key_type, key)
        return self.delete(storage_key)