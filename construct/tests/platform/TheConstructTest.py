# from construct.platform.FundingStage import FundingStage
from construct.platform.FundingRoadmap import FundingRoadmap
# from construct.platform.SmartTokenShare import SmartTokenShare
# from construct.platform.Milestone import Milestone
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments

from construct.platform.SmartTokenShareNew import SmartTokenShare, sts_get_attr, sts_create, sts_get, get_total_in_circulation 
from construct.platform.FundingStageNew import FundingStage, fs_get_attr, fs_create, fs_get, fs_contribute, fs_status, fs_can_exchange, fs_add_to_circulation, fs_calculate_can_exchange, get_in_circulation, fs_claim_contributions, fs_refund, fs_get_addr_balance, fs_set_addr_balance

from construct.platform.MilestoneNew import Milestone, ms_create, ms_get, ms_update_progress, ms_get_progress

class TheConstructTest():
    """
    Test the TheConstruct from start to finish
    """

    project_id = 'projectID'
    symbol = 'PRO'
    decimals = 8
    owner = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
    total_supply = 10000000 * 100000000
    add_amount = 150

    funding_stage_id = 'funding_stage_id'
    start_block = 1
    end_block = 22000
    supply = 100000
    tokens_per_gas = 100
    



    def test(self, operation, args):

        
        # sts = SmartTokenShare()
        fr = FundingRoadmap()
        # fs = FundingStage()
        # ms = Milestone()

        storage = StorageManager()
        attachments = get_asset_attachments()

        if operation == 'create_all':
            print('create_all')

            sts_create(self.project_id, self.symbol, self.decimals, self.owner, self.total_supply)
            fs_create(self.project_id, 'first_stage', 1, 999999, 1000, 100)
            fs_create(self.project_id, 'second_stage', 1, 12750, 500, 100)
            fs_create(self.project_id, 'third_stage', 1, 12450, 100, 100)
            fs_create(self.project_id, 'fourth_stage', 1, 99999, 200, 100)
            
            fss = ['first_stage', 'second_stage', 'third_stage', 'fourth_stage']

            ms_create(self.project_id, 'first_mile', 'First', 'sub', 'hash')
            ms_create(self.project_id, 'second_mile', 'First', 'sub', 'hash')
            ms_create(self.project_id, 'third_mile', 'First', 'sub', 'hash')
            ms_create(self.project_id, 'fourth_mile', 'First', 'sub', 'hash')
            
            mss = ['first_mile', 'second_mile', 'third_mile', 'fourth_mile']

            admins = [self.owner]

            fr.add_funding_stages(self.project_id, fss)
            fr.add_milestones(self.project_id, mss)
            fr.add_project_admins(self.project_id, admins)
            fr.set_active_index(self.project_id, 0)

            return True
            

        if operation == 'get_funding_stages':
            print('get_funding_stages')

            stages = fr.get_funding_stages(self.project_id)
            print(stages)

            return stages

        
        if operation == 'kyc':
            print('attachments.sender_addr')
            print(attachments.sender_addr)
            storage.put_triple(self.project_id, 'KYC_address', self.owner, True)
          

        if operation == 'calim_test':
            storage.put_double('CLAIM', attachments.sender_addr, attachments.gas_attached)


        if operation == 'contribute':
            print('#contribute')
            # Registers KYC address
            storage.put_triple(self.project_id, 'KYC_address', attachments.sender_addr, True)
            
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]

            fs = fs_get(self.project_id, active_funding_stage)
            
            fs_contribute(fs)
            # storage.put_double('CLAIM', attachments.sender_addr, attachments.gas_attached)
            print('contribute#')

        if operation == 'get_idx':
            active_idx = fr.get_active_index(self.project_id)
            print(active_idx)
            return active_idx

        if operation == 'get_active_fs':
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            print(active_funding_stage)
            return active_funding_stage
        
        # 4 Put == (1 GAS per KB)
        # 7 Get == 0.7 GAS
        if operation == 'contribute_fs':
            print('#contribute_fs')

            active_funding_stage = args[0]
            
            fs = fs_get(self.project_id, active_funding_stage)
            fs_contribute(fs)
            
            print('contribute_fs#')
        
        
        if operation == 'balance':
            print('balance')
            # bal = storage.get_double(self.project_id, attachments.sender_addr)
            fs_id = args[0]
            addr = args[1]
            
            fs = fs_get('projectID', fs_id)
            bal = fs_get_addr_balance(fs, addr)
            print(bal)

        if operation == 'funding_stage_status':
            print('#funding_stage_status')
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            

            fs = fs_get(self.project_id, active_funding_stage)
            status = fs_status(fs)

            print('funding_stage_status#')
            print(status)
            return status

        if operation == 'current_index':
            active_idx = fr.get_active_index(self.project_id)
            print(active_idx)
            return active_idx
        
        if operation == 'milestone_progress':
            print('#milestone_progress')
            active_idx = fr.get_active_index(self.project_id)
            milestones = fr.get_milestones(self.project_id)
            active_milestone = milestones[active_idx]

            ms = ms_get(self.project_id, active_milestone)
            prog = ms_get_progress(ms)
            print('milestone_progress#')
            print(prog)
            return prog

        if operation == 'complete_milestone':
            print('complete_milestone')
            fr.update_milestone_progress(self.project_id, 100)
            
        if operation == 'sts_get':
            sts = sts_get('projectID')
            arg = args[0]            

            if arg == 'project_id':
                return sts.project_id

            if arg == 'symbol':
                return sts.symbol

            if arg == 'decimals':
                return sts.decimals
            
            if arg == 'owner':
                return sts.owner
            
            if arg == 'total_supply':
                return sts.total_supply

            if arg == 'total_in_circulation':
                return get_total_in_circulation(sts)

        if operation == 'fs_get':
            active_idx = fr.get_active_index('projectID')
            funding_stages = fr.get_funding_stages('projectID')
            active_funding_stage = funding_stages[active_idx]
            
            fs = fs_get('projectID', active_funding_stage)

            arg = args[0]
            # attr = fs_get_attr(fs, arg)
            
            if arg == 'project_id':
                return fs.project_id

            if arg == 'funding_stage_id':
                return fs.funding_stage_id

            if arg == 'start_block':
                return fs.start_block
            
            if arg == 'end_block':
                return fs.end_block
            
            if arg == 'supply':
                return fs.supply

            if arg == 'tokens_per_gas':
                return fs.tokens_per_gas

            if arg == 'in_circulation':
                return get_in_circulation(fs)

        if operation == 'fs_claim_contributions':
            fs_id = args[0]
            deposit_addr = args[1]
            fs = fs_get('projectID', fs_id)
            fs_claim_contributions(fs, deposit_addr)

        if operation == 'fs_refund':
            fs_id = args[0]
            refund_addr = args[1]
            fs = fs_get('projectID', fs_id)
            fs_refund(fs, refund_addr)
        
        return True

