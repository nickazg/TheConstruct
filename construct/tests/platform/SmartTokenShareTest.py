from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class SmartTokenShareTest():
    
    # Test Vars
    test_project_id = 'project_id'
    test_symbol = 'symbol'
    test_decimals = 8
    test_owner = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
    test_total_supply = 10000000 * 100000000
    # test_in_circulation = 0
    test_sts_info =  b'\x01\x05\x01\x06symbol\x01\x01\x08\x01\x14#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9\x01\x07\x00\x80\xc6\xa4~\x8d\x03\x01\x01\x00'
    
    test_funding_stage_id = 'test_funding_stage_id'
    test_start_block = 1500
    test_end_block = 3000
    test_supply = 500
    test_tokens_per_gas = 10
    # test_crowdfund_in_circulation = 0 
    test_crowdfund_info = b'\x01\x05\x01\x02\xdc\x05\x01\x02\xb8\x0b\x01\x02\xf4\x01\x01\x01\n\x01\x01\x00'
    test_add_amount = 150

    def test_create(self):
        sts = SmartTokenShare()

        # Running create()
        sts.create(self.test_project_id, self.test_symbol, self.test_decimals, self.test_owner, self.test_total_supply)
        
        # Pull output from storage
        storage = StorageManager()
        output = storage.get_double('STS', self.test_project_id)

        # Check Test
        if output == self.test_sts_info:
            print('test_create PASSED')
            return True
        
        print('test_create FAILED')
        return False

    def test_start_new_crowdfund(self):
        sts = SmartTokenShare()

        # Running start_new_crowdfund()
        sts.start_new_crowdfund(self.test_project_id, self.test_funding_stage_id, self.test_start_block, self.test_end_block, self.test_supply, self.test_tokens_per_gas)
        
        # Pull output from storage
        storage = StorageManager()
        output = storage.get_triple('STS', self.test_project_id, self.test_funding_stage_id)

        # Check Test
        if output == self.test_crowdfund_info:
            print('test_start_new_crowdfund PASSED')
            return True
        
        print('test_start_new_crowdfund FAILED')
        return False

    def test_crowdfund_available_amount(self):
        sts = SmartTokenShare()

        # Running crowdfund_available_amount()
        available = sts.crowdfund_available_amount(self.test_project_id, self.test_funding_stage_id)
        
        test_available = self.test_supply - 0

        # Check Test
        if available == test_available:
            print('test_crowdfund_available_amount PASSED')
            return True
        
        print('test_crowdfund_available_amount FAILED')
        return False

    def test_add_to_crowdfund_circulation(self):
        sts = SmartTokenShare()

        # Setting default info
        storage = StorageManager()
        storage.put_triple('STS', self.test_project_id, self.test_funding_stage_id, self.test_crowdfund_info)    


        # Running add_to_crowdfund_circulation()
        sts.add_to_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        sts.add_to_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        sts.add_to_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        
        in_circ = sts.get_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id)

        test_in_circ = self.test_add_amount * 3

        # Check Test
        if in_circ == test_in_circ:
            print('test_add_to_crowdfund_circulation PASSED')
            return True
        
        print('test_add_to_crowdfund_circulation FAILED')
        return False

    def test_get_crowdfund_circulation(self):
        sts = SmartTokenShare()

        # Setting default info
        storage = StorageManager()
        storage.put_triple('STS', self.test_project_id, self.test_funding_stage_id, self.test_crowdfund_info)    

        sts.add_to_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id, self.test_add_amount)
        
        # Running get_crowdfund_circulation()
        in_circ = sts.get_crowdfund_circulation(self.test_project_id, self.test_funding_stage_id)

        # Check Test
        if in_circ == self.test_add_amount:
            print('test_get_crowdfund_circulation PASSED')
            return True
        
        print('test_get_crowdfund_circulation FAILED')
        return False 





    def test_total_available_amount(self):
        sts = SmartTokenShare()

        # Running crowdfund_available_amount()
        available = sts.total_available_amount(self.test_project_id, self.test_funding_stage_id)
        
        test_available = self.test_total_supply - 0

        # Check Test
        if available == test_available:
            print('test_total_available_amount PASSED')
            return True
        
        print('test_total_available_amount FAILED')
        return False

    def test_add_to_total_circulation(self):
        sts = SmartTokenShare()

        # Setting default info
        storage = StorageManager()
        storage.put_double('STS', self.test_project_id, self.test_sts_info)

        # Running add_to_crowdfund_circulation()
        sts.add_to_total_circulation(self.test_project_id, self.test_add_amount)
        sts.add_to_total_circulation(self.test_project_id, self.test_add_amount)
        sts.add_to_total_circulation(self.test_project_id, self.test_add_amount)
        
        in_circ = sts.get_total_circulation(self.test_project_id)

        test_in_circ = self.test_add_amount * 3

        # Check Test
        if in_circ == test_in_circ:
            print('test_add_to_total_circulation PASSED')
            return True
        
        print('test_add_to_total_circulation FAILED')
        return False

    def test_get_total_circulation(self):
        sts = SmartTokenShare()

        # Setting default info
        storage = StorageManager()
        storage.put_double('STS', self.test_project_id, self.test_sts_info) 

        sts.add_to_total_circulation(self.test_project_id, self.test_add_amount)
        
        # Running get_crowdfund_circulation()
        in_circ = sts.get_crowdfund_circulation(self.test_project_id)

        # Check Test
        if in_circ == self.test_add_amount:
            print('test_get_total_circulation PASSED')
            return True
        
        print('test_get_total_circulation FAILED')
        return False 