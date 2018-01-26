from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat, list, range, take, substr

from construct.platform.FundingStage import FundingStage
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingRoadmap():
    """
    Stores and Manages the interaction between the Funding Stages, Milestones and the 
    SmartTokenShare.
    """
    project_id = ''

    def set_project_id(self, project_id):
        """Sets the current FundingRoadmap reference project_id
        Args:
            project_id (str):
                ID for referencing the project
        """    
        self.project_id = project_id

    def get_funding_stages(self):
        """    
        Registers all input addresses 
        Return:
            (list): The number of addresses to registered for KYC
        """
        storage = StorageManager()
       
        serialized_stages = storage.get_double('FS_stages', self.project_id)
        funding_stages = storage.deserialize_bytearray(serialized_stages)

        return funding_stages

    def add_funding_stages(self, new_funding_stages:list):
        """Adds the input list of funding stages to storage (as serialized array)
        Args:
            new_funding_stages (list):
                list of funding stages to save to storage
        """   
        storage = StorageManager()

        serialized_cur_fs = storage.get_double('FS_stages', self.project_id)
        serialized_new_fs = storage.serialize_array(add_funding_stages)
        
        serialized_combined_fs = concat(serialized_cur_fs, serialized_new_fs)

        serialized_cur_fs = storage.put_double('FS_stages', self.project_id, serialized_combined_fs)
