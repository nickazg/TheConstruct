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
        storage = StorageManager()
        
        info_list = [sts_supply, start_block, end_block, tokens_per_gas]        
        
        serialized_info = storage.serialize_array(info_list)
        print('serialized_info')
        print(serialized_info)
        
        storage.put_double(project_id, funding_stage_id, serialized_info)

        return funding_stage_id
      
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
        # if len(info_list) == 4: # VM doesnt seem to like this..         
        return info_list

    def get_sts_supply(self, info_list:list):
        sts_supply = info_list[0]
        return sts_supply

    def get_start_block(self, info_list:list):
        start_block = info_list[1]
        return start_block

    def get_end_block(self, info_list:list):
        end_block = info_list[2]
        return end_block

    def get_tokens_per_gas(self, info_list:list):
        tokens_per_gas = info_list[3]
        return tokens_per_gas  