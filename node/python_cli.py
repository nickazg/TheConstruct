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

from neo.EventHub import events, SmartContractEvent

from neocore.Cryptography.Crypto import Crypto

# events = EventEmitter(wildcard=True)

# ['157a025e90760b680a660126e6bdfe53b1decf03', 'create_fs', "['MyFirstProj', 'FUNDING_ID', 1, 9999, 10000, 100]"]
# ['ae444436fe6f020d27a2effe3d7f02e3dbc98acc', 'create_sts', '[\'MyFirstProj\', \'MFP\', 8, bytearray(b\'#\\xba\\\'\\x03\\xc52c\\xe8\\xd6\\xe5"\\xdc2 39\\xdc\\xd8\\xee\\x\ne9\'), 1000000]']


# If you want the log messages to also be saved in a logfile, enable the
# next line. This configures a logfile with max 10 MB and 3 rotations:
# settings.set_logfile("/tmp/logfile.log", max_bytes=1e7, backup_count=3)

TEST = ['157a025e90760b680a660126e6bdfe53b1decf03', 'create_sts', '["MyFirstProj", "MFP", 8, bytearray(b"\\x01\\x05\\x01\\x01\\x01\\x01\\x02\\x0f\\\'\\x01\\x02\\x10\\\'\\x01\\x01d\\x01\\x01\\x00"), 1000000]']

CONTRACT_SH = b''

CHAIN = 'privnet'

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[34m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

class TheConstructInterface(object):

    running = True
    invoking = False
    operations_completed = [] 
    notify = None
    rebuilding = False
    active_color = ''

    invoked_operation = ''

    # SC_hash = '6f2bf7aa7148efa29f0a527b261c7ef17204685a'    
    SC_hash = '157a025e90760b680a660126e6bdfe53b1decf03'    
    # SC_hash = 'ae444436fe6f020d27a2effe3d7f02e3dbc98acc'    
    # SC_hash = 'aaa37379f032bb70309982c68e2424cb2b6fe090'    
    Wallet = None

    def __init__(self, debug=False):
        self.input_parser = InputParser()
        self.start_height = Blockchain.Default().Height
        self.start_dt = datetime.datetime.utcnow()
        settings.set_log_smart_contract_events(False)

        self.notify = NotificationDB.instance()

        if debug:
            settings.set_log_smart_contract_events(True)
        
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
                                
                
                if et == SmartContractEvent.EXECUTION_SUCCESS:
                    print(self.active_color+'\n|--------   T H E    C O N S T R U C T  --------|'+colors.ENDC)
                    
                    for result in results:
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
                    for result in results:
                        print(' \033[1mOutput:\033[0m \t\t\t', result)
                    print('\n')

                

    def run(self):
        dbloop = task.LoopingCall(Blockchain.Default().PersistBlocks)
        dbloop.start(.1)

        Blockchain.Default().PersistBlocks()  
        
        self.open_wallet('../neo-python-priv-wallet.db3', '1234567890')
        # print(self.Wallet.ToJson()['synced_balances'])

        self.height_check()
        
        # while self.running:
        # logger.info("Block %s / %s", str(Blockchain.Default().Height), str(Blockchain.Default().HeaderHeight))
        # logger.info("Wallet %s / %s", str(self.Wallet._current_height), str(Blockchain.Default().Height))
        # if self.Wallet._current_height <= Blockchain.Default().Height-20:                
        #     self.Wallet.Rebuild()
        #     self.rebuilding = True               
            
        #     while self.Wallet._current_height < Blockchain.Default().Height-2:
        #         print('Rebuilding..')
        #         sleep(5)
        
        # if self.invoking:
        #     self.wait_for_invoke_complete()
        
        self.invoke_construct("create_sts", ["MyFirstProj", "MFP", 8, bytearray(b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'), 1000000])
        self.invoke_construct("create_fs", ["MyFirstProj", "FUNDING_ID", 1, 9999, 10000, 100])
        
        # self.invoke_construct("create_sts", ["MyFirstProj", "MFP", 8, bytearray(b"\\x01\\x05\\x01\\x01\\x01\\x01\\x02\\x0f\\\'\\x01\\x02\\x10\\\'\\x01\\x01d\\x01\\x01\\x00"), 1000000])
        # self.invoke_construct("create_sts", "[\"MyFirstProj\", \"MFP\", 8, bytearray(b\"\\x01\\x05\\x01\\x01\\x01\\x01\\x02\\x0f\\\'\\x01\\x02\\x10\\\'\\x01\\x01d\\x01\\x01\\x00\"), 1000000]")
        # self.invoke_construct("create_fs", "[\"MyFirstProj\", \"FUNDING_ID\", 1, 9999, 10000, 100]")
        # self.invoke_construct("fs_status", "[\"MyFirstProj\", \"funding_ids\"]")


        self.quit()


    def height_check(self):
        last_height = 0
        while (Blockchain.Default().HeaderHeight - last_height) > 10:
            print('Updating Height...')
            last_height = Blockchain.Default().HeaderHeight
            sleep(5)

        print('Wallet Height: ', self.Wallet._current_height)
        print('Blockchain Height: ', Blockchain.Default().Height)
        print(self.Wallet.ToJson()['synced_balances'])

        gas = self.Wallet.GetBalance(self.Wallet.GetCoinAssets()[1], True)
        print('gas', gas)

        if self.Wallet._current_height <= Blockchain.Default().Height-20: 
                        
            self.Wallet.Rebuild()
            
            while self.Wallet._current_height < Blockchain.Default().Height-2:
                print('Rebuilding Wallet..')
                sleep(5)
    
    def wait_for_invoke_complete(self):
        while self.invoking:
            sleep(2)        
        

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

    # INVOKE
    def invoke_construct(self, operation, args):
         
        
        self.invoking = True

        arguments = [self.SC_hash, operation, str(args)]
        
        tx, fee, results, num_ops = TestInvokeContract(self.Wallet, arguments)
        
        if tx is not None and results is not None:
            result = InvokeContract(self.Wallet, tx, fee)    
        
        else:
            print('Invoke failed')
            self.quit()

        self.wait_for_invoke_complete()

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
