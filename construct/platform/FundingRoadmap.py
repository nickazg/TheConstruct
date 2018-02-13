from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat, list, range, take, substr


from construct.platform.FundingStage import FundingStage
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class FundingRoadmap():
    """
    Interface for Managing the Funding Roadmap
    """
    def get_methods(self, address):
        
        # public
        methods = ['getMilestones', 'getFundinsStages', 'getActiveIndex']
        
        # MIGHT NOT work like this... 
        project_admins = self.get_project_admins()
        if address in project_admins:
            # admin
            methods += ['addMilestones', 'addFundingStages', 'setActiveIndex']

        return methods

    def add_list(self, project_id, key, new_list:list):
        """Adds the input list of funding stages to storage (as serialized array)
        Args:
            new_list (list):
                list of funding stages to save to storage
        """   
        storage = StorageManager()

        # Gets current stored list
        serialized_list = storage.get_double(key, project_id)

        # Serializes list 
        serialized_new_list = storage.serialize_array(new_list)

        # Updates list
        serialized_combined_lists = concat(serialized_list, serialized_new_list)

        # Saves updated serialized list to storage
        storage.put_double(key, project_id, serialized_combined_lists)

    def get_list(self, project_id, key):
        """    
        Registers all input addresses 
        Return:
            (list): Output list for key
        """
        storage = StorageManager()

        # Gets current stored list
        serialized_list = storage.get_double(key, project_id)

        # Converts serialized list to normal list
        output_list = storage.deserialize_bytearray(serialized_list)

        return output_list

    def add_funding_stages(self, project_id, new_funding_stages:list):
        """Adds the input list of funding stages to storage (as serialized array)
        Args:
            new_funding_stages (list):
                list of funding stages to save to storage
        """  
        self.add_list(project_id, 'FR_stages', new_funding_stages)
    
    def get_funding_stages(self, project_id):
        """    
        Registers all input addresses 
        Return:
            (list): The number of addresses to registered for KYC
        """
        funding_stages = get_list(project_id, 'FR_stages')
        
        return funding_stages

    def add_milestones(self, project_id, new_milestones:list):
        """Adds the input list of milestones to storage (as serialized array)
        Args:
            new_milestones (list):
                list of milestones to add
        """ 
        self.add_list(project_id, 'FR_milestones', new_milestones)  
    
    def get_milestones(self, project_id):
        """    
        Gets all milestones saved to storage
        Return:
            (list): The number of milestones
        """
        milestones = get_list(project_id, 'FR_milestones')

        return milestones

    def add_project_admins(self, project_id, new_admins:list):
        """Adds the input list of admins to storage (as serialized array)
        Args:
            new_milestones (list):
                list of admins to add
        """ 
        self.add_list(project_id, 'FR_admins', new_admins)    

    def get_project_admins(self, project_id):
        """    
        Gets all admins saved to storage
        Return:
            (list): The number of admins
        """
        admins = get_list(project_id, 'FR_admins')

        return admins