from construct.common.StorageManager import StorageManager
from boa.code.builtins import list

class SmartTokenShare():
    """
    Interface for managing a Smart Token Share (STS). Based on NEP5 token, however all values 
    are dymanically stored in the contract storage.
    """
    symbol_idx = 0
    decimals_idx = 1
    owner_idx = 2
    total_supply_idx = 3
    in_circulation_idx = 4

    def create(self, project_id, symbol, decimals, owner, total_supply):
        """
        Args:
            project_id (str):
                ID for referencing the project

            symbol (str):
                Representation symbol
                
            decimals (int):
                Amount of decimal places, default 8

            owner (bytes):
                Owner of the token

            total_supply (int):
                total supply of the token
        Return:
            (None): 
        """
        storage = StorageManager()

        # Default circulation
        in_circulation = 0

        # Info structure
        sts_info = [symbol, decimals, owner, total_supply, in_circulation]

        # Will only save to storage if none exsits for this project_id
        if not storage.get_double('STS', project_id):
            sts_info_serialized = storage.serialize_array(sts_info)
            storage.put_double('STS', project_id, sts_info_serialized)

    def total_available_amount(self, project_id):
        """
        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The avaliable tokens for the total project
        """
        storage = StorageManager()
        
        # Pull STS info
        sts_info_serialized = storage.get_double('STS', project_id)
        sts_info = storage.deserialize_bytearray(sts_info_serialized)

        # STS vars
        in_circulation = sts_info[4]
        supply = sts_info[3]

        available = supply - in_circulation

        return available

    def add_to_total_circulation(self, project_id:str, amount:int):
        """
        Adds an amount of token to circlulation

        Args:
            project_id (str):
                ID for referencing the project
            amount (int):
                amount of tokens added
        """
        storage = StorageManager()
        
        # Pull STS info
        sts_info_serialized = storage.get_double('STS', project_id)
        sts_info = storage.deserialize_bytearray(sts_info_serialized)

        # info into vars
        symbol = sts_info[0]
        decimals = sts_info[1]
        owner = sts_info[2]
        total_supply = sts_info[3]
        in_circulation = sts_info[4]

        # Calculation
        in_circulation = in_circulation + amount 

        # output STS info
        updated_sts_info = [symbol, decimals, owner, total_supply, in_circulation]
        
        # Save STS info
        updated_sts_info_serialized = storage.serialize_array(updated_sts_info)
        storage.put_double('STS', project_id, updated_sts_info_serialized)    

    def get_total_circulation(self, project_id:str):
        """
        Get the total amount of tokens in circulation

        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The total amount of tokens in circulation
        """        
        storage = StorageManager()
        
        # Pull STS info
        sts_info_serialized = storage.get_double('STS', project_id)
        sts_info = storage.deserialize_bytearray(sts_info_serialized)

        # in_circulation var
        in_circulation = sts_info[4]

        return in_circulation

    def get_info(self, project_id:str):
        """
        Get the info list

        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (list): info list
        """    
        storage = StorageManager()
        
        # Pull STS info
        sts_info_serialized = storage.get_double('STS', project_id)
        sts_info = storage.deserialize_bytearray(sts_info_serialized)

        return sts_info