from construct.common.StorageManager import StorageManager

class SmartTokenShare():
    """
    A Template for a Smart Token Share (STS), managing STS info. Based on NEP5 token, however all values 
    are stored in the contract storage.
    """
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

    def start_new_crowdfund(self, project_id, funding_stage_id, start_block, end_block, supply, tokens_per_gas):
        """
        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
                
            start_block (int):
                Block to start fund

            end_block (int):
                Block to end fund

            supply (int):
                Supply of the token in this crowdfund

            tokens_per_gas (int):
                Token to gas ratio
        Return:
            (None): 
        """
        storage = StorageManager()
        
        # Default circulation
        in_circulation = 0
        
         # Info structure
        crowdfund_info = [start_block, end_block, supply, tokens_per_gas, in_circulation]

        # Saving info to storage
        crowdfund_info_serialized = storage.serialize_array(crowdfund_info)
        storage.put_triple('STS', project_id, funding_stage_id, crowdfund_info_serialized)

    def crowdfund_available_amount(self, project_id, funding_stage_id):
        """
        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
        Return:
            (int): The avaliable tokens for the current sale
        """
        storage = StorageManager()
        
        # Pull Crowdfund info
        crowdfund_info_serialized = storage.get_triple('STS', project_id, funding_stage_id)
        crowdfund_info = storage.deserialize_bytearray(crowdfund_info_serialized)

        # Crowdfund vars
        in_circulation = crowdfund_info[4]
        supply = crowdfund_info[2]

        available = supply - in_circulation

        return available

    def add_to_crowdfund_circulation(self, project_id, funding_stage_id, amount):
        """
        Adds an amount of token to circlulation

        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage

            amount (int):
                amount of tokens added  
        """
        storage = StorageManager()
        
        # Pull Crowdfund info
        crowdfund_info_serialized = storage.get_triple('STS', project_id, funding_stage_id)
        crowdfund_info = storage.deserialize_bytearray(crowdfund_info_serialized)

        # info into vars
        start_block = crowdfund_info[0]
        end_block = crowdfund_info[1]
        supply = crowdfund_info[2]
        tokens_per_gas = crowdfund_info[3]
        in_circulation = crowdfund_info[4]

        # Calculation
        updated_in_circulation = in_circulation + amount

        # output STS info
        updated_crowdfund_info = [start_block, end_block, supply, tokens_per_gas, updated_in_circulation]
        
        # Save STS info
        updated_crowdfund_info_serialized = storage.serialize_array(updated_crowdfund_info)
        storage.put_triple('STS', project_id, funding_stage_id, updated_crowdfund_info_serialized)    

    def get_crowdfund_circulation(self, project_id, funding_stage_id):
        """
        Get the total amount of tokens in circulation

        Args:
            project_id (str):
                ID for referencing the project

            funding_stage_id (str):
                ID for referencing the funding stage
        Return:
            (int): The total amount of tokens in circulation
        """        
        storage = StorageManager()
        
        # Pull Crowdfund info
        crowdfund_info_serialized = storage.get_triple('STS', project_id, funding_stage_id)
        crowdfund_info = storage.deserialize_bytearray(crowdfund_info_serialized)

        # in_circulation var
        in_circulation = crowdfund_info[4]

        return in_circulation

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
        updated_sts_info_serialized = storage.serialize_array(sts_info)
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