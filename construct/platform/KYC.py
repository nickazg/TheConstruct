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
    
    # User submit
    def kyc_submit(self, sts:SmartTokenShare, address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash):
        storage = StorageManager()
        if CheckWitness(address):
            if len(address) == 20:
                kyc_array = list(address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash)
                serialized_kyc_sub = storage.serialize_array(output_kyc_array)
                storage.put_triple('KYC', sts.project_id, address, serialized_kyc_sub)
                return address
    
    # Admin check
    def get_kyc_submission(self, sts:SmartTokenShare, address):
        storage = StorageManager()
        if CheckWitness(sts.owner):
            if len(address) == 20:
                serialized_kyc_sub = storage.get_triple('KYC', sts.project_id, address)
                return storage.deserialize_bytearray(serialized_kyc_sub)                

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