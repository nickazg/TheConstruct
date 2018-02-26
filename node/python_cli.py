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
import pprint

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
from neo.Prompt.Commands.LoadSmartContract import LoadContract, GatherContractDetails, \
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
from neo.Prompt.Utils import parse_param, lookup_addr_str

from neo.EventHub import events, SmartContractEvent

from neocore.Cryptography.Crypto import Crypto

from neo.Wallets.utils import to_aes_key

import binascii
from neo.Prompt.Utils import parse_param
from neo.Core.FunctionCode import FunctionCode
from neo.Core.State.ContractState import ContractPropertyState
from prompt_toolkit import prompt
import json
from neo.Prompt.Utils import get_arg
from neo.SmartContract.Contract import Contract


def safe(unsafe_str, undo=False):
    if undo:
        return unsafe_str.replace('_', ' ')
    return unsafe_str.replace(' ', '_')

# Creates an object from a dict (one layer)
class Struct(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


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

    SC_hash = '17e92c33e613e0f2f34fda070451e50ec2f14e01' 
    Wallet = None

    project_id = ''

    def __init__(self, input_args=None, debug=False):
        self.input_parser = InputParser()
        self.input_args = input_args
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
                
                
                if not debug and sc_event.test_mode:  
                    return 
                
                # Inding the invoked op
                if et == SmartContractEvent.RUNTIME_LOG and sc_event.test_mode:
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
                    
                    self.op_output = results
                    
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

        self.arg_handler(self.input_args)

        # Check Node and Wallet status
        self.height_check()  
              
        self.quit()


    def arg_handler(self, args):
        
        # WALLET - REQUIRED
        if args.wallet and args.password:
            self.open_wallet(args.wallet, to_aes_key(args.password))
            self.height_check()
        else:
            print('Need to pass in wallet path AND password eg  "-w /path/to/wallet.db3  -pass 1234"')
            return

        # FR CONFIG JSON
        if args.fr_config:
                self.invoke_setup_config(args.fr_config, from_json=True, test=False)

        # PROJECT - REQUIRED
        if args.project:
            self.project_id = args.project
        
        if not self.project_id:
            print('Need to pass in project id  "-pro MyProject"')
            return
        
        # SUMMARY
        if args.summary:
            project_summary = self.get_project_summary()
            pprint.pprint(project_summary)

        
        # CONTRIBUTE 
        if args.send_gas and args.funding_stage:
            fs_id = args.funding_stage
            gas_to_send = int(args.send_gas)
            self.invoke_construct("fs_contribute", [self.project_id, fs_id], gas=gas_to_send)
        
        elif args.send_gas and args.funding_stage:
            print('Funding stage needs to be specified if sending gas eg: "-fs first_stage -send 10"')    
        
        
        # INVOKE
        if args.invoke and args.args:
            print('args.args', args.args)
            self.invoke_construct( args.invoke, eval(args.args))
            
        
        if args.claim_contributions and args.funding_stage and args.to_addr and args.from_addr:
            # to_addr_data = lookup_addr_str(self.Wallet, args.to_addr).Data
            # from_addr_data = lookup_addr_str(self.Wallet, args.from_addr).Data
            fs_id = args.funding_stage
            self.invoke_construct_claim('claim_fs_contributions', fs_id, to_addr=args.to_addr, from_addr=args.from_addr)


        if args.claim_refund and args.funding_stage and args.to_addr and args.from_addr:
            # to_addr_data = lookup_addr_str(self.Wallet, args.to_addr).Data
            # from_addr_data = lookup_addr_str(self.Wallet, args.from_addr).Data
            fs_id = args.funding_stage
            self.invoke_construct_claim('claim_refund', fs_id, to_addr=args.to_addr, from_addr=args.from_addr)

        # KYC 
        if args.kyc_register:
            addr = args.kyc_register
            self.invoke_construct("kyc_register", [self.project_id, addr])

        if args.kyc_status:
            addr = args.kyc_status
            self.invoke_construct("kyc_status", [self.project_id, addr])

        # parser.add_argument("-ms", "--milestone", action="store", help="Milestone)

    
    def get_project_summary(self):
        
        print('\n*NOTE: Reading Information from Contract, No fees will be charged (Ignore any fee messages)\n')
        summary = {
            'project':{
                'id':self.project_id
            },
        }

        # Getting STS info
        sts_attrs = ['symbol', 'decimals', 'owner', 'total_supply', 'total_in_circulation']        
        for sts_attr in sts_attrs:
            attr = self.invoke_construct("sts_attribute", [self.project_id, sts_attr], readonly=True, wait=True)
            
            # For Strings
            if sts_attr in ['symbol']:
                summary['project'][sts_attr] = [item.GetString() for item in attr][0]
            
            # For Ints
            elif sts_attr in ['decimals', 'total_supply', 'total_in_circulation']:
                summary['project'][sts_attr] = [item.GetBigInteger() for item in attr][0]

            # Everything else
            else:
                summary['project'][sts_attr] = [item.GetByteArray() for item in attr][0]

       
        # Getting all FS info
        fss_raw = self.invoke_construct("get_funding_stages", [self.project_id], readonly=True, wait=True)
        fss_array = [item.GetArray() for item in fss_raw][0]
        fss = [item.GetString() for item in fss_array]
        summary['funding_stages'] = {}
        for fs_id in fss:
            summary['funding_stages'][fs_id] = {}
            fs_attrs = ['start_block', 'end_block', 'supply', 'tokens_per_gas', 'in_circulation']
            for fs_attr in fs_attrs:
                attr = self.invoke_construct("fs_attribute", [self.project_id, fs_id, fs_attr], readonly=True, wait=True)
                summary['funding_stages'][fs_id][fs_attr] = [item.GetBigInteger() for item in attr][0]

        # Getting all MS info
        mss_raw = self.invoke_construct("get_milestones", [self.project_id], readonly=True, wait=True)
        mss_array = [item.GetArray() for item in mss_raw][0]
        mss = [item.GetString() for item in mss_array]
        summary['milestones'] = {}     
        for ms_id in mss:
            summary['milestones'][ms_id] = {}
            ms_attrs = ['title', 'subtitle', 'extra_info_hash', 'progress']
            for ms_attr in ms_attrs:
                attr = self.invoke_construct("ms_attribute", [self.project_id, ms_id, ms_attr], readonly=True, wait=True)
                
                # For Strings
                if ms_attr in ['title', 'subtitle', 'extra_info_hash']:
                    summary['milestones'][ms_id][ms_attr] = [ safe(item.GetString(), True) for item in attr][0]
                
                # For Ints
                elif ms_attr in ['progress']:
                    summary['milestones'][ms_id][ms_attr] = [item.GetBigInteger() for item in attr][0]
        
        # Main INFO
        active_idx_raw = self.invoke_construct("get_active_index", [self.project_id], readonly=True, wait=True)
        active_idx = [item.GetBigInteger() for item in active_idx_raw][0]
        current_fs = fss[active_idx]
        current_ms = mss[active_idx]

        fs_status_raw = self.invoke_construct("fs_status", [self.project_id, current_fs], readonly=True, wait=True)

        fs_status = "Unknown.."
        try:
            fs_status_int = fs_status_raw[0].GetBigInteger()
            if fs_status_int == 1:
                fs_status = (fs_status_int, "Funding Stage completed successfully")
            if fs_status_int == 2:
                fs_status = (fs_status_int, "Funding Stage still active")
            if fs_status_int == 3:          
                fs_status = (fs_status_int,"Funding Stage failed")
        except:
            print("Failed to get 'fs_status'")
        
        cur_supply = summary['funding_stages'][current_fs]['supply']
        cur_circ = summary['funding_stages'][current_fs]['in_circulation']
        curent_stage_percent = ( (cur_supply - cur_circ) / cur_supply ) * 100 
        current_milestone_percent = summary['milestones'][current_ms]['progress']

        summary['project']['current_funding_stage'] = current_fs
        summary['project']['current_milestone'] = current_ms
        summary['project']['funded_percent'] = curent_stage_percent        
        summary['project']['funding_stage_status'] = fs_status        
        summary['project']['milestone_percent'] = current_milestone_percent

        return summary

    def invoke_setup_config(self, config, from_json=False, test=False):         
        if from_json:
            json_file = open(config)
            json_str = json_file.read()
            json_data = json.loads(json_str)
            config = json_data

        self.project_id = config['project']['id']
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
        
        # Getting SH bytearray
        project_owner_data = lookup_addr_str(self.Wallet, project.owner).Data
            
        # CREATE SMART TOKEN SHARE
        self.invoke_construct("create_sts", [project.id, project.symbol, 8, project_owner_data, project.total_supply], test=test)

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
            self.invoke_construct("create_ms", [project.id, ms.id, safe(ms.title), safe(ms.subtitle), ms.extra_info_hash], test=test)

    # INVOKE
    def invoke_construct(self, operation, args, gas=None, readonly=False, test=False, wait=False):        
        self.invoking = True
        self.op_output = None
        
        arguments = [self.SC_hash, operation, str(args)]
        print('arguments', arguments)
        if gas:
            gas = '--attach-gas='+str(gas)
            arguments = [self.SC_hash, operation, str(args), gas]
                    
        if test:
            return

        tx, fee, results, num_ops = TestInvokeContract(self.Wallet, arguments)
        if tx is not None and results is not None:

            if readonly:
                self.invoking = False                
                return results
            
            result = InvokeContract(self.Wallet, tx, fee)    
        
        else:
            print('Invoke failed')
            self.quit()

        self.wait_for_invoke_complete()
 
    def invoke_construct_claim(self, claim_type, fs_id, from_addr, to_addr):

        # # Finding Pubkey for "to_addr"
        # pub_key = ''
        # for addr in self.Wallet.PubKeys():
        #     if addr['Address'] == to_addr:
        #         pub_key = addr['Public Key']

        # # Importing Contract to Pubkey(to_addr)
        # import_contract_args = [self.SC_hash, pub_key]
        # from_addr = ImportContractAddr(self.Wallet, import_contract_args)
        # # from_addr = ''
        # # print('from_addr', from_addr)
        
        # Pre Claim Invoke (Unlock funds to "to_addr")
        to_addr_data = lookup_addr_str(self.Wallet, to_addr).Data
        self.invoke_construct(claim_type, [self.project_id, fs_id, to_addr_data])
        
        # Checking amount owed on contract storage (Instant/No Fee)
        claim_owed_raw = self.invoke_construct('check_claim_owed', [self.project_id, to_addr_data], readonly=True, wait=True)
        print('claim_owed_raw', claim_owed_raw)
        claim_owed = claim_owed_raw[0].GetBigInteger() / Fixed8.D
        print('Current owing (Verified):', claim_owed)

        if claim_owed > 0:
        
            # Calim Verification Tx
            verification_args = ['gas', to_addr, str(claim_owed), '--from-addr='+str(from_addr)]
            print('verification_args', verification_args)
            construct_and_send(self, self.Wallet, verification_args)
    
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
        print('Commands completed.')
        self.running = False
        NodeLeader.Instance().Shutdown()        
        Blockchain.Default().Dispose()
        NotificationDB.close()
        reactor.stop()
 
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Debug")
    parser.add_argument("-m", "--mainnet", action="store_true", default=False,
                        help="Use MainNet instead of the default TestNet")
    parser.add_argument("-p", "--privnet", action="store_true", default=False,
                        help="Use PrivNet instead of the default TestNet")
    
    parser.add_argument("-w", "--wallet", action="store", help="Wallet path")
    parser.add_argument("-pass", "--password", action="store", help="Wallet path")
    parser.add_argument("-pro", "--project", action="store", help="Project")
    parser.add_argument("-fs", "--funding_stage", action="store", help="Funding Stage")
    parser.add_argument("-ms", "--milestone", action="store", help="Milestone")
    parser.add_argument("-con", "--fr_config", action="store", help="Funding Roadmap config")
    parser.add_argument("-sum", "--summary", action="store_true", default=False, help="Get Summary of project")

    parser.add_argument("-to_addr", "--to_addr", action="store", help="To Addr")
    parser.add_argument("-from_addr", "--from_addr", action="store", help="From addr")
    
    parser.add_argument("-send", "--send_gas", action="store", help="Contribute to project")
    parser.add_argument("-cr", "--claim_refund", action="store_true", default=False, help="Claim refund")
    parser.add_argument("-cc", "--claim_contributions", action="store_true", default=False, help="Claim contributions")

    parser.add_argument("-kyc", "--kyc_status", action="store", help="Get kyc status")
    parser.add_argument("-kreg", "--kyc_register", action="store", help="Register KYC addr")

    parser.add_argument("-invoke", "--invoke", action="store", help="Invoke operation")
    parser.add_argument("-args", "--args", action="store", help="Valuss to input as list []")


    

    args = parser.parse_args()

    if args.mainnet and args.privnet:
        print("Cannot use both --mainnet and --privnet arguments")
        exit(1)

    # Setup depending on command line arguments. By default, the testnet settings are already loaded.
    if args.mainnet:
        settings.setup_mainnet()
    elif args.privnet:
        settings.setup_privnet()
    
    # Instantiate the blockchain and subscribe to notifications
    blockchain = LevelDBBlockchain(settings.LEVELDB_PATH)
    Blockchain.RegisterBlockchain(blockchain)
    
    # Try to set up a notification db
    if NotificationDB.instance():
        NotificationDB.instance().start()

    cli = TheConstructInterface(input_args=args, debug=args.debug)
    

    # Run
    reactor.suggestThreadPoolSize(15)
    reactor.callInThread(cli.run)
    NodeLeader.Instance().Start()
    reactor.run()




if __name__ == "__main__":
    main()

    

