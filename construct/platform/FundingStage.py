from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Blockchain import GetHeight
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.KYC import KYC
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments

from construct.platform.SmartTokenShare import SmartTokenShare, sts_get, sts_get_attr, sts_add_to_total_circulation, get_total_in_circulation 

from boa.code.builtins import list

OnTransfer = RegisterAction('transfer', 'from', 'to', 'amount')
OnRefund = RegisterAction('refund', 'to', 'amount')

class FundingStage():
    """
    Object for managing Funding Stages
    """
    project_id = ''
    funding_stage_id = ''
    start_block = 0
    end_block = 0
    supply = 0
    tokens_per_gas = 0
    in_circulation = 0

def get_in_circulation(fs:FundingStage) -> int:
    """
    This is required specifically for this variable
    """
    return fs.in_circulation

def fs_get_attr(fs:FundingStage, attr_name):
    """
    This is required to be able to read fs object variables in certain cases..
    """

    if attr_name == 'project_id':
        return fs.project_id

    if attr_name == 'funding_stage_id':
        return fs.funding_stage_id

    if attr_name == 'start_block':
        return fs.start_block
    
    if attr_name == 'end_block':
        return fs.end_block
    
    if attr_name == 'supply':
        return fs.supply

    if attr_name == 'tokens_per_gas':
        return fs.tokens_per_gas

    if attr_name == 'in_circulation':
        return fs.in_circulation


def fs_create(project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas) -> FundingStage:
    """
    Creates a new Funding Stage using the input attributes, saves it to storage and returns
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
    # init objects
    storage = StorageManager()
    fs =  FundingStage()
    
    # Saves vars to object
    fs.project_id = project_id
    fs.funding_stage_id = funding_stage_id
    fs.start_block = start_block
    fs.end_block = end_block
    fs.supply = supply
    fs.tokens_per_gas = tokens_per_gas
    fs.in_circulation = 0
    
    # Info structure
    fs_info = [start_block, end_block, supply, tokens_per_gas, 0]

    # Saving info to storage
    fs_info_serialized = storage.serialize_array(fs_info)
    storage.put_triple('FS', project_id, funding_stage_id, fs_info_serialized)

    return fs


def fs_get(project_id, funding_stage_id) -> FundingStage:
    """
    Pulls an existing Funding Stage from storage using the input attributes, and returns
    a FundingStage object
    Args:
        project_id (str):
            ID for referencing the project

        funding_stage_id (str):
            ID for referencing the funding stage
            
    Return:
        (FundingStage):
            Returns a funding stage object containing attributes
    """
    storage = StorageManager()
    fs = FundingStage()
    
    # Pull FundingStage info
    fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)

    if not fs_info_serialized:
        print('fs_info_serialized is null')            
        return None
    
    fs_info = storage.deserialize_bytearray(fs_info_serialized)

    # Saves vars to object
    fs.project_id = project_id
    fs.funding_stage_id = funding_stage_id
    fs.start_block = fs_info[0]
    fs.end_block = fs_info[1]
    fs.supply = fs_info[2]
    fs.tokens_per_gas = fs_info[3]
    fs.in_circulation = fs_info[4]
    
    return fs

def fs_available_amount(fs:FundingStage) -> int:
    """
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

    Return:
        (int): The avaliable tokens for the Funding Stage
    """

    available = fs.supply - fs.in_circulation

    return available

def fs_get_circulation(fs:FundingStage) -> int:
    """
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

    Return:
        (int): The amount of tokens in the Funding Stage
    """    
    return fs.in_circulation

def fs_add_to_circulation(fs:FundingStage, amount:int) -> bool:
    """
    Args:
        fs (FundingStage):
            Funding Stage object containing specific attributes

        amount (int):
            Amount of tokens added  
    """
    storage = StorageManager()

    # Calculation
    fs.in_circulation = fs.in_circulation + amount

    # Output STS info
    updated_fs_info = [fs.start_block, fs.end_block, fs.supply, fs.tokens_per_gas, fs.in_circulation]
    
    # Serialize array and save to storage
    updated_fs_info_serialized = storage.serialize_array(updated_fs_info)
    storage.put_triple('FS', fs.project_id, fs.funding_stage_id, updated_fs_info_serialized)
    
    # Update sts **
    sts = sts_get(fs.project_id)
    sts_add_to_total_circulation(sts, amount)

    return True


def fs_status(fs:FundingStage) -> int:
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
    if fs.in_circulation >= fs.supply:
        print("Funding Stage completed successfully")
        return 1

    # Active    
    if height < fs.end_block:
        print("Funding Stage still active")
        return 2       

    # Fail            
    print("Funding Stage failed")
    return 3

def fs_calculate_can_exchange(fs:FundingStage, amount:int):
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
    sts = sts_get(fs.project_id)

    # Gets the current total in circulation
    total_in_circulation = get_total_in_circulation(sts)

    # Calculates TOTAL circulation after input amount is added
    new_total_amount = total_in_circulation + amount

    # Calculates current circulation after input amount is added
    new_fs_amount = fs.in_circulation + amount

    total_supply = sts_get_attr(sts, 'total_supply')
    if new_total_amount > total_supply:
        print("amount greater than total supply")
        return False

    if new_fs_amount > fs.supply:
        print("amount greater than funding stage supply")
        return False
    
    if height < fs.start_block:
        print("Funding stage not begun yet")
        return False
    
    if height > fs.end_block:
        print("Funding stage has ended")
        return False

    return True
   

def fs_can_exchange(fs:FundingStage, attachments:Attachments) -> bool:
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
    if attachments.gas_attached == 0:
        print("no gas attached")
        return False

    # Checks KYC
    kyc = KYC()
    if not kyc.kyc_status(fs.project_id, attachments.sender_addr):
        print("Failed KYC")
        return False
    
    # Gets the amount requested
    amount_requested = attachments.gas_attached * fs.tokens_per_gas / 100000000
    
    # Checks weather the input amount is avaliable to exchange
    allowed = fs_calculate_can_exchange(fs, amount_requested)

    return allowed


# Invoked to mintTokens, exchange GAS for STS
def fs_contribute(fs:FundingStage) -> bool:
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
    storage = StorageManager()
    attachments = get_asset_attachments()

    # this looks up whether the exchange can proceed
    allowed = fs_can_exchange(fs, attachments)

    if not allowed:
        print("Cannot exchange value, refunding")
        OnRefund(attachments.sender_addr, attachments.gas_attached)
        return False
    
    # lookup the current balance of the address
    current_sts_balance = fs_get_addr_balance(fs, attachments.sender_addr)

    # calculate the amount of tokens the attached gas will earn
    exchanged_sts = attachments.gas_attached * fs.tokens_per_gas / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_sts + current_sts_balance
    
    # Saves updated address balance to storage
    fs_set_addr_balance(fs, attachments.sender_addr, new_total)

    # # update the in circulation amount
    fs_add_to_circulation(fs, exchanged_sts)

    # dispatch transfer event
    OnTransfer(attachments.receiver_addr, attachments.sender_addr, exchanged_sts)

    return True

def fs_get_addr_balance(fs:FundingStage, addr):
    storage = StorageManager()
    balance = storage.get_triple(fs.project_id, fs.funding_stage_id, addr)
    print('balance')
    return balance

def fs_set_addr_balance(fs:FundingStage, addr, new_balance):
    storage = StorageManager()
    storage.put_triple(fs.project_id, fs.funding_stage_id, addr, new_balance)


def fs_calculate_system_fee(fs:FundingStage):
    
    # No floats allowed 
    # fee_percent = 5 # 5%
    fee_percent = 5 # 10 ^ 8 = 0.05

    # Calculates the gas amount contributed, decimal safe 10^8
    gas_contributed = fs.in_circulation / fs.tokens_per_gas * 100000000
    
    # Some calculation
    fee_calculated = gas_contributed * fee_percent / 100

    return fee_calculated


# If the funding stage fails, this method will return the GAS.
def fs_refund(fs:FundingStage, refund_addr):
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
    storage = StorageManager()

    if CheckWitness(refund_addr):

        # If the funding stage completed sucessfully
        if fs_status(fs) != 1:   

            # lookup the current balance of the address
            current_sts_balance = fs_get_addr_balance(fs, refund_addr)
            
            # Calculate gas from current_sts_balance
            gas_contribution = current_sts_balance / fs.tokens_per_gas * 100000000

            # unlocks current_sts_balance to refund_addr, as 10^8
            storage.put_double('CLAIM', refund_addr, gas_contribution)

            # sets refund_addr balance to 0
            fs_set_addr_balance(fs, refund_addr, 0)

            return True
    
    return False

# Project Owner can calim the contributions from sucessfull funding stage
def fs_claim_contributions(fs:FundingStage, owner_addr):
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
    storage = StorageManager()
    if CheckWitness(owner_addr):
        
        # If the funding stage complted sucessfully
        if fs_status(fs) == 1:

            # Checks the owner_addr matches the sts project owner
            sts = sts_get(fs.project_id)
            if sts_get_attr(sts, 'owner') == owner_addr:
            
                # Calculates the gas amount contributed, decimal safe 10^8
                gas_contributed = fs.in_circulation / fs.tokens_per_gas * 100000000

                # Calculating fee
                fee_calculated = fs_calculate_system_fee(fs)

                # Deducting fees
                gas_to_claim = gas_contributed - fee_calculated
                
                # Sets the claim amount for the address, as 10^8
                storage.put_double('CLAIM', owner_addr, gas_to_claim)
                return True
    
    return False


def fs_claim_system_fee(fs:FundingStage, system_owner_addr):
    storage = StorageManager()

    if CheckWitness(system_owner_addr):

        # If the funding stage complted sucessfully
        if fs_status(fs) == 1:  

            # Calculating fee
            fee_calculated = fs_calculate_system_fee(fs)

            # Sets the claim amount for the address, as 10^8
            storage.put_double('CLAIM', system_owner_addr, fee_calculated)

            return True
    
    return False