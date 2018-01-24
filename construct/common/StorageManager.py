from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import concat

class StorageManager():
    """
    Wrapper for the storage api and adds convenient functionality
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

    # Serialization
    # https://github.com/CityOfZion/neo-boa/blob/master/boa/tests/src/SerializationTest.py
    # ability to combine multiple key-value stores into one object
    def flatten_storage(self):
        pass
    
    # Deserialization
    # ability to to expand flattened storage back into its respective key-value stores   
    def expand_storage(self):
        pass