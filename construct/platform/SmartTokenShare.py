from construct.common.StorageManager import StorageManager

class SmartTokenShare():
    """
    A Template for a Smart Token Share (STS), based on NEP5 token however all variables 
    are stored in the contract storage.
    """    
    symbol = ''

    project_id = ''

    decimals = 8

    # This is the script hash of the address for the owner of the token
    owner = b''
    
    # Standard 10m total supply * 10^8 ( decimals) 
    total_supply = 10000000 * 100000000  
    
    current_supply = 0

    # Current ratio for every gas token, this will be updated for each funding stage
    current_tokens_per_gas = 1 * 100000000 # * 10^8 ( decimals)

    # when to start the crowdsale
    current_sale_start_block = 1

    # when to end the initial limited round
    current_sale_end_block = 1000
    
    def deploy_new_sts(self, project_id:str, owner:bytes, symbol:str):
        """Method to Deploy a new project Smart Token Share
        Args:
            project_id (str):
                ID for referencing the project
            owner (bytes):
                Script hash address of the token owner aka project address
            symbol (str):
                Symbol to represent Smart Token Share

        Return:
            (int): status code representing if execution was a success.
        """   
        storage = StorageManager()
        
        # Checks if project isnt saved already
        if storage.get_type('STS_symbol', project_id) != symbol:
            storage.put_type('STS_symbol', project_id, symbol)
            storage.put_type('STS_owner', project_id, owner)

            self.symbol = symbol
            self.project_id = project_id
            self.owner = owner

            return 1
        
        else:
            return 0    
    
    def get_project_info(self, project_id:str):
        """Method to pull and populate SmartTokenShare object
        Args:
            project_id (str):
                ID for referencing the project

        Return:
            (int): status code representing if execution was a success.
        """  
        # Pulling variables from contract storage
        storage = StorageManager()
        symbol = storage.get_type('STS_symbol', project_id)
        print('### symbol')
        print(symbol)
        print('symbol ###')

        # Will return with status code 0 if project doesnt exist.
        if symbol:
            print("made it!")
            owner = storage.get_type('STS_owner', project_id)
            current_sale_start_block = storage.get_type('STS_current_sale_start_block', project_id)
            current_sale_end_block = storage.get_type('STS_current_sale_end_block', project_id)
            current_supply = storage.get_type('STS_current_supply', project_id)
            current_tokens_per_gas = storage.get_type('STS_current_tokens_per_gas', project_id)

            # Updates STS object with values from contract storage
            self.symbol = symbol
            self.owner = owner
            self.project_id = project_id
            self.current_sale_start_block = current_sale_start_block
            self.current_sale_end_block = current_sale_end_block
            self.current_supply = current_supply
            self.current_tokens_per_gas =  current_tokens_per_gas

            return True
        
        return False
    
    def start_new_crowdfund(self, project_id:str, start_block:int, end_block:int, supply:int, tokens_per_gas:int):
        """Method to create a new crowdfund setting all necessary variables and storage values 
        Args:
            project_id (str):
                ID for referencing the project
            
            start_block (int):
                Block number that the sale will begin on
            
            end_block (int):
                Block number that the sale will end on
            
            supply (int):
                How many tokens will be avalible in the current sale, must input * 10^8

            tokens_per_gas (int):
                Token multiplier, tokens per gas sent                             
        Return:
            (int): status code representing if execution was a success.
        """  
        # Updating storage
        storage = StorageManager()        
        storage.put_type('STS_current_sale_start_block', project_id, start_block)
        storage.put_type('STS_current_sale_end_block', project_id, end_block)
        storage.put_type('STS_current_tokens_per_gas', project_id, tokens_per_gas)
        
        # Updating STS object
        self.current_sale_start_block = start_block
        self.current_sale_end_block = end_block
        self.current_tokens_per_gas = tokens_per_gas

        # Calculating current supply based on input supply and current tokens in circulation
        in_circulation = storage.get_type('STS_in_circulation', project_id)
        self.current_supply = in_circulation + supply
        
        # Updates current supply storage
        storage.put_type('STS_current_supply', project_id, self.current_supply)

        return 1

    def current_available_amount(self, project_id:str):
        """
        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The avaliable tokens for the current sale
        """
        # Gets the amount of tokens currently in circulation
        storage = StorageManager()
        in_circulation = storage.get_type('STS_in_circulation', project_id)

        # Gets the current supply ( not total supply )
        self.current_supply = storage.get_type('STS_current_supply', project_id)
       
        # Calculates the remaining avaliable supply by subtracting current circulation 
        # from current supply
        current_available = self.current_supply - in_circulation
        return current_available

    def total_available_amount(self, project_id:str):
        """
        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The avaliable tokens for the total project
        """
        # Gets the amount of tokens currently in circulation
        storage = StorageManager()
        in_circulation = storage.get_type('STS_in_circulation', project_id)

        # Calculates remaining avaliable supply by subtracting current circulation 
        # from total supply
        total_available = self.total_supply - in_circulation
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
        # Gets the amount of tokens currently in circulation
        storage = StorageManager()
        in_circulation = storage.get_type('STS_in_circulation', project_id)

        # Adds input amount to circulation
        in_circulation += amount

        # Puts updated circulation amount back to storage
        storage.put_type('STS_in_circulation', project_id, in_circulation)

    def get_circulation(self, project_id:str):
        """
        Get the total amount of tokens in circulation

        Args:
            project_id (str):
                ID for referencing the project
        Return:
            (int): The total amount of tokens in circulation
        """        
        # Gets the amount of tokens currently in circulation
        storage = StorageManager()
        return storage.get_type('STS_in_circulation', project_id)