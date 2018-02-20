"""
TheConstruct - NEO smart contract - https://github.com/nickazg/TheConstruct

Author: Nick Grobler
Email: nickazg@gmail.com
Date: Jan 17 2017
"""

VERSION = "0.0.1"

# from boa.blockchain.vm.Neo.Runtime import Log, GetTrigger, CheckWitness
# from boa.blockchain.vm.Neo.Storage import GetContext, Put
# from boa.blockchain.vm.Neo.Transaction import GetHash, GetUnspentCoins
# from boa.blockchain.vm.Neo.TriggerType import Application,Verification
# from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer
# from boa.code.builtins import concat

from boa.blockchain.vm.Neo.Runtime import GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.blockchain.vm.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetInputs, GetUnspentCoins



from construct.common.StorageManager import StorageManager
# from construct.platform.SmartTokenShare import SmartTokenShare
# from construct.platform.SmartTokenShareHandler import SmartTokenShareHandler
# from construct.platform.FundingStage import FundingStage
# from construct.platform.FundingRoadmap import FundingRoadmap

from construct.platform.SmartTokenShareNew import SmartTokenShare, sts_get_attr, sts_create, sts_get, get_total_in_circulation 
from construct.platform.FundingStageNew import FundingStage, fs_get_attr, fs_create, fs_get, fs_contribute, fs_status, fs_can_exchange, fs_add_to_circulation, fs_calculate_can_exchange, get_in_circulation, fs_claim_contributions, fs_refund, fs_get_addr_balance, fs_set_addr_balance, fs_claim_system_fee, fs_calculate_system_fee
from construct.platform.MilestoneNew import Milestone, ms_create, ms_get, ms_update_progress, ms_get_progress

from construct.platform.FundingRoadmap import FundingRoadmap
from construct.platform.KYC import KYC


from construct.tests.Tests import run_tests
from construct.common.Txio import Attachments, get_asset_attachments, get_asset_attachments_for_prev
from construct.common.Utils import claim


GAS_ASSET_ID = b'\xe7\x2d\x28\x69\x79\xee\x6c\xb1\xb7\xe6\x5d\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8e\x77\x58\xde\x42\xe4\x16\x8b\x71\x79\x2c\x60'

def Main(operation, args):
    """Entry point for the smart contract.
    Args:
        operation (str):
            UUID used as the first part of the key for Storage.Put().
        args (str):
            UUID used as the second part of the key for Storage.Put().
    Return:
        (bytearray): The result of the operation
    """        
    # Gets the transaction trigger
    trigger = GetTrigger()
    storage = StorageManager()



    if trigger == Verification:
        print('Verification')

        attachments = get_asset_attachments()
        prev_attachments = get_asset_attachments_for_prev()

        gas_requested = prev_attachments.gas_attached - attachments.gas_attached
        print(gas_requested)

        # Get amount avaliable for address
        claim_amount = storage.get_double('CLAIM', attachments.receiver_addr)

        # If the request is the EXACT amount (not less), approve the tx
        if claim_amount == gas_requested:
            print('Successfully send claim tx')
            return True     

    elif trigger == Application:
        print('Application')

        # tests = run_tests(operation, args)
        # return tests

        fr = FundingRoadmap()
        kyc = kyc()

        
        #    F U N D I N G    R O A D M A P   #

        # ARGS: project_id, [new_admins]
        if operation == 'add_project_admins':
            if len(args) == 2: 
                fr.add_project_admins(args[0], args[1])
                return True
        
                           
        
        #    S M A R T    T O K E N    S H A R E   #
        
        # ARGS: project_id, symbol, decimals, owner, total_supply
        if operation == 'create_sts':            
            if len(args) == 5:                
                sts_create(args[0], args[1], args[2], sargs[3], args[4])
                return args[0]

        # ARGS: project_id, attribute: {'project_id', 'symbol', 'decimals', 'owner', 'total_supply', 'total_in_circulation'}
        if operation == 'sts_attribute':
            if len(args) == 2:  
                sts = sts_get(args[0])
                return sts_get_attr(sts, args[1])
                

        # ARGS: project_id
        if operation == 'total_tokens_available':
            if len(args) == 1: 
                sts = sts_get(args[0])
                return sts_total_available_amount(sts)
            
        
        
        #    F U N D I N G    S T A G E   #

        # ARGS: project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas
        if operation == 'create_fs':
            if len(args) == 6: 
                fs_create(args[0], args[1], args[2], sargs[3], args[4], args[5])
                fr.add_funding_stages(args[0], [args[1]])
                return args[1]
        
        # ARGS: project_id, funding_stage_id, attribute: {'project_id', 'funding_stage_id', 'start_block', 'end_block', 'supply', 'tokens_per_gas', 'in_circulation'}
        if operation == 'fs_attribute':
            if len(args) == 3:  
                fs = fs_get(args[0], args[1])
                return fs_get_attr(fs, args[2])

        # ARGS: project_id, funding_stage_id    
        if operation == 'fs_tokens_available':
            if len(args) == 2: 
                fs = fs_get(args[0], args[1])
                return fs_available_amount(fs)
        
        # ARGS: project_id, funding_stage_id     
        if operation == 'fs_status':
            if len(args) == 2: 
                fs = fs_get(args[0], args[1])
                return fs_status(fs)       
                    


        #    M I L E S T O N E    #

        # ARGS: project_id, milestone_id, title, subtitle, extra_info_hash
        if operation == 'create_ms':
            if len(args) == 5: 
                ms_create(args[0], args[1], args[2], sargs[3], args[4])
                fr.add_milestones(args[0], mss)
                return args[1]
            
        # ARGS: project_id, milestone_id, updated_progress
        if operation == 'update_ms_progess':
            if len(args) == 3: 
                ms = ms_get(args[0], args[1])
                ms_update_progress(ms, args[2])
                return args[2]
                    


        #   C L A I M S   #

        # ARGS: project_id, funding_stage_id, refund_addr  
        if operation == 'claim_fs_refund':
            if len(args) == 3: 
                fs = fs_get(args[0], args[1])
                return fs_refund(args[2])                

        # ARGS: project_id, funding_stage_id, owner_addr
        if operation == 'claim_fs_contributions':
            if len(args) == 3: 
                fs = fs_get(args[0], args[1])
                return fs_claim_contributions(args[2])    

        # ARGS: project_id, funding_stage_id, system_owner_addr
        if operation == 'claim_fs_system_fee':
            if len(args) == 3: 
                fs = fs_get(args[0], args[1])
                return fs_claim_system_fee(args[2])

        
        
        #   K Y C   #

        # ARGS: project_id, address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash
        if operation == 'kyc_submit':
            if len(args) == 10:
                kyc.kyc_submit(args[0], args[1], args[2], sargs[3], args[4], args[5], args[6], args[7], args[8], args[9])
                return args[1]
        
        # ARGS: project_id, [addresses]
        if operation == 'kyc_register':
            if len(args) == 2:
                return kyc.kyc_register(args[0], args[1])
        
        # ARGS: project_id, address
        if operation == 'kyc_status':
            if len(args) == 2:
                return kyc.kyc_status(args[0], args[1])

        # ARGS: project_id, address
        if operation == 'get_kyc_submission':
            if len(args) == 2:
                return kyc.get_kyc_submission(args[0], args[1])






        # # TODO - Dont forget ;) 
        # # Fork contract to new version, all storage is transferred.
        # # See: https://github.com/neo-project/neo/blob/master/neo/SmartContract/StateMachine.cs#L210
        # if operation == 'contract_migrate':

        #     # Check if the invoker is the owner of this contract
        #     if CheckWitness(OWNER):
        #         print("Migrate Contract!")