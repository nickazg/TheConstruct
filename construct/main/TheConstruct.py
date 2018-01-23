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

from construct.platform.SmartTokenShare import SmartTokenShare


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
        (int): status code representing if execution was a success.
    """    
    
    sts = SmartTokenShare()

    # Gets the transaction trigger
    trigger = GetTrigger()
    
    
    if trigger == Verification:
        return True

    elif trigger == Application:
        print("operation: ", operation)
        
        if operation == 'create':
            sts.deploy_new_project_sts("MyProjID", sts.owner, 'FST')
        
        if operation == 'start_new_crowdfund':  
            sts.start_new_crowdfund("MyProjID", 1, 100000, 1000, 100)
        
        if operation == 'check':  
            sts.get_project("MyProjID")
    
        print("## DEBUG")
        print(sts.symbol)
        print(sts.current_tokens_per_gas)
        print(sts.project_id)
        print(sts.total_supply)
        print("DEBUG ## ")

        return True
        
