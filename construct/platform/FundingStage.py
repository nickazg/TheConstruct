from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingStage():
    """
    Manages the Smart Token Share in the contex of a funding roadmap, controls when news 
    crowdsales
    """

    def start_new_crowdfund(self, sts:SmartTokenShare, start_block:int, end_block:int, supply:int, tokens_per_gas:int):
        sts.get_project_info(sts.project_id)
        # start_block = 123
        # end_block = 123123
        # supply = 1110
        tokens_per_gas_calculated = tokens_per_gas * (10**sts.decimal)
        sts.start_new_crowdfund(sts.project_id, start_block, end_block, supply, tokens_per_gas)
        return True