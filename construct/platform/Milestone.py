from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction

from construct.common.StorageManager import attrs_is_valid, serialize, deserialize, get_triple, put_triple

# Struct for storing the Milestone
ATTRS = {}
ATTRS['project_id'] = ''
ATTRS['milestone_id'] =  ''
ATTRS['title'] = ''
ATTRS['subtitle'] = ''
ATTRS['extra_info_hash'] = ''
ATTRS['progress'] = 0


def ms_is_valid(attrs):
    # Keys to check
    keys = [
        'project_id',
        'milestone_id',
        'title',
        'subtitle',
        'extra_info_hash',
        'progress']
    
    is_valid = attrs_is_valid(attrs, keys)

    if not is_valid:
        Notify('Invalid Milestone Attrs..')

    return is_valid

def ms_get_attr(attrs, attr_name):
    """
    This is required to be able to read fs object variables in certain cases..
    """
    # Check if invalid
    if not ms_is_valid(attrs):
        return

    return attrs[attr_name]

def ms_create(project_id, milestone_id, title, subtitle, extra_info_hash):
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
    # If sts with project id already exists
    pre_existing = ms_load_attrs(project_id, milestone_id)
    if pre_existing:
        return pre_existing

    # New funding stage attrs dict
    ms = ATTRS

    # Saves vars to object
    ms['project_id'] = project_id
    ms['milestone_id'] = milestone_id
    ms['title'] = title
    ms['subtitle'] = subtitle
    ms['extra_info_hash'] = extra_info_hash
    ms['progress'] = 0
    
    return ms

def ms_load_attrs(project_id, milestone_id):    
    # Pulling serialized attrs from storage
    serialized_attrs = get_triple('MS', project_id, milestone_id)
    attrs = deserialize(serialized_attrs)

    # Check if invalid
    if not ms_is_valid(attrs):
        return
    
    return attrs

def ms_save_attrs(attrs):    
    # Check if invalid
    if not ms_is_valid(attrs):
        return

    # Putting serialized attrs to storage
    serialized_attrs = serialize(attrs)
    put_triple('MS', attrs['project_id'], attrs['milestone_id'], serialized_attrs)

def ms_update_progress(attrs, updated_progress):
    """
    Args:
        ms (Milestone):
            Milestone object containing specific attributes
        
        updated_progress (int):
            New progress of the milestone

    Return:
        (int): The avaliable tokens for the Milestone
    """
    # If the updated progress is higher
    if updated_progress > attrs['progress']:
        
        # Clamp at 100%
        if updated_progress > 100:
            updated_progress = 100

        # Updates object variable
        attrs['progress'] = updated_progress
        
    
    return attrs['progress']
