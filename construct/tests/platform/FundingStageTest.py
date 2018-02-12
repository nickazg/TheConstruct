from construct.platform.FundingStage import FundingStage
from construct.platform.KYC import KYC
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments
from boa.code.builtins import list


class FundingStageTest():
    
    test_project_id = 'project_id'
    test_funding_stage_id = 'test_funding_stage_id'
    test_start_block = 1500
    test_end_block = 3000
    test_supply = 500
    test_tokens_per_gas = 10
    
    test_fs_info = b'\x01\x05\x01\x02\xdc\x05\x01\x02\xb8\x0b\x01\x02\xf4\x01\x01\x01\n\x01\x01\x00'
    test_add_amount = 150

    test_address1 = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
    test_address2 = b'j\x1agL0\xff\x926\x02\xde.a\x1fR\xe3FT\x0f\xba|'


    def test_create(self):
        fs = FundingStage()

        # Running start_new_crowdfund()
        fs.create(self.test_project_id, self.test_funding_stage_id, self.test_start_block, self.test_end_block, self.test_supply, self.test_tokens_per_gas)
        
        # Pull output from storage
        storage = StorageManager()
        output = storage.get_triple('FS', self.test_project_id, self.test_funding_stage_id)

        # Check Test
        if output == self.test_fs_info:
            print('test_create PASSED')
            return True
        
        print('test_create FAILED')
        return False

    def test_available_amount(self):
        fs = FundingStage()

        # Running crowdfund_available_amount()
        available = fs.available_amount(self.test_project_id, self.test_funding_stage_id)
        
        test_available = self.test_supply - 0

        # Check Test
        if available == test_available:
            print('test_available_amount PASSED')
            return True
        
        print('test_available_amount FAILED')
        return False

    def test_add_to_circulation(self):
        fs = FundingStage()

        # Setting default info
        storage = StorageManager()
        storage.put_triple('FS', self.test_project_id, self.test_funding_stage_id, self.test_fs_info)    


        # Running add_to_crowdfund_circulation()
        fs.add_to_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        fs.add_to_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        fs.add_to_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        
        in_circ = fs.get_circulation(self.test_project_id, self.test_funding_stage_id)

        test_in_circ = self.test_add_amount * 3

        # Check Test
        if in_circ == test_in_circ:
            print('test_add_to_circulation PASSED')
            return True
        
        print('test_add_to_circulation FAILED')
        return False

    def test_get_circulation(self):
        fs = FundingStage()

        # Setting default info
        storage = StorageManager()
        storage.put_triple('FS', self.test_project_id, self.test_funding_stage_id, self.test_fs_info)    

        fs.add_to_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        
        # Running get_crowdfund_circulation()
        in_circ = fs.get_circulation(self.test_project_id, self.test_funding_stage_id)

        # Check Test
        if in_circ == self.test_add_amount:
            print('test_get_circulation PASSED')
            return True
        
        print('test_get_circulation FAILED')
        return False 
    
    def test_calculate_can_exchange(self):
        fs = FundingStage()

        ## Testing Pass
        fs.create(self.test_project_id, self.test_funding_stage_id, 1, 99999, 1000, 100)
        passed = fs.calculate_can_exchange(self.test_project_id, self.test_funding_stage_id, 5)

        ## Testing Failures
        # supply of 2
        fs.create(self.test_project_id, 'fs_supply_test', 1, 99999, 2, 100)
        fs_supply_test = fs.calculate_can_exchange(self.test_project_id, 'fs_supply_test', 5)
        
        # start block of 9999999
        fs.create(self.test_project_id, 'start_block_test', 9999999, 99999, 1000, 100)
        start_block_test = fs.calculate_can_exchange(self.test_project_id, 'start_block_test', 5)

        # end block of 10
        fs.create(self.test_project_id, 'end_block_test', 1, 10, 1000, 100)
        end_block_test = fs.calculate_can_exchange(self.test_project_id, 'end_block_test', 5)

        # Check Test
        if passed:
            if not fs_supply_test and not start_block_test and not end_block_test:
                print('test_calculate_can_exchange PASSED')
                return True
        
        print('test_calculate_can_exchange FAILED')
        return False

    def test_can_exchange(self):
        fs = FundingStage()

        attachments = get_asset_attachments()

        # Registers KYC address
        storage = StorageManager()
        storage.put_triple(self.test_project_id, 'KYC_address', self.test_address2, True)

        fs.create(self.test_project_id, 'test_can_exchange', 1, 999999, 10000, 100)
        test_result = fs.can_exchange(self.test_project_id, 'test_can_exchange', attachments)

        # Check Test
        if test_result:
            print('test_can_exchange PASSED')
            return True
        
        print('test_can_exchange FAILED')
        return False

    def test_exchange(self):

        fs = FundingStage()
        attachments = get_asset_attachments()


        # Test vars
        tokens_per_gas = 100
        test_exchanged_sts = attachments.gas_attached * tokens_per_gas / 100000000


        # Sets balance to 0
        storage = StorageManager()
        storage.put_double(self.test_project_id, attachments.sender_addr, 0)

        # Registers KYC address
        storage.put_triple(self.test_project_id, 'KYC_address', self.test_address2, True)

        # Setting default info
        storage = StorageManager()
        storage.delete_triple('FS', self.test_project_id, self.test_funding_stage_id)

        # Creates new test fund
        fs.create(self.test_project_id, self.test_funding_stage_id, 1, 999999, 10000, tokens_per_gas)

        # Testing exchange method and checking stored balance
        fs.exchange(self.test_project_id, self.test_funding_stage_id)
        result1 = storage.get_double(self.test_project_id, attachments.sender_addr)

        # Testing exchange method and checking stored balance again (should double)
        fs.exchange(self.test_project_id, self.test_funding_stage_id)
        result2 = storage.get_double(self.test_project_id, attachments.sender_addr)
        
        # Check Test
        print('CHECK')
        print(result1)
        print(result2)
        print(test_exchanged_sts)
        
        if result1 == test_exchanged_sts and result2 == test_exchanged_sts * 2:
            print('test_exchange PASSED')
            return True
        
        print('test_exchange FAILED')
        return False