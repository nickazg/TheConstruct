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

from construct.common.StorageManager import StorageManager
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.platform.SmartTokenShareHandler import SmartTokenShareHandler
from construct.platform.FundingStage import FundingStage
from construct.platform.FundingRoadmap import FundingRoadmap


OWNER = b''
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
    fs = FundingStage()

    if trigger == Verification:
        return True

    elif trigger == Application:
        if operation != None and len(args) > 0:
            
            sts = SmartTokenShare()
            sts_handler = SmartTokenShareHandler()

            # project_id always first arg
            project_id = args[0]

            # fs.start_new_crowdfund(project_id, sts)
            
            # Pulling info from storeage
            sts.get_project_info(project_id)        

            for handler_op in sts_handler.get_methods():
                if operation == handler_op:
                    return sts_handler.handle_sts(operation, args, sts)

            # TEST
            if operation == 'create':
                symbol = args[2]
                owner = args[1]
                sts.deploy_new_sts(project_id, owner, symbol)

            if operation == 'test':
                print('###TEST')
                storage = StorageManager()
                # test_list = list('fs1', 'fs2', 'fs3')
                test_list = ["sdad","adsa","asda"]
                
                # test_list_len = len(test_list)
                # print(test_list_len)
                
                test_serialize = storage.serialize_array(test_list)
                print(test_serialize)
                
                # test_deserialize = storage.deserialize_bytearray(test_serialize)
                # test_deserialize_len = len(test_deserialize)
                # print(test_deserialize_len)
                print('TEST###')


            
            if operation == 'fr_make':
                funding_roadmap = FundingRoadmap()
                funding_roadmap.set_project_id(project_id)

                funding_stage = FundingStage()
                funding_stage.create(project_id, 'fs1', 1000, 50, 100000, 20)
                funding_stage.create(project_id, 'fs2', 2000, 50, 100000, 20)
                funding_stage.create(project_id, 'fs3', 3000, 50, 100000, 20)

                funding_stages = ['fs1', 'fs2', 'fs3']
                funding_roadmap.add_funding_stages(funding_stages)

            # if operation == 'fr_get':
                funding_roadmap = FundingRoadmap()
                funding_roadmap.set_project_id(project_id)
                funding_stages = funding_roadmap.get_funding_stages()
                
                print("#funding_stages")

                for fs_id in funding_stages:
                    print('###')
                    print(fs_id)
                    funding_stage = FundingStage()
                    funding_stage.read_from_storage(project_id, fs_id)                    
                    # print(funding_stage.funding_stage_id)
                    # print(funding_stage.sts_supply)
                    print('######')

            # # TEST
            # if operation == 'start_new_crowdfund':  
            #     sts.start_new_crowdfund("MyProjID", 1, 100000, 1000, 100)

        
            # print("## DEBUG")
            # print(sts.symbol)
            # print(sts.current_tokens_per_gas)
            # print(sts.project_id)
            # print(sts.total_supply)
            # print("DEBUG ## ")

            return True
            
            # TODO - Dont forget ;) 
            # Fork contract to new version, all storage is transferred.
            # See: https://github.com/neo-project/neo/blob/master/neo/SmartContract/StateMachine.cs#L210
            if operation == 'contract_migrate':

                # Check if the invoker is the owner of this contract
                if CheckWitness(OWNER):
                    print("Migrate Contract!")
