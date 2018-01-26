from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.common.StorageManager import StorageManager
from construct.platform.SmartTokenShare import SmartTokenShare

OnTransfer = RegisterAction('transfer','project_id' , 'from', 'to', 'amount')
OnRefund = RegisterAction('refund','project_id' , 'to', 'amount')

OnInvalidKYCAddress = RegisterAction('invalid_registration','project_id' ,'address')
OnKYCRegister = RegisterAction('kyc_registration','project_id' ,'address')

class KYC():
    """
    Manages KYC registration and lookup
    """

    def kyc_register(self, args, sts:SmartTokenShare):
        """    
        Registers all input addresses 
        Args:
            args (list):
                list a list of arguments
            
            sts (SmartTokenShare):
                Smart Token Share reference object

        Return:
            (int): The number of addresses to registered for KYC
        """
        ok_count = 0
        
        # Ignoring the first arg which should be the project_id
        addresses = args[1:]

        if CheckWitness(sts.owner):

            for address in addresses:

                if len(address) == 20:

                    storage = StorageManager()
                    storage.put_triple(sts.project_id, 'KYC_address', address, True)

                    OnKYCRegister(sts.project_id, address)
                    ok_count += 1

        return ok_count


    def kyc_status(self, args, sts:SmartTokenShare):
        """
        Gets the KYC Status of an address

        Args:
            args (list):
                list a list of arguments
            
            sts (SmartTokenShare):
                Smart Token Share reference object
        Return:
            (bool): Returns the kyc status of an address
        """
        storage = StorageManager()

        if len(args) > 1:
            address = args[1]

            return storage.get_triple(sts.project_id, 'KYC_address', address)

        return False