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
    def kyc_submit(self, project_id, address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash):
        """    
        Submits a KYC information to the smart contract 
        Args:
            sts (SmartTokenShare):
                Smart Token Share reference object
            
            address (str):
                Wallet address to whitelist

            phys_address (str):
                Physical Address

            first_name (str):
                First Name

            last_name (str):
                Last Name

            id_type (str):
                Id type, eg passport, drivers licence

            id_number (str):
                ID Number

            id_expiry (str):
                Expiry data

            file_location (str):
                web location where file is stored

            file_hash (str):
                hash of file
        """
        storage = StorageManager()

        # Checking its the correct address
        if CheckWitness(address):
            if len(address) == 20:

                # Combines all args into a single list
                output_kyc_array = list(address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash)
                
                # Serialises list into a single bytearray, and stores that into storeage
                serialized_kyc = storage.serialize_array(output_kyc_array)
                storage.put_triple('KYC', project_id, address, serialized_kyc)
    
    # Admin check
    def get_kyc_submission(self, project_id, address):
        """    
        Submits a KYC information to the smart contract 
        Args:
            sts (SmartTokenShare):
                Smart Token Share reference object
            
            address (str):
                Wallet address to whitelist
        Returns:
            (list): Of KYC submission list (address, phys_address, first_name, last_name, id_type, id_number, id_expiry, file_location, file_hash)
        """
        storage = StorageManager()

        sts = SmartTokenShare()
        sts_info = sts.get_info(project_id)

        owner = sts_info[sts.owner_idx]

        # Checking the invoker is the owner/admin
        if CheckWitness(owner):
            if len(address) == 20:

                # Deserialises bytearray back into a list
                serialized_kyc_sub = storage.get_triple('KYC', project_id, address)
                return storage.deserialize_bytearray(serialized_kyc_sub)                

    # Requires Admin to invoke
    def kyc_register(self, project_id, addresses):
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
        sts = SmartTokenShare()
        sts_info = sts.get_info(project_id)

        owner = sts_info[sts.owner_idx]

        ok_count = 0
        
        # Ignoring the first arg which should be the project_id
        # addresses = args[1:]

        if CheckWitness(owner):

            for address in addresses:

                if len(address) == 20:

                    storage = StorageManager()
                    storage.put_triple(project_id, 'KYC_address', address, True)

                    OnKYCRegister(project_id, address)
                    ok_count += 1

        return ok_count


    def kyc_status(self, project_id, address):
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

        return storage.get_triple(project_id, 'KYC_address', address)