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
from construct.platform.SmartTokenShare import SmartTokenShare
from construct.platform.SmartTokenShareHandler import SmartTokenShareHandler
from construct.platform.FundingStage import FundingStage
from construct.platform.FundingRoadmap import FundingRoadmap

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

        print('gas_requested')
        print(gas_requested)

        # Get amount avaliable for address
        claim_amount = storage.get_double('CLAIM', attachments.receiver_addr)

        # If the request is the EXACT amount (not less), approve the tx
        if claim_amount == gas_requested:
            print('Successfully send claim tx')
            return True     

    elif trigger == Application:

        print('Application')
        # return False

        tests = run_tests(operation, args)

        return tests









        # # TODO - FEE ;) 

        # # TODO - Dont forget ;) 
        # # Fork contract to new version, all storage is transferred.
        # # See: https://github.com/neo-project/neo/blob/master/neo/SmartContract/StateMachine.cs#L210
        # if operation == 'contract_migrate':

        #     # Check if the invoker is the owner of this contract
        #     if CheckWitness(OWNER):
        #         print("Migrate Contract!")