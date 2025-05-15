import requests
import base64

def get_virtual_token_reserves(bonding_curve_account: str, rpc_url: str = "https://api.mainnet-beta.solana.com"):
    """
    Fetches and returns the virtual token reserves from a Solana bonding curve account.
    
    Args:
        bonding_curve_account (str): The address of the bonding curve account
        rpc_url (str): Solana RPC URL
        
    Returns:
        int: The virtual token reserves value
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            bonding_curve_account,
            {"encoding": "base64"}
        ]
    }
    
    response = requests.post(rpc_url, json=payload)
    if not response.json().get('result'):
        raise Exception("Account data not found!")
    
    data = response.json()['result']['value']['data'][0]
    account_data = base64.b64decode(data)

    virtual_token_reserves = int.from_bytes(account_data[8:16], byteorder='little')
    
    return virtual_token_reserves

def calculate_bonding_curve_progress(bonding_curve_account: str):
    """
    Calculate the bonding curve progress based on virtual token reserves.
    
    Args:
        virtual_token_reserves: Current virtual token reserves
        
    Returns:
        float: Progress percentage
    """
    INITIAL_VIRTUAL_RESERVES = 1_073_000_000 * (10**6)
    TOTAL_TOKENS_TO_COLLECT = 793_100_000 * (10**6)
    
    numerator = INITIAL_VIRTUAL_RESERVES - get_virtual_token_reserves(bonding_curve_account)
    progress = (numerator * 100) / TOTAL_TOKENS_TO_COLLECT
    
    return progress
