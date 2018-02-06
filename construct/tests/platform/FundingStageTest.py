from construct.platform.FundingStage import FundingStage
from construct.common.StorageManager import StorageManager

class FundingStageTest():
    
    # Test Vars
    test_project_id = 'project_id'
    test_funding_stage_id = 'funding_stage_id'    
    test_sts_supply = 100
    test_start_block = 1000
    test_end_block = 2000
    test_tokens_per_gas = 10 * 1000000000

    test_fs_info = b'\x01\x04\x01\x01d\x01\x02\xe8\x03\x01\x02\xd0\x07\x01\x05\x00\xe4\x0bT\x02'
       

    def test_create(self):
        fs = FundingStage()
              
        # Running create()
        fs.create(self.test_project_id, self.test_funding_stage_id, self.test_sts_supply, self.test_start_block, self.test_end_block, self.test_tokens_per_gas)

        storage = StorageManager()
        fs_info = storage.get_double(self.test_project_id, self.test_funding_stage_id)

        # Check Test
        if fs_info == self.test_fs_info:
            print('test_create PASSED')
            return True
        
        print('test_create FAILED')
        return False

    def test_read_from_storage(self):
        fs = FundingStage()
               
        storage = StorageManager()
        storage.put_double(self.test_project_id, self.test_funding_stage_id, self.test_fs_info)

        # Running read_from_storage()
        fs_info = fs.read_from_storage(self.test_project_id, self.test_funding_stage_id)

        # Pulling variables from fs_info 
        sts_supply = fs.get_sts_supply(fs_info)
        start_block = fs.get_start_block(fs_info)
        end_block = fs.get_end_block(fs_info)
        tokens_per_gas = fs.get_tokens_per_gas(fs_info)

        # Check Test
        if sts_supply == self.test_sts_supply and start_block == self.test_start_block and end_block == self.test_end_block and tokens_per_gas == self.test_tokens_per_gas:
            print('test_read_from_storage PASSED')
            return True
        
        print('test_read_from_storage FAILED')
        return False
