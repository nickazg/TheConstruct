from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.blockchain.vm.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetInputs, GetUnspentCoins
from boa.blockchain.vm.Neo.Blockchain import GetTransaction
from boa.blockchain.vm.Neo.Output import GetValue, GetAssetId, GetScriptHash
from boa.blockchain.vm.Neo.Input import GetHash, GetIndex

class Attachments():
    """
    Container object ( struct ) for passing around information about attached neo and gas
    """
    neo_attached = 0

    gas_attached = 0

    neo_attached_recieved = 0

    gas_attached_recieved = 0

    sender_addr = 0

    receiver_addr = 0

    neo_asset_id = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'

    gas_asset_id = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'

    unspent_coins = 0



def get_asset_attachments() -> Attachments:
    """
    Gets information about NEO and Gas attached to an invocation TX

    :return:
        Attachments: An object with information about attached neo and gas
    """
    attachment = Attachments()

    tx = GetScriptContainer()  # type:Transaction
    references = tx.References

    attachment.receiver_addr = GetExecutingScriptHash()

    if len(references) > 0:

        reference = references[0]
        attachment.sender_addr = reference.ScriptHash

        sent_amount_neo = 0
        sent_amount_gas = 0

        recieved_amount_neo = 0
        recieved_amount_gas = 0

        for output in tx.Outputs:
            if output.ScriptHash == attachment.receiver_addr and output.AssetId == attachment.neo_asset_id:
                sent_amount_neo += output.Value

            if output.ScriptHash == attachment.receiver_addr and output.AssetId == attachment.gas_asset_id:
                sent_amount_gas += output.Value

            if output.ScriptHash == attachment.sender_addr and output.AssetId == attachment.neo_asset_id:
                recieved_amount_neo += output.Value

            if output.ScriptHash == attachment.sender_addr and output.AssetId == attachment.gas_asset_id:
                recieved_amount_gas += output.Value

        
        attachment.neo_attached = sent_amount_neo
        attachment.gas_attached = sent_amount_gas


        attachment.neo_attached_recieved = recieved_amount_neo
        attachment.gas_attached_recieved = recieved_amount_gas

    return attachment

# def get_prev_tx() -> Transaction:
#     tx = GetScriptContainer()  # type:Transaction

#     input = tx.Inputs[0]
    
    
#     input.PrevHash
#     input.PrevIndex

#     prev_tx = GetTransaction(input.PrevHash)

#     return prev_tx

def get_asset_attachments_for_prev() -> Attachments:
    attachment = Attachments()

    tx = GetScriptContainer()  # type:Transaction
    

    sent_amount_neo = 0
    sent_amount_gas = 0

    attachment.receiver_addr = GetExecutingScriptHash()

    for input in tx.Inputs:

        prev_tx = GetTransaction(input.Hash)
        references = prev_tx.References

        if len(references) > 0:

            reference = references[0]
            sender_addr = reference.ScriptHash

            prev_output = prev_tx.Outputs[input.Index]
            
            if prev_output.ScriptHash == attachment.receiver_addr and prev_output.AssetId == attachment.neo_asset_id:
                sent_amount_neo += prev_output.Value

            if prev_output.ScriptHash == attachment.receiver_addr and prev_output.AssetId == attachment.gas_asset_id:
                sent_amount_gas += prev_output.Value

        
    attachment.neo_attached = sent_amount_neo
    attachment.gas_attached = sent_amount_gas

    return attachment