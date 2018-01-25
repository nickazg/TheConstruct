from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import concat

class StorageManager():
    """
    Wrapper for the storage api and adds convenient functionality
    """
    ctx = GetContext()

    def get(self, key):
        return Get(self.ctx, key)
    
    def get_double(self, key_one, key_two):
        storage_key = concat(key_one, key_two)
        return self.get(storage_key)

    def get_triple(self, key_one, key_two, key_three):
        storage_key_two = concat(key_one, key_two)
        storage_key_three = concat(storage_key_two, key_three)
        return self.get(storage_key_three)

    def put(self, key, value):
        Put(self.ctx, key, value)
    
    def put_double(self, key_one, key_two, value):
        storage_key = concat(key_one, key_two)
        return self.put(storage_key, value)

    def put_triple(self, key_one, key_two, key_three, value):
        storage_key_two = concat(key_one, key_two)
        storage_key_three = concat(storage_key_two, key_three)
        return self.put(storage_key_three, value)

    def delete(self, key):
        Delete(self.ctx, key)

    def delete_double(self, key_one, key_two):
        storage_key = concat(key_one, key_two)
        return self.delete(storage_key)
    
    def delete_triple(self, key_one, key_two, key_three):
        storage_key_two = concat(key_one, key_two)
        storage_key_three = concat(storage_key_two, key_three)
        return self.delete(storage_key_three)
    
    # Serialization
    # https://github.com/CityOfZion/neo-boa/blob/master/boa/tests/src/SerializationTest.py
    # ability to combine multiple key-value stores into one object
    def flatten_storage(self):
        pass
    
    # Deserialization
    # ability to to expand flattened storage back into its respective key-value stores   
    def expand_storage(self):
        pass