from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.common.FundingStage import FundingStage
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingRoadmap():
    """
    Stores and Manages the interaction between the Funding Stages, Milestones and the 
    SmartTokenShare.
    """
    project_id = ''

    def get_funding_roadmap(self, project_id):
        self.project_id = project_id

    def add_funding_stage(self, fs:FundingStage)
        storage = StorageManager()

        # funding_stages = storage.get_double('FR_funding_stages', self.project_id)