from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Settings import settings
from neocore.UInt160 import UInt160
from neo.Wallets.utils import to_aes_key
import os
from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase

settings.USE_DEBUG_STORAGE = False
# settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class ConstructTest(WalletFixtureTestCase):

    dirname = None
    
    wallet_1_script_hash = UInt160(data=b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)')

    wallet_1_addr = 'APRgMZHZubii29UXF9uFa6sohrsYupNAvx'

    _wallet1 = None

    @classmethod
    def setUpClass(cls):

        cls.dirname = '/'.join(os.path.abspath(__file__).split('/')[:-3])

        super(ConstructTest, cls).setUpClass()

    @classmethod
    def GetWallet1(cls, recreate=False):
        if cls._wallet1 is None or recreate:
            cls._wallet1 = UserWallet.Open(ConstructTest.wallet_1_dest(), to_aes_key(ConstructTest.wallet_1_pass()))
        return cls._wallet1

