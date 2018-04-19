from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Action import RegisterAction

from construct.platform.KYC import kyc_status
from construct.common.StorageManager import attrs_is_valid, serialize, deserialize, get_triple, put_triple, get_double, put_double
from construct.common.Txio import get_asset_attachments

from construct.platform.SmartTokenShare import sts_add_to_total_circulation, sts_get_attr

from boa.builtins import list

OnTransfer = RegisterAction('transfer', 'from', 'to', 'amount')
OnRefund = RegisterAction('refund', 'to', 'amount')

# Struct for storing the Funding Stage
ATTRS = {}
ATTRS['project_id'] = ''
ATTRS['funding_stage_id'] =  0
ATTRS['start_block'] = 0
ATTRS['end_block'] = 0
ATTRS['supply'] = 0
ATTRS['tokens_per_gas'] = 0
ATTRS['in_circulation'] = 0


def fs_is_valid(attrs):
    # Keys to check
    keys = [
        'project_id',
        'funding_stage_id',
        'start_block',
        'end_block',
        'supply',
        'tokens_per_gas',
        'in_circulation']
    
    is_valid = attrs_is_valid(attrs, keys)

    if not is_valid:
        Notify('Invalid Funding Stage Attrs..')

    return is_valid

def fs_create(project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas):
    """
    Creates a new Funding Stage using the input attributes, and returns
    a FundingStage object
    Args:
        project_id (str):
            ID for referencing the project

        funding_stage_id (str):
            ID for referencing the funding stage
            
        start_block (int):
            Block to start fund

        end_block (int):
            Block to end fund

        supply (int):
            Supply of the token in this fs

        tokens_per_gas (int):
            Token to gas ratio
    Return:
        (FundingStage):
            Returns a funding stage object containing these attributes
    """
    # New funding stage attrs dict
    fs = ATTRS

    # Saves vars to object
    fs['project_id'] = project_id
    fs['funding_stage_id'] = funding_stage_id
    fs['start_block'] = start_block
    fs['end_block'] = end_block
    fs['supply'] = supply
    fs['tokens_per_gas'] = tokens_per_gas
    fs['in_circulation'] = 0
    
    return fs

def fs_load_attrs(project_id, funding_stage_id):    
    # Pulling serialized attrs from storage
    serialized_attrs = get_triple('FS', project_id, funding_stage_id)
    if not serialized_attrs:
        Notify('No Attrs exist for Funding Stage')
        return

    attrs = deserialize(serialized_attrs)
    
    # Check if invalid
    if not fs_is_valid(attrs):
        return
    
    return attrs

def fs_save_attrs(attrs):
    
    # Check if invalid
    if not fs_is_valid(attrs):
        return

    # Putting serialized attrs to storage
    serialized_attrs = serialize(attrs)
    put_triple('FS', attrs['project_id'], attrs['funding_stage_id'], serialized_attrs)

def fs_get_attr(attrs, attr_name):
    """
    This is required to be able to read fs object variables in certain cases..
    """
    # Check if invalid
    if not fs_is_valid(attrs):
        return

    return attrs[attr_name]


def fs_available_amount(attrs):
    """
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

    Return:
        (int): The avaliable tokens for the Funding Stage
    """
    available = attrs['supply'] - attrs['in_circulation']
    return available

def fs_add_to_circulation(attrs, sts_attrs, amount):
    """
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

        amount (int):
            Amount of tokens added  
    """
    # storage = StorageManager()

    # Calculation
    attrs['in_circulation'] += amount
    sts_add_to_total_circulation(sts_attrs, amount)

def fs_status(attrs):
    """
    Gets the completion status of the funding stage
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes
    
    Return:
        (int):
            Id of current stage
    """
    height = GetHeight()

    # Success
    if attrs['in_circulation'] >= attrs['supply']:
        print("Funding Stage completed successfully")
        return 1

    # Active    
    if height < attrs['end_block']:
        print("Funding Stage still active")
        return 2       

    # Fail            
    print("Funding Stage failed")
    return 3

def fs_calculate_can_exchange(attrs, sts_attrs, amount):
    """
    Checks weather the input amount is avaliable to exchange
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes
        
        amount (int):
            Amounnt in question
    
    Return:
        (bool):
            Is avaliable
    """
    height = GetHeight()

    # Gets the SmartTokenShare object
    # sts = sts_get(attrs'project_id'])

    # Gets the current total in circulation
    total_in_circulation = sts_get_attr(sts_attrs, 'total_in_circulation')

    # Calculates TOTAL circulation after input amount is added
    new_total_amount = total_in_circulation + amount

    # Calculates current circulation after input amount is added
    new_fs_amount = attrs['in_circulation'] + amount

    # Get total supply from STS
    total_supply = sts_get_attr(sts_attrs, 'total_supply')
    
    if new_total_amount > total_supply:
        print("amount greater than total supply")
        return False

    if new_fs_amount > attrs['supply']:
        print("amount greater than funding stage supply")
        return False
    
    if height < attrs['start_block']:
        print("Funding stage not begun yet")
        return False
    
    if height > attrs['end_block']:
        print("Funding stage has ended")
        return False

    return True
   

def fs_can_exchange(attrs, sts_attrs, attachments):
    """
    Checks weather the input amount is allowed to exchange to the requested address
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes
        
        attachments (Attachments):
            Attachments object to inspect the transaction
    
    Return:
        (bool):
            Is allowed
    """
    # Checks attached gas
    if attachments['gas_attached'] == 0:
        print("no gas attached")
        return False

    # Checks KYC
    if not kyc_status(attrs['project_id'], attachments['sender_addr']):
        Notify("Failed KYC")
        return False
    
    # Gets the amount requested
    amount_requested = attachments['gas_attached'] * attrs['tokens_per_gas'] / 100000000
    
    # Checks weather the input amount is avaliable to exchange
    allowed = fs_calculate_can_exchange(attrs, sts_attrs, amount_requested)

    return allowed


# Invoked to mintTokens, exchange GAS for STS
def fs_contribute(attrs, sts_attrs):
    """
    Method to run in conjuction with attached gas, runs necessary checks to establish if 
    a contributon is valid
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes
    
    Return:
        (bool):
            Did contribute
    """
    # storage = StorageManager()
    attachments = get_asset_attachments()

    # this looks up whether the exchange can proceed
    allowed = fs_can_exchange(attrs, sts_attrs, attachments)

    if not allowed:
        print("Cannot exchange value, refunding")
        OnRefund(attachments['sender_addr'], attachments['gas_attached'])
        return False
    
    # lookup the current balance of the address
    current_sts_balance = fs_get_addr_balance(attrs, attachments['sender_addr'])

    # calculate the amount of tokens the attached gas will earn
    exchanged_sts = attachments['gas_attached'] * attrs['tokens_per_gas'] / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_sts + current_sts_balance
    
    # Saves updated address balance to storage
    fs_set_addr_balance(attrs, attachments['sender_addr'], new_total)

    # # update the in circulation amount
    fs_add_to_circulation(attrs, sts_attrs, exchanged_sts)

    # dispatch transfer event
    OnTransfer(attachments['receiver_addr'], attachments['sender_addr'], exchanged_sts)

    return True

# Storage Get
def fs_get_addr_balance(attrs, addr):
    balance = get_triple(attrs['project_id'], attrs['funding_stage_id'], addr)
    return balance

# Storage Put
def fs_set_addr_balance(attrs, addr, new_balance):
    put_triple(attrs['project_id'], attrs['funding_stage_id'], addr, new_balance)


def fs_calculate_system_fee(attrs):
    
    # No floats allowed 
    # fee_percent = 5 # 5%
    fee_percent = 5 # 10 ^ 8 = 0.05

    # Calculates the gas amount contributed, decimal safe 10^8
    gas_contributed = attrs['in_circulation'] / attrs['tokens_per_gas'] * 100000000
    
    # Some calculation
    fee_calculated = gas_contributed * fee_percent / 100

    return fee_calculated

# Storage Put
# If the funding stage fails, this method will return the GAS.
def fs_refund(attrs, refund_addr):
    """
    This is required to prep a refund for for a verification transaction
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

        refund_addr (bytearray):
            Address of the refund address in question
    
    Return:
        (bool):
            Can Refund
    """
    if CheckWitness(refund_addr):

        # If the funding stage failed
        if fs_status(attrs) != 1:   

            # lookup the current balance of the address
            current_sts_balance = fs_get_addr_balance(attrs, refund_addr)
            
            # Calculate gas from current_sts_balance
            gas_contribution = current_sts_balance / attrs['tokens_per_gas'] * 100000000

            # unlocks current_sts_balance to refund_addr, as 10^8
            put_double('CLAIM', refund_addr, gas_contribution)

            # sets refund_addr balance to 0
            fs_set_addr_balance(attrs, refund_addr, 0)

            return True
    
    return False

# Storage Put
# Project Owner can calim the contributions from sucessfull funding stage
def fs_claim_contributions(attrs, sts_attrs, owner_addr):
    """
    This is required to prep a claim for a verification transaction
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

        owner_addr (bytearray):
            Address of the claim deposit address
    
    Return:
        (bool):
            Can Claim
    """
    if CheckWitness(owner_addr):
        
        # If the funding stage complted sucessfully
        if fs_status(attrs) == 1:

            # Checks the owner_addr matches the sts project owner
            # sts = sts_get(fs.['project_id'])
            if sts_get_attr(sts_attrs, 'owner') == owner_addr:
            
                # Calculates the gas amount contributed, decimal safe 10^8
                gas_contributed = attrs['in_circulation'] / attrs['tokens_per_gas'] * 100000000

                # Calculating fee
                fee_calculated = fs_calculate_system_fee(attrs)

                # Deducting fees
                gas_to_claim = gas_contributed - fee_calculated
                
                # Sets the claim amount for the address, as 10^8
                put_double('CLAIM', owner_addr, gas_to_claim)
                return True
    
    return False

# Storage Put
def fs_claim_system_fee(attrs, system_owner_addr):
    if CheckWitness(system_owner_addr):

        # If the funding stage complted sucessfully
        if fs_status(attrs) == 1:  

            # Calculating fee
            fee_calculated = fs_calculate_system_fee(attrs)

            # Sets the claim amount for the address, as 10^8
            put_double('CLAIM', system_owner_addr, fee_calculated)

            return True
    
    return False