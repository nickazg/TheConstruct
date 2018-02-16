from construct.platform.FundingStage import FundingStage
from construct.platform.FundingRoadmap import FundingRoadmap
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.platform.Milestone import Milestone
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments

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

        
        sts = SmartTokenShare()
        fr = FundingRoadmap()
        fs = FundingStage()
        ms = Milestone()

        storage = StorageManager()
        attachments = get_asset_attachments()

        if operation == 'create_all':
            print('create_all')

            sts.create(self.project_id, self.symbol, self.decimals, self.owner, self.total_supply)
            fs.create(self.project_id, 'first_stage', 1, 99999, 1000, 100)
            fs.create(self.project_id, 'second_stage', 1, 99999, 500, 100)
            fs.create(self.project_id, 'third_stage', 1, 99999, 100, 100)
            fs.create(self.project_id, 'fourth_stage', 1, 99999, 200, 100)
            
            fss = ['first_stage', 'second_stage', 'third_stage', 'fourth_stage']

            ms.create(self.project_id, 'first_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'second_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'third_mile', 'First', 'sub', 'hash')
            ms.create(self.project_id, 'fourth_mile', 'First', 'sub', 'hash')
            
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

        
        if operation == 'contribute':
            print('#contribute')
            # Registers KYC address
            storage.put_triple(self.project_id, 'KYC_address', attachments.sender_addr, True)
            
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            x = fs.exchange(self.project_id, active_funding_stage)
            print('contribute#')
            print(x)
        
        
        if operation == 'balance':
            print('balance')
            bal = storage.get_double(self.project_id, self.owner)
            print(bal)

        if operation == 'funding_stage_status':
            print('#funding_stage_status')
            active_idx = fr.get_active_index(self.project_id)
            funding_stages = fr.get_funding_stages(self.project_id)
            active_funding_stage = funding_stages[active_idx]
            fs_status = fs.status(self.project_id, active_funding_stage)
            print('funding_stage_status#')
            print(fs_status)

        if operation == 'current_index':
            active_idx = fr.get_active_index(self.project_id)
            print(active_idx)
        
        if operation == 'milestone_progress':
            print('#milestone_progress')
            active_idx = fr.get_active_index(self.project_id)
            milestones = fr.get_milestones(self.project_id)
            active_milestone = milestones[active_idx]

            prog = ms.get_progress(self.project_id, active_milestone)
            print('milestone_progress#')
            print(prog)

        if operation == 'complete_milestone':
            print('complete_milestone')
            fr.update_milestone_progress(self.project_id, 100)
    
        return True