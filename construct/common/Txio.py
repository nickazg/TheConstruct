from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetInputs, GetUnspentCoins
from boa.interop.Neo.Blockchain import GetTransaction
from boa.interop.Neo.Output import GetValue, GetAssetId, GetScriptHash
from boa.interop.Neo.Input import GetIndex

ATTACHMENTS = {}
ATTACHMENTS['neo_attached'] = 0
ATTACHMENTS['gas_attached'] = 0
ATTACHMENTS['neo_attached_recieved'] = 0
ATTACHMENTS['gas_attached_recieved'] = 0
ATTACHMENTS['sender_addr'] = 0
ATTACHMENTS['receiver_addr'] = 0
ATTACHMENTS['neo_asset_id'] = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
ATTACHMENTS['gas_asset_id'] = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'
ATTACHMENTS['unspent_coins'] = 0

def get_asset_attachments():
    """
    Gets information about NEO and Gas attached to an invocation TX

    :return:
        Attachments: An object with information about attached neo and gas
    """
    tx = GetScriptContainer()  # type:Transaction
    references = tx.References

    ATTACHMENTS['receiver_addr'] = GetExecutingScriptHash()

    if len(references) > 0:

        reference = references[0]
        ATTACHMENTS['sender_addr'] = reference.ScriptHash

        sent_amount_neo = 0
        sent_amount_gas = 0

        recieved_amount_neo = 0
        recieved_amount_gas = 0

        for output in tx.Outputs:
            if output.ScriptHash == ATTACHMENTS['receiver_addr'] and output.AssetId == ATTACHMENTS['neo_asset_id']:
                sent_amount_neo += output.Value

            if output.ScriptHash == ATTACHMENTS['receiver_addr'] and output.AssetId == ATTACHMENTS['gas_asset_id']:
                sent_amount_gas += output.Value

            if output.ScriptHash == ATTACHMENTS['sender_addr'] and output.AssetId == ATTACHMENTS['neo_asset_id']:
                recieved_amount_neo += output.Value

            if output.ScriptHash == ATTACHMENTS['sender_addr'] and output.AssetId == ATTACHMENTS['gas_asset_id']:
                recieved_amount_gas += output.Value

        
        ATTACHMENTS['neo_attached'] = sent_amount_neo
        ATTACHMENTS['gas_attached'] = sent_amount_gas


        ATTACHMENTS['neo_attached_recieved'] = recieved_amount_neo
        ATTACHMENTS['gas_attached_recieved'] = recieved_amount_gas

    return ATTACHMENTS

def get_asset_attachments_for_prev():
    tx = GetScriptContainer()  # type:Transaction
    

    sent_amount_neo = 0
    sent_amount_gas = 0

    ATTACHMENTS['receiver_addr'] = GetExecutingScriptHash()

    for input in tx.Inputs:

        prev_tx = GetTransaction(input.Hash)
        references = prev_tx.References

        if references:

            # reference = references[0]
            # sender_addr = reference.ScriptHash

            prev_output = prev_tx.Outputs[input.Index]
            
            if prev_output.ScriptHash == ATTACHMENTS['receiver_addr'] and prev_output.AssetId == ATTACHMENTS['neo_asset_id']:
                sent_amount_neo += prev_output.Value

            if prev_output.ScriptHash == ATTACHMENTS['receiver_addr'] and prev_output.AssetId == ATTACHMENTS['gas_asset_id']:
                sent_amount_gas += prev_output.Value

        
    ATTACHMENTS['neo_attached'] = sent_amount_neo
    ATTACHMENTS['gas_attached'] = sent_amount_gas

    return ATTACHMENTS