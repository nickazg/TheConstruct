"""
Minimal NEO node with custom code in a background thread.
It will log events from all smart contracts on the blockchain
as they are seen in the received blocks.
"""
import threading
import argparse
import datetime
import json
import os
import psutil
import traceback
import logging
import sys

from time import sleep

from pymitter import EventEmitter

from logzero import logger
from twisted.internet import reactor, task

from neo.Network.NodeLeader import NodeLeader
from neo.Core.Blockchain import Blockchain
from neo.VM.ScriptBuilder import ScriptBuilder
from neo.Blockchain import GetBlockchain
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Settings import settings

from neo import __version__
from neo.Core.Blockchain import Blockchain
from neocore.Fixed8 import Fixed8
from neo.IO.MemoryStream import StreamManager
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Implementations.Blockchains.LevelDB.DebugStorage import DebugStorage
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Implementations.Notifications.LevelDB.NotificationDB import NotificationDB
from neo.Network.NodeLeader import NodeLeader
from neo.Prompt.Commands.BuildNRun import BuildAndRun, LoadAndRun
from neo.Prompt.Commands.Invoke import InvokeContract, TestInvokeContract, test_invoke
from neo.Prompt.Commands.LoadSmartContract import LoadContract, GatherContractDetails, ImportContractAddr, \
    ImportMultiSigContractAddr
from neo.Prompt.Commands.Send import construct_and_send, parse_and_sign
from neo.contrib.nex.withdraw import RequestWithdrawFrom, PrintHolds, DeleteHolds, WithdrawOne, WithdrawAll, \
    CancelWithdrawalHolds, ShowCompletedHolds, CleanupCompletedHolds
from neo.Prompt.Commands.Tokens import token_approve_allowance, token_get_allowance, token_send, token_send_from, \
    token_mint, token_crowdsale_register
from neo.Prompt.Commands.Wallet import DeleteAddress, ImportWatchAddr, ImportToken, ClaimGas, DeleteToken, AddAlias, \
    ShowUnspentCoins
from neo.Prompt.Utils import get_arg
from neo.Prompt.InputParser import InputParser
from neo.Settings import settings, DIR_PROJECT_ROOT
from neo.UserPreferences import preferences
from neocore.KeyPair import KeyPair
from neocore.UInt256 import UInt256
from neocore.UInt160 import UInt160
from neocore.BigInteger import BigInteger

from neo.EventHub import events, SmartContractEvent

from neocore.Cryptography.Crypto import Crypto


# If you want the log messages to also be saved in a logfile, enable the
# next line. This configures a logfile with max 10 MB and 3 rotations:
# settings.set_logfile("/tmp/logfile.log", max_bytes=1e7, backup_count=3)

# Creates an object from a dict (one layer)
class Struct(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

fr_config = {
    'project': {
        'id':                   'TheConstruct2',
        'symbol':               'STR',
        'owner':                bytearray(b'#\xba\'\x03\xc52c\xe8\xd6\xe5\"\xdc2 39\xdc\xd8\xee\xe9'),
        'total_supply':         1000000,
    },
    'funding_stages': [
        {
            'id':               'first_stage',
            'start_block':      10000,
            'end_block':        13000,
            'supply':           100000,
            'tokens_per_gas':   1000, # = 100 GAS
        },
        {
            'id':               'second_stage',
            'start_block':      12000,
            'end_block':        13000,
            'supply':           250000,
            'tokens_per_gas':   500, # = 500 GAS
        },
        # {
        #     'id':               'third_stage',
        #     'start_block':      13000,
        #     'end_block':        13100,
        #     'supply':           250000,
        #     'tokens_per_gas':   250, # = 1000 GAS
        # },
        # {
        #     'id':               'fourth_stage',
        #     'start_block':      14000,
        #     'end_block':        14100,
        #     'supply':           300000,
        #     'tokens_per_gas':   100, # = 3000 GAS
        # }
    ],
    'milestones': [
        {
            'id':               'first_milestone',
            'title':            'Proof of Work',
            'subtitle':         'Complete a proof of work model',
            'extra_info_hash':  'o3ufh249uj308ohw0fjp2409fj90jwijifsfjpw09jowfg0swp',
        },
        {
            'id':               'second_milestone',
            'title':            'Deploy SC',
            'subtitle':         'Deploy SC to Mainnet',
            'extra_info_hash':  'rsfufasdadsaasdasd23f2fqf2ff23f23fg23f23f32f2f3f32',
        },
        # {
        #     'id':               'third_milestone',
        #     'title':            'Create Website',
        #     'subtitle':         'Create Frontend Client',
        #     'extra_info_hash':  '2308fj239fn3o2ihfj90kwdlpesfk3w9fpejpiesjfsfjsdpfj',
        # },
        # {
        #     'id':               'fourth_milestone',
        #     'title':            'Marketing and Team',
        #     'subtitle':         'Expand team, and start marketing',
        #     'extra_info_hash':  'f209join3895hoj9qdkou4if4wjffoiw3jfoinf0iwja9sgh5h',
        # },
    ]
}


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[34m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# scripthash = 0f530bad60e7ea752fcd8630ead0635a15c5c32f
# operation = 'create_sts'
# args = ["testone", "first_stage", 1, 999999, 1000, 100]

def MultiTestInvokeContract(wallet, scripthash, operation, args, withdrawal_tx=None, parse_params=True, from_addr=None):
    BC = GetBlockchain()

    contract = BC.GetContract(scripthash)

    if contract:
        sb = ScriptBuilder()
        sb.EmitAppCallWithOperationAndArgs(contract.Code.ScriptHash(), operation, args)
        # sb.EmitAppCallWithOperationAndArgs(self.ScriptHash, 'symbol')
        # sb.EmitAppCallWithOperationAndArgs(self.ScriptHash, 'decimals')

        out = sb.ToArray()

        outputs = []

        if neo_to_attach:

            output = TransactionOutput(AssetId=Blockchain.SystemShare().Hash,
                                       Value=neo_to_attach,
                                       script_hash=contract.Code.ScriptHash(),
                                       )
            outputs.append(output)

        if gas_to_attach:

            output = TransactionOutput(AssetId=Blockchain.SystemCoin().Hash,
                                       Value=gas_to_attach,
                                       script_hash=contract.Code.ScriptHash())

            outputs.append(output)

        return test_invoke(out, wallet, outputs, withdrawal_tx)

    else:

        print("Contract %s not found" % args[0])

    return None, None, None, None


class TheConstructInterface(object):

    running = True
    invoking = False
    operations_completed = [] 
    notify = None
    rebuilding = False
    active_color = ''

    invoked_operation = ''

    # SC_hash = '60d149a29f25f19cd8e3be816a69bf6300c755af' # 7490
    SC_hash = '32f7bfaec818e6b39523115be370c1ce02a024cc'  # 8000
    Wallet = None

    def __init__(self, debug=False):
        self.input_parser = InputParser()
        self.start_height = Blockchain.Default().Height
        self.start_dt = datetime.datetime.utcnow()
        settings.set_log_smart_contract_events(False)

        self.notify = NotificationDB.instance()

        # if debug:
        #     settings.set_log_smart_contract_events(True)
        
        # EVENTS
        @events.on(SmartContractEvent.RUNTIME_NOTIFY)
        @events.on(SmartContractEvent.RUNTIME_LOG)
        @events.on(SmartContractEvent.EXECUTION_SUCCESS)
        @events.on(SmartContractEvent.EXECUTION_FAIL)
        @events.on(SmartContractEvent.STORAGE)        
        def on_sc_event(sc_event):
            if sc_event.test_mode:
                self.active_color = colors.WARNING
            else:
                self.active_color = colors.GREEN
            
            if str(sc_event.contract_hash) == str(self.SC_hash):
                et = sc_event.event_type
                results = sc_event.event_payload               
                
                if et == SmartContractEvent.RUNTIME_LOG:
                    if sc_event.test_mode:
                        try:
                            decoded_result = results[0].decode("utf-8")
                            if ':' in decoded_result:
                                self.invoked_operation = decoded_result.split(':')[-1]
                        except:
                            pass
                                
                
                if et == SmartContractEvent.EXECUTION_SUCCESS or et == SmartContractEvent.RUNTIME_NOTIFY:
                    print(self.active_color+'\n|--------   T H E    C O N S T R U C T  --------|'+colors.ENDC)
                    
                    for result in results:
                        if self.invoked_operation in ['fs_attribute', 'get_active_index', 'update_active_ms_progress', 'get_ms_progess']:
                            result = int.from_bytes(result, byteorder='little', signed=False)
                        print('\033[1m Output:\033[0m \t\t\t', result)

                    if sc_event.test_mode:
                        print('\n \033[1mSuccessfully Sent Request:\033[0m\t', self.invoked_operation)
                        print('\n Please wait for block to process.. ')                      
                    else:
                        print('\n \033[1mSuccessfully Executed Request:\033[0m\t', self.invoked_operation)
                        self.invoking = False
                        self.invoked_operation = ''
                    
                    print(self.active_color+'|-----------------------------------------------|'+colors.ENDC)
                    print('\n')
                    


                elif debug:
                    print(self.active_color+'\n|--------   T H E    C O N S T R U C T  --------|'+colors.ENDC)
                    print(' Event Type: ', et)
                    for result in results:
                        print(' \033[1mOutput:\033[0m \t\t\t', result)
                    print('\n')

    def run(self):
        dbloop = task.LoopingCall(Blockchain.Default().PersistBlocks)
        dbloop.start(.1)

        Blockchain.Default().PersistBlocks()  
        
        self.open_wallet('../neo-python-priv-wallet.db3', '1234567890')
        # print(self.Wallet.ToJson()['synced_balances'])


        # Check Node and Wallet status
        self.height_check()  
        
        # Test Methods to invoke
        addrs = [ 
            bytearray(b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9')]

        print('CONTRACT: ', self.SC_hash)
        # self.invoke_fr_config(fr_config, test=False)
        # # self.invoke_construct("create_sts", ["TheConstruct2", "MFP", 8, bytearray(b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'), 1000000])
        # # self.invoke_construct("create_fs", ["TheConstruct2", "first_stage", 1, 999999, 1000, 100])
        # # self.invoke_construct("create_fs", ["TheConstruct2", "second_stage", 1, 999999, 1000, 100])
        # # self.invoke_construct("create_ms", ["TheConstruct2", "first_milestone", "SEED", "asdjnasd", "asdasd"])

        # self.invoke_construct("kyc_register", ["TheConstruct2"] + addrs)        
        # # self.invoke_construct("kyc_status", ["TheConstruct2"] + addrs)        
        # self.invoke_construct("fs_contribute", ["TheConstruct2", "first_stage"], gas=50)
        # self.invoke_construct("fs_status", ["TheConstruct2", "first_stage"], readonly=True)
        # self.invoke_construct("fs_attribute", ["TheConstruct2", "second_stage", "in_circulation"], readonly=True)
        # self.invoke_construct("fs_attribute", ["TheConstruct2", "second_stage", "supply"], readonly=True)
        # self.invoke_construct("get_active_index", ["TheConstruct2"], readonly=True)
        # self.invoke_construct("update_active_ms_progress", ["TheConstruct2", 110])
        # self.invoke_construct("get_active_index", ["TheConstruct2"], readonly=True)
        # self.invoke_construct("get_ms_progess", ["TheConstruct2", 'second_milestone'], readonly=True)
        # self.invoke_construct("fs_status", ["TheConstruct2", "second_stage"], readonly=True)
        self.invoke_construct("get_active_fs", ["TheConstruct2"], readonly=True)
        # # self.invoke_construct("get_active_ms", ["TheConstruct2"], readonly=True)
        # self.invoke_construct("get_funding_stages", ["TheConstruct2"], readonly=True)

        self.quit()

    def invoke_fr_config(self, config, test=False):         
        
        project = Struct(config['project'])
        funding_stages = config['funding_stages']
        milestones = config['milestones']
        

        if len(config['project']) != 4:
            print('Invalid Config')
            return     

        if not project.id:
            print('Invalid Config')
            return

        if len(funding_stages) != len(milestones):
            print('Number of Funding Stages and Milestones need to match')
            return 
            
        # CREATE SMART TOKEN SHARE
        self.invoke_construct("create_sts", [project.id, project.symbol, 8, project.owner, project.total_supply], test=test)

        # CREATE FUNDING STAGES
        for funding_stage in funding_stages:
            if len(funding_stage) != 5:
                print('Invalid Config for Funding Stage')
                return 

            fs = Struct(funding_stage)
            self.invoke_construct("create_fs", [project.id, fs.id, fs.start_block, fs.end_block, fs.supply, fs.tokens_per_gas], test=test)

        # CREATE MILESTONES
        for milestone in milestones:
            if len(milestone) != 4:
                print('Invalid Config for Milestone: ', milestone)
                return 

            ms = Struct(milestone)
            self.invoke_construct("create_ms", [project.id, ms.id, ms.title, ms.subtitle, ms.extra_info_hash], test=test)


    # INVOKE
    def invoke_construct(self, operation, args, gas=None, readonly=False, test=False):        
        self.invoking = True
        
        arguments = [self.SC_hash, operation, str(args)]
        
        if gas:
            gas = '--attach-gas='+str(gas)
            arguments = [self.SC_hash, operation, str(args), gas]
                    

        print('invoke_construct: ', arguments)
        if test:
            return

        tx, fee, results, num_ops = TestInvokeContract(self.Wallet, arguments)
        print('tx', tx)
        print('fee', fee)
        print('results', results)
        print('num_ops', results)
        if tx is not None and results is not None:

            if readonly:
                self.invoking = False
                return
            
            result = InvokeContract(self.Wallet, tx, fee)    
        
        else:
            print('Invoke failed')
            self.quit()

        self.wait_for_invoke_complete()

    # CHECK NODE HEIGHT
    def height_check(self):
        last_height = 0
        neo = self.Wallet.GetBalance(self.Wallet.GetCoinAssets()[0])
        gas = self.Wallet.GetBalance(self.Wallet.GetCoinAssets()[1])
        
        while (Blockchain.Default().HeaderHeight - last_height) > 10:
            print('Updating Height...')
            last_height = Blockchain.Default().HeaderHeight
            sleep(5)

        print('Wallet Height: ', self.Wallet._current_height)
        print('Blockchain Height: ', Blockchain.Default().Height)
        print('Header Height: ', Blockchain.Default().HeaderHeight)
        print('Gas Balance: ', gas)

        if self.Wallet._current_height <= Blockchain.Default().Height-20 or gas.ToInt() == 0: 
                        
            self.Wallet.Rebuild()            
            while self.Wallet._current_height < Blockchain.Default().Height-2:
                print('Rebuilding Wallet..')
                sleep(5)
    
    def wait_for_invoke_complete(self):
        while self.invoking:
            sleep(4)        
        sleep(0.5)

    # CREATE WALLET
    def create_wallet(self, path, password):
        try:
            self.Wallet = UserWallet.Create(path, password)
            contract = self.Wallet.GetDefaultContract()
            key = self.Wallet.GetKey(contract.PublicKeyHash)
            print("Wallet %s" % json.dumps(self.Wallet.ToJson(), indent=4))
            print("Pubkey %s" % key.PublicKey.encode_point(True))
        except Exception as e:            
            print("Exception creating wallet: %s" % e)
            self.Wallet = None
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print("Could not remove {}: {}".format(path, e))
            return

        if self.Wallet:
            self._walletdb_loop = task.LoopingCall(self.Wallet.ProcessBlocks)
            self._walletdb_loop.start(1)
    
    # OPEN WALLET
    def open_wallet(self, path, password):
        
        if not os.path.exists(path):
            print("Wallet file not found")
            return 
        
        try:
            self.Wallet = UserWallet.Open(path, password)

            self._walletdb_loop = task.LoopingCall(self.Wallet.ProcessBlocks)
            self._walletdb_loop.start(1)
            print("Opened wallet at %s" % path)
        except Exception as e:
            print("Could not open wallet: %s" % e)

    # QUIT
    def quit(self):
        print('Shutting down. This may take a bit...')
        self.running = False
        Blockchain.Default().Dispose()
        reactor.stop()
        NodeLeader.Instance().Shutdown()
        NotificationDB.close()
        exit(1)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Debug")
    parser.add_argument("-m", "--mainnet", action="store_true", default=False,
                        help="Use MainNet instead of the default TestNet")
    parser.add_argument("-p", "--privnet", action="store_true", default=False,
                        help="Use PrivNet instead of the default TestNet")
    parser.add_argument("-c", "--config", action="store", help="Use a specific config file")
    parser.add_argument('--version', action='version',
                        version='neo-python v{version}'.format(version=__version__))

    args = parser.parse_args()

    if args.config and (args.mainnet or args.privnet):
        print("Cannot use both --config and --mainnet/--privnet arguments, please use only one.")
        exit(1)
    if args.mainnet and args.privnet:
        print("Cannot use both --mainnet and --privnet arguments")
        exit(1)

    # Setup depending on command line arguments. By default, the testnet settings are already loaded.
    if args.config:
        settings.setup(args.config)
    elif args.mainnet:
        settings.setup_mainnet()
    elif args.privnet:
        settings.setup_privnet()
    
    # Instantiate the blockchain and subscribe to notifications
    blockchain = LevelDBBlockchain(settings.LEVELDB_PATH)
    Blockchain.RegisterBlockchain(blockchain)
    
    # Try to set up a notification db
    if NotificationDB.instance():
        NotificationDB.instance().start()

    cli = TheConstructInterface(debug=args.debug)

    # Run
    reactor.suggestThreadPoolSize(15)
    reactor.callInThread(cli.run)
    NodeLeader.Instance().Start()
    reactor.run()

if __name__ == "__main__":
    main()

fr_config_template = {
    'project': {
        'id':                   '',
        'symbol':               '',
        'owner':               b'',
        'total_supply':         0,
    },
    'funding_stages':[
        { 
            'id':               'first_stage',
            'start_block':      0,
            'end_block':        0,
            'supply':           0,
            'tokens_per_gas':   0,
        }
    ],
    'milestones':[ 
        {
            'id':               'first_milestone',
            'title':            '',
            'subtitle':         '',
            'extra_info_hash':  '',
        }
    ]
}

