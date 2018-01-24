from boa.blockchain.vm.Neo.Runtime import CheckWitness, Notify
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.code.builtins import concat

from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

OnTransfer = RegisterAction('project_id', 'transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('project_id', 'approve', 'addr_from', 'addr_to', 'amount')


class SmartTokenShareHandler():
    """
    Based off the NEP5 Handler, the SmartTokenShareHandler handles the transfering of STS's 
    """ 
    project_id = ''

    def get_methods(self):

        method = ['project_id', 'symbol', 'decimals', 'totalSupply', 'currentSupply', 'balanceOf','transfer', 'transferFrom', 'approve', 'allowance']
        return method

    def handle_sts(self, operation, args, sts: SmartTokenShare):
        # project_id always first arg
        self.project_id = args[0]
        
        storage = StorageManager()
        arg_error = 'Incorrect Arg Length'
        
        if operation == 'decimals':
            return sts.decimals

        elif operation == 'symbol':
            return sts.symbol

        elif operation == 'totalSupply':
            return sts.total_supply

        elif operation == 'currentSupply':
            return sts.current_supply

        elif operation == 'balanceOf':
            if len(args) == 2:
                account = args[1]
                return storage.get_type(self.project_id, account)
            return arg_error

        elif operation == 'transfer':
            if len(args) == 4:
                t_from = args[1]
                t_to = args[2]
                t_amount = args[3]
                return self.do_transfer(storage, t_from, t_to, t_amount)
            return arg_error

        elif operation == 'transferFrom':
            if len(args) == 4:
                t_from = args[1]
                t_to = args[2]
                t_amount = args[3]
                return self.do_transfer_from(storage, t_from, t_to, t_amount)
            return arg_error

        elif operation == 'approve':
            if len(args) == 4:
                t_owner = args[1]
                t_spender = args[2]
                t_amount = args[3]
                return self.do_approve(storage, t_owner, t_spender, t_amount)
            return arg_error

        elif operation == 'allowance':
            if len(args) == 3:
                t_owner = args[1]
                t_spender = args[2]
                return self.do_allowance(storage, t_owner, t_spender)

            return arg_error

        return False

    def do_transfer(self, storage: StorageManager, t_from, t_to, amount):

        if amount <= 0:
            return False

        if CheckWitness(t_from):

            if t_from == t_to:
                print("transfer to self!")
                return True

            from_val = storage.get_type(self.project_id, t_from)

            if from_val < amount:
                print("insufficient funds")
                return False

            if from_val == amount:
                storage.delete_type(self.project_id, t_from)

            else:
                difference = from_val - amount
                storage.put_type(self.project_id, t_from, difference)

            to_value = storage.get_type(self.project_id, t_to)

            to_total = to_value + amount

            storage.put_type(self.project_id, t_to, to_total)

            OnTransfer(self.project_id, t_from, t_to, amount)

            return True
        else:
            print("from address is not the tx sender")

        return False
    
    def do_transfer_from(self, storage: StorageManager, t_from, t_to, amount):

        if amount <= 0:
            return False

        available_key = concat(t_from, t_to)

        available_to_to_addr = storage.get_type(self.project_id, available_key)

        if available_to_to_addr < amount:
            print("Insufficient funds approved")
            return False

        from_balance = storage.get_type(self.project_id, t_from)

        if from_balance < amount:
            print("Insufficient tokens in from balance")
            return False

        to_balance = storage.get_type(self.project_id, t_to)

        new_from_balance = from_balance - amount

        new_to_balance = to_balance + amount

        storage.put_type(self.project_id, t_to, new_to_balance)
        storage.put_type(self.project_id, t_from, new_from_balance)

        print("transfer complete")

        new_allowance = available_to_to_addr - amount

        if new_allowance == 0:
            print("removing all balance")
            storage.delete_type(self.project_id, available_key)
        else:
            print("updating allowance to new allowance")
            storage.put_type(self.project_id, available_key, new_allowance)

        OnTransfer(self.project_id, t_from, t_to, amount)

        return True

    def do_approve(self, storage: StorageManager, t_owner, t_spender, amount):

        if not CheckWitness(t_owner):
            print("Incorrect permission")
            return False

        from_balance = storage.get_type(self.project_id, t_owner)

        # cannot approve an amount that is
        # currently greater than the from balance
        if from_balance >= amount:

            approval_key = concat(t_owner, t_spender)

            current_approved_balance = storage.get_type(self.project_id, approval_key)

            new_approved_balance = current_approved_balance + amount

            storage.put_type(self.project_id, approval_key, new_approved_balance)

            OnApprove(self.project_id, t_owner, t_spender, amount)

            return True

        return False

    def do_allowance(self, storage: StorageManager, t_owner, t_spender):

        allowance_key = concat(t_owner, t_spender)

        amount = storage.get_type(self.project_id, allowance_key)

        return amount
