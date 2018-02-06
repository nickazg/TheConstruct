from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class SmartTokenShareTest():

    def test_create(self):
        sts = SmartTokenShare()

        # Test vars
        test_project_id = 'project_id'

        test_symbol = 'symbol'
        test_decimals = 8
        test_owner = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
        test_total_supply = 10000000 * 100000000
        test_in_circulation = 100

        test_output =  b'\x01\x05\x01\x06symbol\x01\x01\x08\x01\x14#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9\x01\x07\x00\x80\xc6\xa4~\x8d\x03\x01\x01\x00'

        # Running create()
        sts.create(test_project_id, test_symbol, test_decimals, test_owner, test_total_supply)
        
        # Pull output from storage
        storage = StorageManager()
        output = storage.get_double('STS', test_project_id)

        # Check Test
        if output == test_output:
            print('test_create PASSED')
            return True
        
        print('test_create FAILED')
        return False