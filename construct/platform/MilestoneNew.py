from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
# from boa.code.builtins import concat

# # from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class Milestone():
    """
    Object for managing milestones
    """
    project_id = ''
    milestone_id = ''
    title = ''
    subtitle = '' 
    extra_info_hash = ''
    progress = 0

def ms_create(project_id, milestone_id, title, subtitle, extra_info_hash) -> Milestone:
    """
    Creates a new Milestone using the input attributes, saves it to storage and returns
    a Milestone object
    Args:
        project_id (str):
            ID for referencing the project

        milestone_id (str):
            ID for referencing the Milestone
            
        title (str):
            Block to start fund

        subtitle (str):
            Block to end fund

        extra_info_hash (str):
            Supply of the token in this fs

    Return:
        (Milestone):
            Returns a Milestone object containing these attributes
    """
    # init objects
    storage = StorageManager()
    ms = Milestone()

    # Saves vars to object
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
    Pulls an existing Milestone from storage using the input attributes, and returns
    a Milestone object
    Args:
        project_id (str):
            ID for referencing the project

        milestone_id (str):
            ID for referencing the Milestone
            
    Return:
        (Milestone):
            Returns a Milestone object containing attributes
    """
    storage = StorageManager()
    ms = Milestone()
    
    # Pull Milestone info
    milestone_info_serialized = storage.get_triple('MS', project_id, milestone_id)
    milestone_info = storage.deserialize_bytearray(milestone_info_serialized)
    
    # Saves vars to object
    ms.project_id = project_id
    ms.milestone_id = milestone_id
    ms.title = milestone_info[1]
    ms.subtitle = milestone_info[2]
    ms.extra_info_hash = milestone_info[3]
    ms.progress = milestone_info[0]

    return ms


def ms_update_progress(ms:Milestone, updated_progress):
    """
    Args:
        ms (Milestone):
            Milestone object containing specific attributes
        
        updated_progress (int):
            New progress of the milestone

    Return:
        (int): The avaliable tokens for the Milestone
    """
    storage = StorageManager()

    # If the updated progress is higher
    if updated_progress > ms.progress:

        # Clamp at 100%
        if updated_progress > 100:
            updated_progress = 100
        
        # Updates object variable
        ms.progress = updated_progress
        
        # Output milestone info
        updated_milestone_info = [ms.progress, ms.title, ms.subtitle, ms.extra_info_hash]

        # Saving info to storage
        updated_milestone_info_serialized = storage.serialize_array(updated_milestone_info)
        storage.put_triple('MS', ms.project_id, ms.milestone_id, updated_milestone_info_serialized)


def ms_get_progress(ms:Milestone):
    """
    This is required specifically for this variable
    """
    return ms.progress