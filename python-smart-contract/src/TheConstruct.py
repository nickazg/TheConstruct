"""
TheConstruct - NEO smart contract - https://github.com/nickazg/TheConstruct
"""

VERSION = "0.0.1"

from boa.blockchain.vm.Neo.Runtime import Log
from boa.blockchain.vm.Neo.Storage import GetContext, Put
from boa.blockchain.vm.Neo.Transaction import GetHash
from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer
from boa.code.builtins import concat