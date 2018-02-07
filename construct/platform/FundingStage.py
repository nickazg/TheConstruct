from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

from boa.code.builtins import list


class FundingStage():
    """
    Interface for managing Funding Stages
    """
    def create(self, project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas):
        """
        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
                
            start_block (int):
                Block to start fund

            end_block (int):
                Block to end fund

            supply (int):
                Supply of the token in this fs

            tokens_per_gas (int):
                Token to gas ratio
        Return:
            (None): 
        """
        storage = StorageManager()
        
        # Default circulation
        in_circulation = 0
        
         # Info structure
        fs_info = [start_block, end_block, supply, tokens_per_gas, in_circulation]

        # Saving info to storage
        fs_info_serialized = storage.serialize_array(fs_info)
        storage.put_triple('FS', project_id, funding_stage_id, fs_info_serialized)

    def available_amount(self, project_id, funding_stage_id):
        """
        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
        Return:
            (int): The avaliable tokens for the current sale
        """
        storage = StorageManager()
        
        # Pull FundingStage info
        fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)
        fs_info = storage.deserialize_bytearray(fs_info_serialized)

        # FundingStage vars
        in_circulation = fs_info[4]
        supply = fs_info[2]

        available = supply - in_circulation

        return available

    def add_to_circulation(self, project_id, funding_stage_id, amount):
        """
        Adds an amount of token to circlulation

        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage

            amount (int):
                amount of tokens added  
        """
        storage = StorageManager()
        
        # Pull FundingStage info
        fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)
        fs_info = storage.deserialize_bytearray(fs_info_serialized)

        # info into vars
        start_block = fs_info[0]
        end_block = fs_info[1]
        supply = fs_info[2]
        tokens_per_gas = fs_info[3]
        in_circulation = fs_info[4]

        # Calculation
        updated_in_circulation = in_circulation + amount

        # output STS info
        updated_fs_info = [start_block, end_block, supply, tokens_per_gas, updated_in_circulation]
        
        # Save STS info
        updated_fs_info_serialized = storage.serialize_array(updated_fs_info)
        storage.put_triple('FS', project_id, funding_stage_id, updated_fs_info_serialized)

        
        # # Update sts **
        sts = SmartTokenShare()
        sts.add_to_total_circulation(project_id, amount)

    def get_circulation(self, project_id, funding_stage_id):
        """
        Get the total amount of tokens in circulation

        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
        Return:
            (int): The total amount of tokens in circulation
        """        
        storage = StorageManager()
        
        # Pull FundingStage info
        fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)
        fs_info = storage.deserialize_bytearray(fs_info_serialized)

        # in_circulation var
        in_circulation = fs_info[4]

        return in_circulation
