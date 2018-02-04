from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

from boa.code.builtins import list


class FundingStage():
    """
    Manages the Smart Token Share in the contex of a funding roadmap, controls when news 
    crowdsales
    """
    project_id = ''
    funding_stage_id = ''
    sts_supply = 0
    start_block = 0
    end_block = 0
    tokens_per_gas = 0 # as * 10^8 decimals

    def create(self, project_id:str, funding_stage_id:str, sts_supply:int, start_block:int, end_block:int, tokens_per_gas:int):
        """Setup the new funding stage, and creates a new crowdfund on the Smart Token Share
        Args:
            sts (SmartTokenShare):
                Smart Token Share reference object

            funding_stage_id (str):
                ID to reference the funding stage

            sts_supply (int):
                The supply of smart token shares to be distributed in this funding stage

            start_block (int):
                Starting block of the fund

            end_block (int):
                Ending block of the fund

            tokens_per_gas (int):
                Token multiplier for sts tokens to be distributed
        """  
        self.project_id = project_id
        self.funding_stage_id = funding_stage_id
        self.sts_supply = sts_supply
        self.start_block = start_block
        self.end_block = end_block
        self.tokens_per_gas = tokens_per_gas

        # Need to update sts to current 
        # sts =  SmartTokenShare()
        # sts.get_project_info(project_id)
        # sts.start_new_crowdfund(project_id, start_block, end_block, sts_supply, tokens_per_gas)

        return funding_stage_id

    def save_to_storage(self):
        """
        Saves the current funding stage to contract storage
        """
        storage = StorageManager()
        
        info_list = list(self.sts_supply, self.start_block, self.end_block, self.tokens_per_gas)
        
        serialized_info = storage.serialize_array(info_list)

        storage.put_double(self.project_id, self.funding_stage_id, serialized_info)

    
    def read_from_storage(self, project_id:str, funding_stage_id:str):
        """
        Description
        Args:
            sts (SmartTokenShare):
                Smart Token Share reference object

            funding_stage_id (str):
                ID to reference the funding stage
        Returns:
            (None):
        """
        storage =  StorageManager()
        
        # Getting the serialized list from storage
        serialized_info = storage.get_double(project_id, funding_stage_id)

        # Deserializing info to a list
        info_list = storage.deserialize_bytearray(serialized_info)

        # Populating neccearry variables
        self.project_id = project_id
        self.funding_stage_id = funding_stage_id
        self.sts_supply = info_list[0]
        self.start_block = info_list[1]
        self.end_block = info_list[2]
        self.tokens_per_gas = info_list[3]

