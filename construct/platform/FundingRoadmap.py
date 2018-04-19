from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.builtins import concat, list, range, take, substr

from construct.common.StorageManager import attrs_is_valid, array_concat, get_double, put_double, serialize, deserialize

from construct.platform.FundingStage import fs_load_attrs, fs_save_attrs, fs_status
from construct.platform.Milestone import ms_load_attrs, ms_save_attrs, ms_update_progress

# Struct for storing the Funding Roadmap
ATTRS = {}
ATTRS['project_id'] = ''
ATTRS['active_idx'] =  0
ATTRS['funding_stages'] = []
ATTRS['milestones'] = []
ATTRS['admins'] = []

def fr_is_valid(attrs):
    # Keys to check
    keys = ['project_id', 'active_idx', 'funding_stages', 'milestones', 'admins']
    
    is_valid = attrs_is_valid(attrs, keys)

    if not is_valid:
        Notify('Invalid Funding Roadmap Attrs..')

    return is_valid

def fr_create(project_id):
    # New funding roadmap attrs dict
    fr = ATTRS

    # Saves updated project_id
    fr['project_id'] = project_id

    return fr

def fr_load_attrs(project_id):    
    # Pulling serialized attrs from storage
    serialized_attrs = get_double('FR', project_id)
    if not serialized_attrs:
        Notify('No Attrs exist for Funding Roadmap, Creating new one.')
        return fr_create(project_id)

    attrs = deserialize(serialized_attrs)
    
    # Check if invalid
    if not fr_is_valid(attrs):
        return
    
    return attrs

def fr_save_attrs(attrs):
    # Putting serialized attrs to storage
    serialized_attrs = serialize(attrs)
    put_double('FR', attrs['project_id'], serialized_attrs)

def fr_get_attr(attrs, attr_name):
    """
    This is required to be able to read fs object variables in certain cases..
    """
    # Check if invalid
    if not fr_is_valid(attrs):
        return

    return attrs[attr_name]

def fr_add_funding_stage(attrs, new_funding_stage):
    """Adds the input list of funding stages to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_funding_stages (list): list of funding stages to save to storage
    """
    updated = array_concat(attrs['funding_stages'], [new_funding_stage])
    attrs['funding_stages'] = updated

def fr_add_milestone(attrs, new_milestone):
    """Adds the input list of milestones to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_milestones (list): list of milestones to add
    """ 
    updated = array_concat(attrs['milestones'], [new_milestone])
    attrs['milestones'] = updated

def fr_add_project_admin(attrs, new_admin):
    """Adds the input list of admins to storage (as serialized array)
    Args:
        project_id (list): ID for referencing the project
        new_milestones (list): list of admins to add
    """ 
    updated = array_concat(attrs['admins'], [new_admin])
    attrs['admins'] = updated  

def fr_set_active_index(attrs, idx):
    """    
    Sets the active index
    Args:
        project_id (list): ID for referencing the project
        idx (int): new active index    
    """
    attrs['active_idx'] = idx

def fr_update_milestone_progress(attrs, progress):
    """    
    Updates the progress of the active index, and runs neccerray checks
    
    Args:
        project_id (list): ID for referencing the project
        progress (int): new progress (100% completes stage/milestone)   
    """
    active_idx = fr_get_attr(attrs, 'active_idx')
    milestones = fr_get_attr(attrs, 'milestones')
    funding_stages = fr_get_attr(attrs, 'funding_stages')

    active_milestone = milestones[active_idx]
    active_funding_stage = funding_stages[active_idx]

    ms_attrs = ms_load_attrs(attrs['project_id'], active_milestone)
    fs_attrs = fs_load_attrs(attrs['project_id'], active_funding_stage)

    if fs_status(fs_attrs) != 1:
        print('Current Funding Stage NOT complete')
        return False
        
    if progress > 100:
        progress = 100
        
    if progress == 100:
        print('progress 100%')
        next_idx = active_idx + 1          
        fr_set_active_index(attrs, next_idx)

    # Update and save milestone attrs to storage 
    ms_update_progress(ms_attrs, progress)   
    ms_save_attrs(ms_attrs)

    return progress