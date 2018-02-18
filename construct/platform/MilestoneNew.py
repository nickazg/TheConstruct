from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class Milestone():
    """
    Interface for managing milestones
    """
    project_id = ''
    milestone_id = ''
    title = ''
    subtitle = '' 
    extra_info_hash = ''
    progress = 0

def ms_create(project_id, milestone_id, title, subtitle, extra_info_hash) -> Milestone:

    storage = StorageManager()
    ms = Milestone()
    
    ms.project_id = project_id
    ms.milestone_id = milestone_id
    ms.title = title
    ms.subtitle = subtitle 
    ms.extra_info_hash = extra_info_hash   

    # Sets progress to 0
    ms.progress = 0

    # Info structure
    milestone_info = [0, title, subtitle, extra_info_hash]

    # Saving info to storage
    milestone_info_serialized = storage.serialize_array(milestone_info)
    storage.put_triple('MS', project_id, milestone_id, milestone_info_serialized)

    return ms
    
def ms_get(project_id, milestone_id) -> Milestone:
    """
    Get the info list

    Args:
        project_id (str):
            ID for referencing the project
    Return:
        (list): info list
    """    
    storage = StorageManager()
    ms = Milestone()
    
    # Pull milestone info
    milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
    milestone_info = storage.deserialize_bytearray(milestone_info_serialized)
    

    # info into vars
    project_id = project_id
    milestone_id = milestone_id
    title = milestone_info[1]
    subtitle = milestone_info[2]
    extra_info_hash = milestone_info[3]
    progress = milestone_info[0]

    return ms


def ms_update_progress(ms:Milestone, updated_progress):
    storage = StorageManager()

    # # Pull milestone info
    # milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
    # milestone_info = storage.deserialize_bytearray(milestone_info_serialized)
    
    # # Milestone vars
    # progress = milestone_info[0]
    # title = milestone_info[1]
    # subtitle = milestone_info[2]
    # extra_info_hash = milestone_info[3]

    # If the updated progress is higher
    if updated_progress > ms.progress:
        
        ms.progress = updated_progress
        
        # Output milestone info
        updated_milestone_info = [ms.progress, ms.title, ms.subtitle, ms.extra_info_hash]

        # Saving info to storage
        updated_milestone_info_serialized = storage.serialize_array(updated_milestone_info)
        storage.put_triple('MS', project_id, milestone_id, updated_milestone_info_serialized)


def ms_get_progress(ms:Milestone):

    # storage = StorageManager()
    
    # # Pull milestone info
    # milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
    # milestone_info = storage.deserialize_bytearray(milestone_info_serialized)

    # # Milestone vars
    # progress = milestone_info[0]

    return ms.progress