from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction

from construct.common.StorageManager import attrs_is_valid, serialize, deserialize, get_triple, put_triple

OnTransfer = RegisterAction('transfer','project_id' , 'from', 'to', 'amount')
OnRefund = RegisterAction('refund','project_id' , 'to', 'amount')

OnInvalidKYCAddress = RegisterAction('invalid_registration','project_id' ,'address')
OnKYCRegister = RegisterAction('kyc_registration','project_id' ,'address')

ATTRS = {}
ATTRS['address'] = ''
ATTRS['phys_address'] = '' 
ATTRS['first_name'] = '' 
ATTRS['last_name'] = '' 
ATTRS['id_type'] = '' 
ATTRS['id_number'] = '' 
ATTRS['id_expiry'] = '' 
ATTRS['file_location'] = '' 
ATTRS['file_hash'] = ''


def kyc_is_valid(attrs):
    # Keys to check
    keys = [
        'address',
        'phys_address', 
        'first_name', 
        'last_name', 
        'id_type', 
        'id_number', 
        'id_expiry', 
        'file_location', 
        'file_hash']
    
    is_valid = attrs_is_valid(attrs, keys)

    if not is_valid:
        Notify('Invalid KYC Attrs..')

    return is_valid

# User submit
def kyc_create(project_id, address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash):
    """    
    Submits a KYC information to the smart contract 
    Args:
        sts (SmartTokenShare):
            Smart Token Share reference object
        
        address (str):
            Wallet address to whitelist

        phys_address (str):
            Physical Address

        first_name (str):
            First Name

        last_name (str):
            Last Name

        id_type (str):
            Id type, eg passport, drivers licence

        id_number (str):
            ID Number

        id_expiry (str):
            Expiry data

        file_location (str):
            web location where file is stored

        file_hash (str):
            hash of file
    """
    # New funding stage attrs dict
    kyc = ATTRS

    # Saves vars to object
    kyc['address'] = address
    kyc['phys_address'] = phys_address
    kyc['first_name'] = first_name
    kyc['last_name'] = last_name
    kyc['id_type'] = id_type
    kyc['id_number'] = id_number
    kyc['id_expiry'] = id_expiry
    kyc['file_location'] = file_location
    kyc['file_hash'] = file_hash

    return kyc

def kyc_submit(attrs):    
    
    # Check if invalid
    if not kyc_is_valid(attrs):
        return

    if len(attrs['address']) != 20:
        Notify('Invalid address type')
        return
        
    # Checking its the correct address
    if not CheckWitness(attrs['address']):
        Notify('Can only submit your own address')
        return

    # Putting serialized attrs to storage
    serialized_attrs = serialize(attrs)
    put_triple('KYC', attrs['project_id'], attrs['address'], serialized_attrs)

def kyc_load_attrs(sts_attrs, address):
    
    if len(address) != 20:
        Notify('Invalid address type')
        return

    # Pulling serialized attrs from storage
    serialized_attrs = get_triple('KYC', sts_attrs['project_id'], address)
    if not serialized_attrs:
        Notify('No Attrs exist for KYC')
        return
    
    attrs = deserialize(serialized_attrs)

    # Check if invalid
    if not kyc_is_valid(attrs):  
        return
    
    # Will only return attrs if Admin or Submission creator
    if CheckWitness(sts_attrs['owner']) or CheckWitness(attrs['address']):
        return attrs

def kyc_get_attr(attrs, attr_name):
    """
    This is required to be able to read fs object variables in certain cases..
    """
    # Check if invalid
    if kyc_is_valid(attrs):
        return attrs[attr_name]

# Requires Admin to invoke
def kyc_register(sts_attrs, project_id, addresses):
    """    
    Registers all input addresses 
    Args:
        args (list):
            list a list of arguments
        
        sts (SmartTokenShare):
            Smart Token Share reference object

    Return:
        (int): The number of addresses to registered for KYC
    """
    # Gets sts object
    ok_count = 0

    if not CheckWitness(sts_attrs['owner']):
        Notify('Only the project owner can register kyc addresses') 
        return
    
    # Submits every address in the list
    for address in addresses:
        
        # Check if address is valid
        if not len(address) == 20:
            Notify('Invalid address type')
            return

        put_triple(project_id, 'KYC_address', address, True)
        OnKYCRegister(project_id, address)
        ok_count += 1

    return ok_count


def kyc_status(project_id, address):
    """
    Gets the KYC Status of an address

    Args:
        args (list):
            list a list of arguments
        
        sts (SmartTokenShare):
            Smart Token Share reference object
    Return:
        (bool): Returns the kyc status of an address
    """
    return get_triple(project_id, 'KYC_address', address)