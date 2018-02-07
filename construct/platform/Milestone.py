from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class Milestone():
    """
    Interface for managing milestones
    """
    def create(self, project_id, milestone_id, title, subtitle, extra_info_hash):
    
        storage = StorageManager()
        
        # Sets progress to 0
        progress = 0

        # Info structure
        milestone_info = [progress, title, subtitle, extra_info_hash]

        # Saving info to storage
        milestone_info_serialized = storage.serialize_array(milestone_info)
        storage.put_triple('MS', project_id, milestone_id, milestone_info_serialized)
       
    def update_progress(self, project_id, milestone_id, updated_progress):
        storage = StorageManager()

        # Pull milestone info
        milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
        milestone_info = storage.deserialize_bytearray(milestone_info_serialized)
        
        # Milestone vars
        progress = milestone_info[0]
        title = milestone_info[1]
        subtitle = milestone_info[2]
        extra_info_hash = milestone_info[3]

        # If the updated progress is higher
        if updated_progress > progress:
            
            # Output milestone info
            updated_milestone_info = [updated_progress, title, subtitle, extra_info_hash]

            # Saving info to storage
            updated_milestone_info_serialized = storage.serialize_array(updated_milestone_info)
            storage.put_triple('MS', project_id, milestone_id, updated_milestone_info_serialized)


    def get_progress(self, project_id, milestone_id):

        storage = StorageManager()
        
        # Pull milestone info
        milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
        milestone_info = storage.deserialize_bytearray(milestone_info_serialized)

        # Milestone vars
        progress = milestone_info[0]

        return progress