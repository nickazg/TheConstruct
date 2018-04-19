from construct.common.StorageManager import serialize

def Main():

    test_dict = {}
    test_dict['var_int'] = 1
    test_dict['var_str'] = 'sdad'
    test_dict['var_list'] = [ 1, 'b', 'c']

    return serialize(test_dict)