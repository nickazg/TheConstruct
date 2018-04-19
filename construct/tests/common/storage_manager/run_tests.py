# from construct.tests.construct_test import ConstructTest
from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.VM.InteropService import StackItem, Array, ByteArray
from neocore.IO.BinaryReader import BinaryReader
from neo.IO.MemoryStream import StreamManager
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Wallets.utils import to_aes_key
DIR = '/Users/nick/Documents/Git/NeoDev/TheConstruct/construct/tests'

WALLET = UserWallet.Open('/Users/nick/Documents/Git/NeoDev/TheConstruct/construct/tests/wallet1.db3', to_aes_key('testpassword'))

class TestStorageManager(BoaTest):

    def test_serialize(self):
        output = Compiler.instance().load('%s/common/storage_manager/test_serialize.py' % DIR).default
        out = output.write()
        tx, results, total_ops, engine = TestBuild(out, [1], WALLET, '02', '05')
        self.assertEqual(len(results), 1)
        print('results[0]',results[0])
        self.assertEqual(results[0].GetByteArray(), bytearray(b'\x80\x05\x00\x01a\x02\x01\x03\x80\x03\x00\x01j\x02\x01\x03\x02\x01\x05\x00\x02jk\x00\x07lmnopqr'))



tsm = TestStorageManager()
tsm.test_serialize()