"""
TheConstruct - NEO smart contract - https://github.com/nickazg/TheConstruct

Author: Nick Grobler
Email: nickazg@gmail.com
Date: Feb 25 2017
"""

VERSION = "1.0.0"

# BOA
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, Notify
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetInputs, GetUnspentCoins
from boa.interop.Neo.Action import RegisterAction

from boa.builtins import breakpoint


# # THE CONSTRUCT - PLATFORMS
from construct.platform.SmartTokenShare import sts_create, sts_load_attrs
from construct.platform.FundingStage import fs_create, fs_load_attrs, fs_save_attrs
from construct.platform.Milestone import ms_create, ms_load_attrs, ms_save_attrs
from construct.platform.FundingRoadmap import fr_load_attrs, fr_add_project_admin, fr_update_milestone_progress
from construct.platform.KYC import kyc_create, kyc_submit, kyc_register, kyc_status, get_kyc_submission

# THE CONSTRUCT - COMMON
from construct.common.StorageManager import get_double, put_double
from construct.common.Txio import get_asset_attachments, get_asset_attachments_for_prev

OnOperationInvoke = RegisterAction('operations_invoke','op_name')

OnInvalidAttrs = RegisterAction('invalid_attrs','type','message')

GAS_ASSET_ID = b'\xe7\x2d\x28\x69\x79\xee\x6c\xb1\xb7\xe6\x5d\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8e\x77\x58\xde\x42\xe4\x16\x8b\x71\x79\x2c\x60'


def Main(operation, args):
    """Entry point for the smart contract.
    Args:
        operation (str):
            UUID used as the first part of the key for Put().
        args (str):
            UUID used as the second part of the key for Put().
    Return:
        (bytearray): The result of the operation
    """

    # Gets the transaction trigger
    trigger = GetTrigger()

    invalid_args_msg = 'INVALID ARGS'
    invaild_op_msg = 'INVALID OPERATION'
    
    if trigger == Verification():
        Notify('Verification')

        attachments = get_asset_attachments()
        prev_attachments = get_asset_attachments_for_prev()

        gas_requested = prev_attachments['gas_attached'] - attachments['gas_attached']

        # Get amount avaliable for address
        claim_amount = get_double('CLAIM', attachments['receiver_addr'])

        # If the request is the EXACT amount (not less), approve the tx
        if claim_amount == gas_requested:
            Notify('Successfully send claim tx')
            return True     

    elif trigger == Application():
        Notify('Application')

        #    F U N D I N G    R O A D M A P   #
        
        project_id = args[0]

        # LOAD
        fr_attrs = fr_load_attrs(project_id)
        sts_attrs = sts_load_attrs(project_id)

        if not fr_attrs:
            OnInvalidAttrs('fr', 'Funding Roadmap doesnt exist')

        if not sts_attrs:
            OnInvalidAttrs('sts', 'Smart Token Share doesnt exist')

        # ARGS: project_id, refund_addr
        if operation == 'check_claim_owed':
            OnOperationInvoke('check_claim_owed')
            print('execute:check_claim_owed')
            if len(args) == 2:
                refund_addr = args[1]
                return get_double('CLAIM', refund_addr)

        # ARGS: project_id, refund_addr
        elif operation == 'reset_claim_owed':
            OnOperationInvoke('reset_claim_owed')
            print('execute:reset_claim_owed')
            if len(args) == 2:
                refund_addr = args[1]
                return put_double('CLAIM', refund_addr, 0)

        # ARGS: project_id, new_admin
        elif operation == 'add_project_admins':
            OnOperationInvoke('add_project_admins')
            print('execute:add_project_admins')
            if len(args) == 2:               
                if CheckWitness(sts_attrs['owner']):
                    new_admin = args[1]
                    fr_add_project_admin(fr_attrs, new_admin)
                    fr_save_attrs(fr_attrs)
                    return True
            return invalid_args_msg

        # ARGS: project_id
        elif operation == 'get_active_index':
            OnOperationInvoke('get_active_index')
            print('execute:get_active_index')
            if len(args) == 1:
                return fr_get_attr(fr_attrs, 'active_idx')
            return invalid_args_msg
        
        # ARGS: project_id
        elif operation == 'get_funding_stages':
            OnOperationInvoke('get_funding_stages')
            print('execute:get_funding_stages')
            if len(args) == 1:
                funding_stages = fr_get_attr(fr_attrs, 'funding_stages')
                return funding_stages
            return invalid_args_msg

        # ARGS: project_id
        elif operation == 'get_active_fs':
            OnOperationInvoke('get_active_fs')
            print('execute:get_active_fs')
            if len(args) == 1:
                active_idx = fr_get_attr(fr_attrs, 'active_idx')
                funding_stages = fr_get_attr(fr_attrs, 'funding_stages')
                active_funding_stage = funding_stages[active_idx]
                return active_funding_stage
            return invalid_args_msg

        # ARGS: project_id
        elif operation == 'get_milestones':
            OnOperationInvoke('get_milestones')
            print('execute:get_milestones')
            if len(args) == 1:
                milestones = fr_get_attr(fr_attrs, 'milestones')
                return milestones
            return invalid_args_msg
        
        # ARGS: project_id
        elif operation == 'get_active_ms':
            OnOperationInvoke('get_active_ms')
            print('execute:get_active_ms')
            if len(args) == 1:
                active_idx = fr_get_attr(fr_attrs, 'active_idx')
                milestones = fr_get_attr(fr_attrs, 'milestones')
                active_milestone = milestones[active_idx]
                return active_milestone
            return invalid_args_msg

        # ARGS: project_id, updated_progress
        elif operation == 'update_active_ms_progress':
            OnOperationInvoke('update_active_ms_progress')
            print('execute:update_active_ms_progress')
            if len(args) == 2:

                if CheckWitness(sts_attrs['owner']):
                    progress = fr_update_milestone_progress(fr_attrs, args[1])
                    
                    # SAVE
                    fr_save_attrs(fr_attrs)
                    return progress
            return invalid_args_msg
        
        
        
        #    S M A R T    T O K E N    S H A R E   #
        
        # ARGS: project_id, symbol, decimals, owner, total_supply
        elif operation == 'create_sts':
            OnOperationInvoke('create_sts')
            print('execute:create_sts')            
            if len(args) == 5:
              
                symbol = args[1]
                decimals = 8 # hardcoded to 8
                owner = args[3]
                total_supply = args[4]                
                
                sts_attrs = sts_create(project_id, symbol, decimals, owner, total_supply)
                fr_set_active_index(fr_attrs, 0)
                
                # SAVE
                sts_save_attrs(sts_attrs)
                fr_save_attrs(fr_attrs)
                return project_id
            return invalid_args_msg
                
        # ARGS: project_id, attribute: {'project_id', 'symbol', 'decimals', 'owner', 'total_supply', 'total_in_circulation'}
        elif operation == 'sts_attribute':
            OnOperationInvoke('sts_attribute')
            print('execute:sts_attribute')
            if len(args) == 2:
                attr = args[1]
                 
                return sts_get_attr(sts_attrs, attr)
            return invalid_args_msg

        # ARGS: project_id
        elif operation == 'total_tokens_available':
            OnOperationInvoke('total_tokens_available')
            print('execute:total_tokens_available')
            if len(args) == 1:

                return sts_total_available_amount(sts_attrs)
            return invalid_args_msg
            
        
        
        #    F U N D I N G    S T A G E   #
        
        funding_stage_id = args[1]
        fs_attrs = fs_load_attrs(project_id, funding_stage_id)

        if not fs_attrs:
            OnInvalidAttrs('fs', 'Funding Stage doesnt exist')

        # ARGS: project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas
        if operation == 'create_fs':
            OnOperationInvoke('create_fs')
            print('execute:create_fs')
            if len(args) == 6:

                if CheckWitness(sts_attrs['owner']):
                    start_block = args[2]
                    end_block = args[3]
                    supply = args[4]
                    tokens_per_gas = args[5]

                    fs_attrs = fs_create(project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas)
                    fr_add_funding_stage(fr_attrs, funding_stage_id)
                    
                    # SAVE
                    fs_save_attrs(fs_attrs)
                    fr_save_attrs(fr_attrs)
                    
                    return funding_stage_id
            return invalid_args_msg
        
        # ARGS: project_id, funding_stage_id, attribute: {'project_id', 'funding_stage_id', 'start_block', 'end_block', 'supply', 'tokens_per_gas', 'in_circulation'}
        if operation == 'fs_attribute':
            OnOperationInvoke('fs_attribute')
            print('execute:fs_attribute')
            if len(args) == 3:
                attr = args[2] 

                return fs_get_attr(fs_attrs, attr)

        # ARGS: project_id, funding_stage_id    
        if operation == 'fs_tokens_available':
            OnOperationInvoke('fs_tokens_available')
            print('execute:fs_tokens_available')
            if len(args) == 2: 

                return fs_available_amount(fs_attrs)
            return invalid_args_msg
        
        # ARGS: project_id, funding_stage_id     
        if operation == 'fs_status':
            OnOperationInvoke('fs_status')
            print('execute:fs_status')
            if len(args) == 2:

                return fs_status(fs_attrs)     
            return invalid_args_msg  
        
        # ARGS: project_id, funding_stage_id     
        if operation == 'fs_contribute':
            OnOperationInvoke('fs_contribute')
            print('execute:fs_contribute')
            if len(args) == 2:

                fs_contribute(fs_attrs, sts_attrs)

                # SAVE
                fs_save_attrs(fs_attrs)
                sts_save_attrs(sts_attrs)
                return True

            return invalid_args_msg  

        # ARGS: project_id, funding_stage_id, addr    
        if operation == 'fs_addr_balance':
            OnOperationInvoke('fs_addr_balance')
            print('execute:fs_addr_balance')
            if len(args) == 2:
                addr = args[2]
                return fs_get_addr_balance(fs_attrs, addr)
            return invalid_args_msg   


        #     M I L E S T O N E    #

        milestone_id = args[1]
        ms_attrs = ms_load_attrs(project_id, milestone_id)

        if not ms_attrs:
            OnInvalidAttrs('ms', 'Milestone doesnt exist')

        # ARGS: project_id, milestone_id, title, subtitle, extra_info_hash
        if operation == 'create_ms':
            OnOperationInvoke('create_ms')
            print('execute:create_ms')
            if len(args) == 5:
                if CheckWitness(sts_attrs['owner']):
                    title = args[2]
                    subtitle = args[3] 
                    extra_info_hash = args[4]

                    ms_attrs = ms_create(project_id, milestone_id, title, subtitle, extra_info_hash)
                    fr_add_milestone(fr_attrs, milestone_id)

                    # SAVE
                    ms_save_attrs(ms_attrs)
                    fr_save_attrs(fr_attrs)
                    return milestone_id
            return invalid_args_msg        

        # ARGS: project_id, milestone_id, attribute: {'project_id', 'milestone_id', 'title', 'subtitle', 'extra_info_hash', 'progress'}
        if operation == 'ms_attribute':
            OnOperationInvoke('ms_attribute')
            print('execute:ms_attribute')
            if len(args) == 3:
                attr = args[2] 

                return ms_get_attr(ms_attrs, attr)

        # ARGS: project_id, milestone_id
        if operation == 'get_ms_progess':
            OnOperationInvoke('get_ms_progess')
            print('execute:get_ms_progess')
            if len(args) == 2:

                return ms_get_attr(ms_attrs, 'progress')
            return invalid_args_msg                    


        #    C L A I M S   #             

        funding_stage_id = args[1] 
    
        # ARGS: project_id, funding_stage_id, refund_addr  
        if operation == 'claim_fs_refund':
            OnOperationInvoke('claim_fs_refund')
            print('execute:claim_fs_refund')
            if len(args) == 3:
                refund_addr = args[2] 

                fs_refund(fs_attrs, refund_addr)
                fs_save_attrs(fs_attrs)
                return True

            return invalid_args_msg                

        # ARGS: project_id, funding_stage_id, owner_addr
        if operation == 'claim_fs_contributions':
            OnOperationInvoke('claim_fs_contributions')
            print('execute:claim_fs_contributions')
            if len(args) == 3:
                owner_addr = args[2]

                fs_claim_contributions(fs_attrs, owner_addr)
                fs_save_attrs(fs_attrs)
                return True
            return invalid_args_msg 

        # ARGS: project_id, funding_stage_id, system_owner_addr
        if operation == 'claim_fs_system_fee':
            OnOperationInvoke('claim_fs_system_fee')
            print('execute:claim_fs_system_fee')
            if len(args) == 3: 
                system_owner_addr = args[2]

                fs_claim_system_fee(fs_attrs, system_owner_addr)
                fs_save_attrs(fs_attrs)
                return True
            return invalid_args_msg

        
        
        #   K Y C   #
        kyc_attrs = sts_load_attrs(project_id)

        if not kyc_attrs:
            OnInvalidAttrs('kyc', 'KYC submission doesnt exist')

        # ARGS: project_id, address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash
        if operation == 'kyc_submit':
            OnOperationInvoke('kyc_submit')
            print('execute:kyc_submit')
            if len(args) == 10:
                address = args[1]
                phys_address = args[2]
                first_name = args[3]
                last_name = args[4]
                id_type = args[5]
                id_number = args[6]
                id_expiry = args[7]
                file_location = args[8]
                file_hash = args[9]

                kyc_attrs = kyc_create(project_id, address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash)
                kyc_submit(kyc_attrs)
                
                return address

            return invalid_args_msg
        
        # ARGS: project_id, addresses -> 
        if operation == 'kyc_register':
            if CheckWitness(sts_attrs['owner']):
                OnOperationInvoke('kyc_register')
                print('execute:kyc_register')
                if len(args) > 1:
                    return kyc_register(sts_attrs, project_id, args)
            return invalid_args_msg
        
        # ARGS: project_id, address
        if operation == 'kyc_status':
            OnOperationInvoke('kyc_status')
            print('execute:kyc_status')
            if len(args) == 2:
                address = args[1]

                return kyc_status(project_id, address)
            return invalid_args_msg

        # ARGS: project_id, address
        if operation == 'get_kyc_submission':
            OnOperationInvoke('get_kyc_submission')
            print('execute:get_kyc_submission')
            if len(args) == 2:
                address = args[1]

                return kyc_load_attrs(sts_attrs, address)
            return invalid_args_msg        
        
        return invaild_op_msg
