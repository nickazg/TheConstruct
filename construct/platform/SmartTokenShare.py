from construct.common.StorageManager import StorageManager
from boa.code.builtins import concat

class SmartTokenShare():
    """
    Basic template for a projects smart token share, based on NEP5 token
    """    
    symbol = 'PROJ'

    project_id = 'b327h982'

    decimals = 8

    # This is the script hash of the address for the owner of the token
    owner = b'\xaf\x12\xa8h{\x14\x94\x8b\xc4\xa0\x08\x12\x8aU\nci[\xc1\xa5'
    
    total_supply = 10000000 * 100000000  # 10m total supply * 10^8 ( decimals)
    
    current_supply = 1000 * 100000000  # 10m total supply * 10^8 ( decimals)

    # Current ratio for every gas token, this will be updated for each funding stage
    current_tokens_per_gas = 1 * 100000000

    # Specifies if the token is able to be minted.
    # current_sale_active = False

    # when to start the crowdsale
    current_sale_start_block = 1

    # when to end the initial limited round
    current_sale_end_block = 1000

    # Create new project token
    def deploy_new_project_sts(self, project_id:str, owner:bytes, symbol:str, decimals:int):
        """Method to Deploy a new project Smart Token Share
        Args:
            project_id (str):
                ID for referencing the project
            owner (bytes):
                Script hash address of the token owner aka project address
            symbol (str):
                Symbol to represent Smart Token Share
            decimals (int):
                Number of decimals

        Return:
            (int): status code representing if execution was a success.
        """   
        storage = StorageManager()
        
        # Checks if project isnt saved already
        if storage.get_type('STS_symbol', project_id) != symbol:
            storage.put_type('STS_symbol', project_id, symbol)
            storage.put_type('STS_decimals', project_id, decimals)

            self.symbol = symbol
            self.project_id = project_id
            self.decimals = decimals

            return 1
        
        else:
            return 0    
    
    # Pulling all token info from storage
    def get_project(self, project_id:str):
        storage = StorageManager()
        symbol = storage.get_type('STS_symbol', project_id)
        decimals = storage.get_type('STS_decimals', project_id)
        current_sale_start_block = storage.get_type('STS_current_sale_start_block', project_id)
        current_sale_end_block = storage.put_type('STS_current_sale_end_block', project_id)
        current_supply = storage.put_type('STS_current_supply', project_id)
        current_tokens_per_gas = storage.put_type('STS_current_tokens_per_gas', project_id)

        if symbol:
            self.symbol = symbol
            self.project_id = project_id
            self.decimals = decimals
            self.current_sale_start_block = current_sale_start_block
            self.current_sale_end_block = current_sale_end_block
            self.current_supply = current_supply
            self.current_tokens_per_gas =  current_tokens_per_gas

            return 1
        
        else:
            return 0

    
    def start_new_crowdfund(self, project_id:str, start_block:int, end_block:int, supply:int, tokens_per_gas:int):
        storage = StorageManager()        
        storage.put_type('STS_current_sale_start_block', project_id, start_block)
        storage.put_type('STS_current_sale_end_block', project_id, end_block)
        storage.put_type('STS_current_tokens_per_gas', project_id, tokens_per_gas)
        self.current_sale_start_block = start_block
        self.current_sale_end_block = end_block
        self.current_tokens_per_gas = tokens_per_gas

        in_circ = storage.get_type('STS_in_circ', project_id)
        self.current_supply = in_circ + supply
        
        storage.put_type('STS_current_supply', project_id, self.current_supply)


    def current_available_amount(self, project_id:str):
        """
        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The avaliable tokens for the current sale
        """
        storage = StorageManager()
        in_circ = storage.get_type('STS_in_circ', project_id)
        self.current_supply = storage.get_type('STS_current_supply', project_id)
       
        current_available = self.current_supply - in_circ
        return current_available

    def total_available_amount(self, project_id:str):
        """
        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The avaliable tokens for the total project
        """
        storage = StorageManager()
        in_circ = storage.get_type('STS_in_circ', project_id)

        total_available = self.total_supply - in_circ
        return total_available

    def add_to_circulation(self, project_id:str, amount:int):
        """
        Adds an amount of token to circlulation

        Args:
            project_id (str):
                ID for referencing the project
            amount (int):
                amount of tokens added
        """
        storage = StorageManager()
        in_circ = storage.get_type('STS_in_circ', project_id)

        in_circ += amount

        storage.put_type('STS_in_circ', project_id, in_circ)

    def get_circulation(self, project_id:str):
        """
        Get the total amount of tokens in circulation

        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The total amount of tokens in circulation
        """
        storage = StorageManager()
        return storage.get_type('STS_in_circ', project_id)