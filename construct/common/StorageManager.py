from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.Neo.Runtime import Serialize, Deserialize
from boa.builtins import concat, list, range, take, substr, has_key, keys, values

"""
Wrapper for the default storage api and adds convenient  functionality
"""

CTX = GetContext()

def get(key):
    return Get(CTX, key)

def get_double(key_one, key_two):
    storage_key = concat(key_one, key_two)
    return get(storage_key)

def get_triple(key_one, key_two, key_three):
    storage_key_two = concat(key_one, key_two)
    storage_key_three = concat(storage_key_two, key_three)
    return get(storage_key_three)

def put(key, value):
    Put(CTX, key, value)

def put_double(key_one, key_two, value):
    storage_key = concat(key_one, key_two)
    return put(storage_key, value)

def put_triple(key_one, key_two, key_three, value):
    storage_key_two = concat(key_one, key_two)
    storage_key_three = concat(storage_key_two, key_three)
    return put(storage_key_three, value)

def delete(key):
    Delete(CTX, key)

def delete_double(key_one, key_two):
    storage_key = concat(key_one, key_two)
    return delete(storage_key)

def delete_triple(key_one, key_two, key_three):
    storage_key_two = concat(key_one, key_two)
    storage_key_three = concat(storage_key_two, key_three)
    return delete(storage_key_three)

def serialize(item):
    print('serialize')
    if item:
        item_keys = keys(item)
        item_values = values(item)

        num_items = len(item_values)

        output_array = list(length=num_items+1)
        # output_array[0] = item_keys

        print('asdasd')
        # for i in range(0, num_items):
        #     print(i)
            # output_array[i] = item_values[i]        

        return Serialize(output_array)

def deserialize(item):
    print('deserialize')
    if item:
        input_array = Deserialize(item)
        item_keys = input_array[0]

        num_keys = len(item_keys)

        output_dict = {}

        for i in range(0, num_keys):
            item_key = item_keys[i]
            item_value = input_array[i+1]
            
            output_dict[item_key] = item_value
        
        return output_dict

def serialize_array(item):
    if item:
        return Serialize(item)

def deserialize_array(item):
    if item:
        return Deserialize(item)

def array_concat(array1, array2):
    new_length = len(array1) + len(array2)
    new_array = list(length=new_length)
    for i in range(0, new_length):
        if i < len(array1):
            new_array[i] = array1[i]
        else:
            i_offset = i - len(array1)
            new_array[i] = array2[i_offset]
        
    return new_array

def attrs_set(attrs, key, value):
    if has_key(attrs, key):
        attrs[key] = value
        return True
    return False

def attrs_is_valid(attrs, attrs_keys):
    if not attrs:
        return False
    
    for key in attrs_keys:
        if not has_key(attrs, key):
            return False    
    return True
