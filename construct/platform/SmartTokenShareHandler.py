from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

OnTransfer = RegisterAction('transfer', 'project_id', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve','project_id', 'addr_from', 'addr_to', 'amount')


class SmartTokenShareHandler():
    """
    Based off the NEP5 Handler. The SmartTokenShareHandler handles the transfering of STS's
    """ 

    def get_methods(self):

        methods = ['symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
        return methods

    def handle_sts(self, operation, args):
        sts = SmartTokenShare()

        # project_id always first arg
        project_id = args[0]
        
        storage = StorageManager()
        arg_error = 'Incorrect Arg Length'
        
        if operation == 'decimals':
            sts_info = sts.get_info(project_id)
            decimals = sts_info[sts.decimals_idx]
            return decimals

        elif operation == 'symbol':
            sts_info = sts.get_info(project_id)
            symbol = sts_info[sts.symbol_idx]
            return symbol

        elif operation == 'totalSupply':
            sts_info = sts.get_info(project_id)
            total_supply = sts_info[sts.total_supply_idx]
            return total_supply

        elif operation == 'balanceOf':
            if len(args) == 2:
                account = args[1]
                return storage.get_double(project_id, account)
            return arg_error

        elif operation == 'transfer':
            if len(args) == 4:
                t_from = args[1]
                t_to = args[2]
                t_amount = args[3]
                return self.do_transfer(project_id, t_from, t_to, t_amount)
            return arg_error

        elif operation == 'transferFrom':
            if len(args) == 4:
                t_from = args[1]
                t_to = args[2]
                t_amount = args[3]
                return self.do_transfer_from(project_id, t_from, t_to, t_amount)
            return arg_error

        elif operation == 'approve':
            if len(args) == 4:
                t_owner = args[1]
                t_spender = args[2]
                t_amount = args[3]
                return self.do_approve(project_id, t_owner, t_spender, t_amount)
            return arg_error

        elif operation == 'allowance':
            if len(args) == 3:
                t_owner = args[1]
                t_spender = args[2]
                return self.do_allowance(project_id, t_owner, t_spender)

            return arg_error

        return False

    def do_transfer(self, project_id, t_from, t_to, amount):
        storage = StorageManager()

        # Pointless
        if amount <= 0:
            return False

        # Validate address
        if CheckWitness(t_from):
            
            # Pointless
            if t_from == t_to:
                print("transfer to self!")
                return True
            
            from_val = storage.get_double(project_id, t_from)

            if from_val < amount:
                print("insufficient funds")
                return False

            if from_val == amount:
                storage.delete_double(project_id, t_from)

            else:
                difference = from_val - amount
                storage.put_double(project_id, t_from, difference)

            to_value = storage.get_double(project_id, t_to)

            to_total = to_value + amount

            storage.put_double(project_id, t_to, to_total)

            OnTransfer(project_id, t_from, t_to, amount)

            return True
        else:
            print("from address is not the tx sender")

        return False
    
    def do_transfer_from(self, project_id, t_from, t_to, amount):
        
        storage = StorageManager()
        if amount <= 0:
            return False

        available_key = concat(t_from, t_to)

        available_to_to_addr = storage.get_double(project_id, available_key)

        if available_to_to_addr < amount:
            print("Insufficient funds approved")
            return False

        from_balance = storage.get_double(project_id, t_from)

        if from_balance < amount:
            print("Insufficient tokens in from balance")
            return False

        to_balance = storage.get_double(project_id, t_to)

        new_from_balance = from_balance - amount

        new_to_balance = to_balance + amount

        storage.put_double(project_id, t_to, new_to_balance)
        storage.put_double(project_id, t_from, new_from_balance)

        print("transfer complete")

        new_allowance = available_to_to_addr - amount

        if new_allowance == 0:
            print("removing all balance")
            storage.delete_double(project_id, available_key)
        else:
            print("updating allowance to new allowance")
            storage.put_double(project_id, available_key, new_allowance)

        OnTransfer(project_id, t_from, t_to, amount)

        return True

    # Owner approves amount allowance to spender
    def do_approve(self, project_id, t_owner, t_spender, amount):
        storage = StorageManager()

        if not CheckWitness(t_owner):
            print("Incorrect permission")
            return False

        from_balance = storage.get_double(project_id, t_owner)

        # cannot approve an amount that is
        # currently greater than the from balance
        if from_balance >= amount:

            approval_key = concat(t_owner, t_spender)

            current_approved_balance = storage.get_double(project_id, approval_key)

            new_approved_balance = current_approved_balance + amount

            storage.put_double(project_id, approval_key, new_approved_balance)

            OnApprove(project_id, t_owner, t_spender, amount)

            return True

        return False

    def do_allowance(self, project_id, t_owner, t_spender):
        storage = StorageManager()

        allowance_key = concat(t_owner, t_spender)

        amount = storage.get_double(project_id, allowance_key)

        return amount
