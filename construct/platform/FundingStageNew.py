from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Blockchain import GetHeight
from boa.blockchain.vm.Neo.Action import RegisterAction

from construct.platform.KYC import KYC
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.platform.FundingStageHelper import add_to_circulation
from construct.common.StorageManager import StorageManager
from construct.common.Txio import Attachments, get_asset_attachments

from construct.platform.SmartTokenShareNew import SmartTokenShare, sts_get 


from boa.code.builtins import list

OnTransfer = RegisterAction('transfer', 'from', 'to', 'amount')
OnRefund = RegisterAction('refund', 'to', 'amount')

class FundingStage():
    """
    Interface for managing Funding Stages
    """
    project_id = ''
    funding_stage_id = ''
    start_block = 0
    end_block = 0
    supply = 0
    tokens_per_gas = 0
    in_circulation = 0


def fs_create(project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas) -> FundingStage:
    """
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
        (None): 
    """
    storage = StorageManager()
    fs =  FundingStage()
    
    fs.project_id = project_id
    fs.funding_stage_id = funding_stage_id
    fs.start_block = start_block
    fs.end_block = end_block
    fs.supply = supply
    fs.tokens_per_gas = tokens_per_gas
    
    # Default circulation
    fs.in_circulation = 0
    
    # Info structure
    fs_info = [start_block, end_block, supply, tokens_per_gas, fs.in_circulation]

    # Saving info to storage
    fs_info_serialized = storage.serialize_array(fs_info)
    storage.put_triple('FS', project_id, funding_stage_id, fs_info_serialized)

    return fs 

def fs_get(project_id:str, funding_stage_id:str) -> FundingStage:
    storage = StorageManager()
    fs = FundingStage()
    
    # Pull FundingStage info
    fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)

    if not fs_info_serialized:
        print('fs_info_serialized is null')            
        return None
    
    fs_info = storage.deserialize_bytearray(fs_info_serialized)

    # info into vars
    fs.start_block = fs_info[0]
    fs.end_block = fs_info[1]
    fs.supply = fs_info[2]
    fs.tokens_per_gas = fs_info[3]
    fs.in_circulation = fs_info[4]
    
    return fs

def fs_available_amount(fs:FundingStage) -> int:
    """
    Args:
        project_id (str):
            ID for referencing the project

        funding_stage_id (str):
            ID for referencing the funding stage
    Return:
        (int): The avaliable tokens for the current sale
    """
    # storage = StorageManager()
    
    # # Pull FundingStage info
    # fs_info = self.get_info(project_id, funding_stage_id)

    # # FundingStage vars
    # in_circulation = fs_info[4]
    # supply = fs_info[2]

    available = fs.supply - fs.in_circulation

    return available

def fs_get_circulation(fs:FundingStage) -> int:
    """
    Get the total amount of tokens in circulation

    Args:
        project_id (str):
            ID for referencing the project

        funding_stage_id (str):
            ID for referencing the funding stage
    Return:
        (int): The total amount of tokens in circulation
    # """        
    # storage = StorageManager()
    
    # # Pull FundingStage info
    # fs_info_serialized = storage.get_triple('FS', project_id, funding_stage_id)
    # fs_info = storage.deserialize_bytearray(fs_info_serialized)

    # # in_circulation var
    # in_circulation = fs_info[4]

    return fs.in_circulation

def fs_add_to_circulation(fs:FundingStage, amount:int) -> bool:
    """
    Adds an amount of token to circlulation

    Args:
        project_id (str):
            ID for referencing the project

        funding_stage_id (str):
            ID for referencing the funding stage

        amount (int):
            amount of tokens added  
    """
    # storage = StorageManager()

    # Pull FundingStage info
    # fs_info = self.get_info(project_id, funding_stage_id)

    # # info into vars
    # print('info into vars')
    # start_block = fs_info[0]
    # end_block = fs_info[1]
    # supply = fs_info[2]
    # tokens_per_gas = fs_info[3]
    # in_circulation = fs_info[4]

    # Calculation
    print('Calculation')
    fs.in_circulation = fs.in_circulation + amount

    # output STS info
    print('output STS info')
    updated_fs_info = [fs.start_block, fs.end_block, fs.supply, fs.tokens_per_gas, fs.in_circulation]
    
    # updated_fs_info = list(length=5)
    # updated_fs_info[0] = start_block
    # updated_fs_info[1] = end_block
    # updated_fs_info[2] = supply
    # updated_fs_info[3] = tokens_per_gas
    # updated_fs_info[4] = updated_in_circulation


    # Save STS info
    # print(updated_in_circulation)
    # print('Save STS info')
    # print(fs.in_circulation)
    
    updated_fs_info_serialized = storage.serialize_array(updated_fs_info)
    storage.put_triple('FS', fs.project_id, fs.funding_stage_id, updated_fs_info_serialized)
    
    # Update sts **
    sts = sts_get(fs.project_id)
    sts_add_to_total_circulation(sts, amount)

    return True


def fs_status(fs:FundingStage) -> int:
    # fs_info = self.get_info(project_id, funding_stage_id)
    
    # # info into vars
    # start_block = fs_info[0]
    # end_block = fs_info[1]
    # supply = fs_info[2]
    # tokens_per_gas = fs_info[3]
    # in_circulation = fs_info[4]

    height = GetHeight()

    # print('supply')
    # print(supply)

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
    

# Invoked to mintTokens, exchange GAS for STS
def fs_contribute(fs:FundingStage) -> bool:
    
    storage = StorageManager()
    attachments = get_asset_attachments()

    # fs_info = self.get_info(project_id, funding_stage_id)
    # if not fs_info:
    #     print('invalid fs_info')
    #     return False
    
    # tokens_per_gas = fs_info[self.tokens_per_gas_idx]

    # this looks up whether the exchange can proceed
    can_exchange = can_exchange(fs, attachments)

    if not can_exchange:
        print("Cannot exchange value, refunding")
        # OnRefund(attachments.sender_addr, attachments.neo_attached)
        return False
    
    # lookup the current balance of the address
    current_sts_balance = storage.get_double(fs.project_id, attachments.sender_addr)

    # calculate the amount of tokens the attached gas will earn
    exchanged_sts = attachments.gas_attached * fs.tokens_per_gas / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_sts + current_sts_balance
    
    storage.put_double(fs.project_id, attachments.sender_addr, new_total)

    # NEED TO FIX THIS!! 
    # # update the in circulation amount
    fs_add_to_circulation(fs, exchanged_sts)
    print('added to circ')

    # dispatch transfer event
    OnTransfer(attachments.receiver_addr, attachments.sender_addr, exchanged_sts)

    return True

def fs_can_exchange(fs:FundingStage, attachments:Attachments) -> bool:
    
    # fs_info = self.get_info(project_id, funding_stage_id)
    # tokens_per_gas = fs_info[self.tokens_per_gas_idx]

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
    
    can_exchange = calculate_can_exchange(fs, amount_requested)

    return can_exchange

def fs_calculate_can_exchange(fs:FundingStage, amount:int):
    # storage = StorageManager()
    height = GetHeight()

    sts = sts_get(fs.project_id)
    
    total_in_circulation = sts_get_total_circulation(sts)
    fs_in_circulation = fs_get_circulation(fs)

    new_total_amount = total_in_circulation + amount
    new_fs_amount = fs_in_circulation + amount

    # sts = SmartTokenShare()
    # sts_info = sts.get_info(project_id)

    # total_supply = sts_info[sts.total_supply_idx]

    # fs_info = self.get_info(project_id, funding_stage_id)
    # fs_supply = fs_info[self.supply_idx]
    # fs_start_block = fs_info[self.start_block_idx]
    # fs_end_block = fs_info[self.end_block_idx]

    if new_total_amount > sts.total_supply:
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

    