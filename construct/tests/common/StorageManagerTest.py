from construct.common.StorageManager import StorageManager
from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete

class StorageManagerTest():
    
    def test_get(self): 
        storage = StorageManager()
        test_key = "test_key"
        test_value = "test_value"   

        Put(storage.ctx, test_key, test_value)
        
        # Test Get
        storage_get = storage.get(test_key)
        
        if storage_get == test_value:
            print('test_get PASSED')
            return True
        
        print('test_get FAILED')
        return False

    def test_put(self):
        storage = StorageManager()
        test_key = "test_key"
        test_value = "test_value"  

        # Test Put
        storage.put(test_key, test_value)

        storage_put = Get(storage.ctx, test_key)

        if storage_put == test_value:
            print('test_put PASSED')
            return True
        
        print('test_put FAILED')
        return False

    def test_delete(self):
        storage = StorageManager()
        test_key = "test_key"
        test_value = "test_value"  

        storage.put(test_key, test_value)
        
        # Test Delete 
        storage.delete(test_key)

        storage_delete = storage.get(test_key)        

        if storage_delete == "":
            print('test_delete PASSED')
            return True
        
        print('test_delete FAILED')
        return False

    def test_serialize_array(self):
        storage = StorageManager()
        test_array = ['test1','test2','test3']
        test_serialize_array = b'\x01\x03\x01\x05test1\x01\x05test2\x01\x05test3'

        # Testing serialize_array
        serialize_array = storage.serialize_array(test_array)

        if serialize_array == test_serialize_array:
            print('test_serialize_array PASSED')
            return True
        
        print('test_serialize_array FAILED')
        return False

    def test_deserialize_array(self):
        storage = StorageManager()
        test_array = ['test1','test2','test3']
        test_serialize_array = b'\x01\x03\x01\x05test1\x01\x05test2\x01\x05test3'

        # Testing deserialize_bytearray
        deserialized_array = storage.deserialize_bytearray(test_serialize_array)
        
        length = len(deserialized_array)

        # Comparing two lists errors: "Not Supported b'\x9c' NUMEQUAL"
        if length == 3:
            test1 = deserialized_array[0]
            test2 = deserialized_array[1]
            test3 = deserialized_array[2]

            if test1 == 'test1' and test2 == 'test2' and test3 == 'test3':
                    
                print('test_deserialize_array PASSED')
                return True
        
        print('test_deserialize_array FAILED')
        return False

