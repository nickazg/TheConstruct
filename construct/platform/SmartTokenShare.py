from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.builtins import list

from construct.common.StorageManager import attrs_is_valid, get_double, put_double, serialize, deserialize

# Struct for storing the Smart Token Share
ATTRS = {}
ATTRS['project_id'] = ''
ATTRS['symbol'] =  ''
ATTRS['decimals'] = 0
ATTRS['owner'] = ''
ATTRS['total_supply'] = 0
ATTRS['total_in_circulation'] = 0


def sts_is_valid(attrs):
    # Keys to check
    keys = [
        'project_id',
        'symbol',
        'decimals',
        'owner',
        'total_supply',
        'total_in_circulation']

    is_valid = attrs_is_valid(attrs, keys)

    if not is_valid:
        Notify('Invalid Smart Token Shares Attrs..')

    return is_valid

def sts_get_attr(attrs, attr_name):
    """
    This is required to be able to read sts object variables in certain cases..
    """

    # Check if invalid
    if not sts_is_valid(attrs):
        return

    return attrs[attr_name]

def sts_create(project_id, symbol, decimals, owner, total_supply):
    """
    Args:
        project_id (str):
            ID for referencing the project

        symbol (str):
            Representation symbol
            
        decimals (int):
            Amount of decimal places, default 8

        owner (bytes):
            Owner of the token

        total_supply (int):
            total supply of the token
    Return:
        (SmartTokenShare): 
            Returns a Smart Token Share object containing these attributes
    """
    # If sts with project id already exists
    pre_existing = sts_load_attrs(project_id)
    if pre_existing:
        return pre_existing

    # New funding stage attrs dict
    sts = ATTRS

    # Saves vars to object
    sts['project_id'] = project_id
    sts['symbol'] = symbol
    sts['decimals'] = decimals
    sts['owner'] = owner
    sts['total_supply'] = total_supply
    sts['total_in_circulation'] = 0
    
    return sts

def sts_load_attrs(project_id):    
    # Pulling serialized attrs from storage
    serialized_attrs = get_double('STS', project_id)
    if not serialized_attrs:
        Notify('No Attrs exist for Smart Token Share')
        return
    
    attrs = deserialize(serialized_attrs)
    
    # Check if invalid
    if not sts_is_valid(attrs):
        return
    
    return attrs

def sts_save_attrs(attrs):
    
    # Check if invalid
    if not sts_is_valid(attrs):
        return

    # Putting serialized attrs to storage
    print('attrs')
    print(attrs)
    serialized_attrs = serialize(attrs)
    put_double('STS', attrs['project_id'], serialized_attrs)


def sts_total_available_amount(attrs):
    """
    Args:
        sts (SmartTokenShare):
            Smart Token Share object containing specific attributes

    Return:
        (int): The avaliable tokens for the total project
    """
    available = attrs['supply'] - attrs['total_in_circulation']

    return available

def sts_add_to_total_circulation(attrs, amount):
    """
    Adds an amount of token to circlulation

    Args:
        sts (SmartTokenShare):
            Smart Token Share object containing specific attributes

        amount (int):
            amount of tokens added
    """  
    # Calculation
    attrs['total_in_circulation'] += amount