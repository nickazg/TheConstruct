from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat, list, range, take, substr


from construct.common.StorageManager import StorageManager

from construct.platform.FundingStage import FundingStage, fs_get_attr, fs_create, fs_get, fs_contribute, fs_status, fs_can_exchange, fs_add_to_circulation, fs_calculate_can_exchange, get_in_circulation
from construct.platform.Milestone import Milestone, ms_create, ms_get, ms_update_progress, ms_get_progress



class FundingRoadmap():
    """
    Interface for Managing the Funding Roadmap
    """
    project_id = ''
    active_idx = 0

def fr_list_append(project_id, key, new_item):
    """Adds the input list of funding stages to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_list (list): list of funding stages to save to storage
    """   
    storage = StorageManager()

    print('new_item')
    print(new_item)

    # Gets current stored list
    current_serialized_list = storage.get_double(project_id, key)

    # Converts serialized list to normal list
    current_list = storage.deserialize_bytearray(current_serialized_list)
    current_list_len = len(current_list)
    print('current_list_len')
    print(current_list_len)

    if current_list_len == 0:
        output_list = [new_item]
    
    else:
        output_list = current_list
        output_list.append(new_item)  
        # Notify(output_list)
        # output_list_len = current_list_len + 1
        # print('output_list_len')
        # print(output_list_len)
        
        # # Creates new list and appends new item to the end
        # output_list = list(length=output_list_len)
        # for i in range(0, current_list_len):    
        #     output_list[i] = current_list[i]    
    
    # output_list[-1] = new_item

    # Serializes list 
    serialized_output_list = storage.serialize_array(output_list)
    print('serialized_output_list')
    print(serialized_output_list)

    # Saves updated serialized list to storage
    storage.put_double(project_id, key, serialized_output_list)


def fr_get_list(project_id, key):
    """    
    Registers all input addresses
    Args:
        project_id (list): ID for referencing the project

    Return:
        (list): Output list for key
    """
    storage = StorageManager()

    # Gets current stored list
    serialized_list = storage.get_double(project_id, key)

    # Converts serialized list to normal list
    output_list = storage.deserialize_bytearray(serialized_list)
    # output_list = ['sdad','sdads']

    return output_list

def fr_add_funding_stage(project_id, new_funding_stage):
    """Adds the input list of funding stages to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_funding_stages (list): list of funding stages to save to storage
    """  
    fr_list_append(project_id, 'FR_stages', new_funding_stage)

def fr_get_funding_stages(project_id):
    """    
    Registers all input addresses
    Args:
        project_id (list): ID for referencing the project

    Return:
        (list): The number of addresses to registered for KYC
    """
    funding_stages = fr_get_list(project_id, 'FR_stages')
    print('funding_stages')
    print(funding_stages)
    return funding_stages

def fr_add_milestone(project_id, new_milestone):
    """Adds the input list of milestones to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_milestones (list): list of milestones to add
    """ 
    fr_list_append(project_id, 'FR_milestones', new_milestone)  

def fr_get_milestones(project_id):
    """    
    Gets all milestones saved to storage
    Args:
        project_id (list): ID for referencing the project
        
    Return:
        (list): The number of milestones
    """
    milestones = fr_get_list(project_id, 'FR_milestones')

    return milestones

def fr_add_project_admin(project_id, new_admin):
    """Adds the input list of admins to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_milestones (list): list of admins to add
    """ 
    fr_list_append(project_id, 'FR_admins', new_admin)    

def fr_get_project_admins(project_id):
    """    
    Gets all admins saved to storage
    Args:
        project_id (list): ID for referencing the project
    
    Return:
        (list): The number of admins
    """
    admins = fr_get_list(project_id, 'FR_admins')

    return admins


def fr_set_active_index(project_id, idx):
    """    
    Sets the active index
    Args:
        project_id (list): ID for referencing the project
        idx (int): new active index    
    """
    storage = StorageManager()
    storage.put_double(project_id, 'FR_active_idx', idx)

def fr_get_active_index(project_id):
    """    
    Gets the active index
    Args:
        project_id (list): ID for referencing the project
    
    Return:
        (int): Index
    """
    storage = StorageManager()
    idx = storage.get_double(project_id, 'FR_active_idx')
    return idx


def fr_update_milestone_progress(project_id, progress):
    """    
    Updates the progress of the active index, and runs neccerray checks
    
    Args:
        project_id (list): ID for referencing the project
        progress (int): new progress (100% completes stage/milestone)   
    """
    print('project_id')
    print(project_id)
    active_idx = fr_get_active_index(project_id)
    print('active_idx')
    print(active_idx)
    milestones = fr_get_milestones(project_id)
    funding_stages = fr_get_funding_stages(project_id)

    active_milestone = milestones[active_idx]
    active_funding_stage = funding_stages[active_idx]

    fs = fs_get(project_id, active_funding_stage)
    check_fs_status = fs_status(fs)
    
    print('check_fs_status')
    print(check_fs_status)

    if check_fs_status != 1:
        print('Current Funding Stage NOT complete')
        return False
        
    # ms = ms_get(project_id, active_milestone)  
    # updated_progress = ms_update_progress(ms, progress)

    if progress > 100:
        progress = 100
        
    if progress == 100:
        print('progress 100%')
        next_idx = active_idx + 1
        print('next_idx')
        print(next_idx)            
        fr_set_active_index(project_id, next_idx)

    # print('project_id')
    # print(project_id)
    ms = ms_get(project_id, active_milestone)
    ms_update_progress(ms, progress)
    
    return progress
        

        