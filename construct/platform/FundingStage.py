from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingStage():
    """
    Manages the Smart Token Share in the contex of a funding roadmap, controls when news 
    crowdsales
    """
    sts = SmartTokenShare()
    funding_stage_id = ''
    sts_supply = 0
    start_block = 0
    end_block = 0
    tokens_per_gas = 0 # as * 10^8 decimals

    def create(self, sts:SmartTokenShare, funding_stage_id:str, sts_supply:int, start_block:int, end_block:int, tokens_per_gas:int):
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
        self.sts = SmartTokenShare()
        self.funding_stage_id = funding_stage_id
        self.sts_supply = sts_supply
        self.start_block = start_block
        self.end_block = end_block
        self.tokens_per_gas = tokens_per_gas

        # Need to update sts to current 
        sts.start_new_crowdfund(sts.project_id, start_block, end_block, sts_supply, tokens_per_gas)
    
