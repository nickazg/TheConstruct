from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat, list, range, take, substr

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingStage():
    """
    Manages the Smart Token Share in the contex of a funding roadmap, controls when news 
    crowdsales
    """
    def get_funding_stages(self, sts:SmartTokenShare):
        storage = StorageManager()
       
        serialized_stages = storage.get_double('FS_stages', sts.project_id)
        funding_stages = storage.deserialize_bytearray(serialized_stages)

        return funding_stages

    def add_funding_stages(self, sts:SmartTokenShare, new_funding_stages:list):
        storage = StorageManager()

        serialized_cur_fs = storage.get_double('FS_stages', sts.project_id)
        serialized_new_fs = storage.serialize_array(add_funding_stages)
        
        serialized_combined_fs = concat(serialized_cur_fs, serialized_new_fs)

        serialized_cur_fs = storage.put_double('FS_stages', sts.project_id, serialized_combined_fs)

    def start_new_crowdfund(self, sts:SmartTokenShare):
        sts.get_project_info(sts.project_id)
        start_block = 123
        end_block = 123123
        supply = 1110
        tokens_per_gas = 10 * (10**sts.decimal)
        sts.start_new_crowdfund(sts.project_id, start_block, end_block, supply, tokens_per_gas)
        return True