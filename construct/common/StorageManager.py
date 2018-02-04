from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import concat, list, range, take, substr

class StorageManager():
    """
    Wrapper for the default storage api and adds convenient  functionality
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

    def serialize_array(self, items):
        # serialize the length of the list
        itemlength = self.serialize_var_length_item(items)
        print('$itemslength')
        print(itemlength)
        
        output = itemlength

        # now go through and append all your stuff
        for item in items:

            # get the variable length of the item
            # to be serialized
            itemlen = self.serialize_var_length_item(item)
            print('$itemlen')
            print(itemlen)

            # add that indicator
            output = concat(output, itemlen)

            # now add the item
            output = concat(output, item)

            print('$output')
            print(output)

        # return the stuff
        return output


    def serialize_var_length_item(self, item):
        # get the length of your stuff
        stuff_len = len(item)

        # now we need to know how many bytes the length of the array
        # will take to store

        # this is one byte
        if stuff_len <= 255:
            byte_len = b'\x01'
        # two byte
        elif stuff_len <= 65535:
            byte_len = b'\x02'
        # hopefully 4 byte
        else:
            byte_len = b'\x04'

        out = concat(byte_len, stuff_len)

        return out

    def deserialize_bytearray(self, data):
        # ok this is weird.  if you remove this print statement, it stops working :/
        print("deserializing data...")
        print(data)

        # get length of length
        collection_length_length = substr(data, 0, 1)

        # get length of collection
        collection_len = substr(data, 1, collection_length_length)

        # create a new collection
        new_collection = list(length=collection_len)

        # calculate offset
        offset = 1 + collection_length_length

        # trim the length data
        newdata = data[offset:]

        for i in range(0, collection_len):

            # get the data length length
            itemlen_len = substr(newdata, 0, 1)

            # get the length of the data
            item_len = substr(newdata, 1, itemlen_len)

            start = 1 + itemlen_len
            end = start + item_len

            # get the data
            item = substr(newdata, start, item_len)

            # store it in collection
            new_collection[i] = item

            # trim the data
            newdata = newdata[end:]

        return new_collection
