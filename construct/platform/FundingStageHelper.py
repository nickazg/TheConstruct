from construct.common.StorageManager import StorageManager
from construct.platform.SmartTokenShare import SmartTokenShare

def add_to_circulation(project_id:str, funding_stage_id:str, amount:int, storage:StorageManager, fs_info:list):
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

    # info into vars
    print('info into vars')
    start_block = fs_info[0]
    end_block = fs_info[1]
    supply = fs_info[2]
    tokens_per_gas = fs_info[3]
    in_circulation = fs_info[4]

    # Calculation
    print('Calculation')
    updated_in_circulation = in_circulation + amount

    # output STS info
    print('output STS info')
    updated_fs_info = [start_block, end_block, supply, tokens_per_gas, updated_in_circulation]
    
    # updated_fs_info = list(length=5)
    # updated_fs_info[0] = start_block
    # updated_fs_info[1] = end_block
    # updated_fs_info[2] = supply
    # updated_fs_info[3] = tokens_per_gas
    # updated_fs_info[4] = updated_in_circulation


    # Save STS info
    # print(updated_in_circulation)
    print('Save STS info')
    print(in_circulation)
    
    updated_fs_info_serialized = storage.serialize_array(updated_fs_info)
    storage.put_triple('FS', project_id, funding_stage_id, updated_fs_info_serialized)
    
    # Update sts **
    sts = SmartTokenShare()
    sts.add_to_total_circulation(project_id, amount)

    return True