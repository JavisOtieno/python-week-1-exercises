import random
import string
from typing import Union, Tuple, List, Dict

# Name Assignment (variables and constants)
MINING_REWARD = 3.125                    # Current Bitcoin block reward (post-2024 halving)
current_block_height = 850000            # Approximate current block height as of 2026
BTC_TO_SATS = 100_000_000                # 1 BTC = 100,000,000 satoshis


# Functions
def calculate_total_reward(blocks_mined) -> int:
    """Calculate the total Bitcoin reward for a given number of mined blocks."""
    return blocks_mined * MINING_REWARD


def is_valid_tx_fee(fee):
    """Return True if the transaction fee is within an acceptable range."""
    return 0.00001 <= fee <= 0.01


def is_large_balance(balance):
    """Determine if a wallet balance is considered large."""
    return balance > 50.0


def tx_priority(size_bytes, fee_btc):
    """Return the priority of a transaction based on fee rate."""
    if size_bytes == 0:
        return 'low'
    fee_rate = fee_btc / size_bytes
    
    if fee_rate >= 0.00005:
        return 'high'
    elif fee_rate >= 0.00001:
        return 'medium'
    else:
        return 'low'


def is_mainnet(network):
    """Check if the network is for Bitcoin mainnet."""
    return network.lower() == "mainnet"


def is_in_range(value):
    """Check if a value is within the range 100 to 200 (inclusive)."""
    return 100 <= value <= 200


def is_same_wallet(wallet1, wallet2):
    """Check if two wallet objects are the same in memory."""
    return wallet1 is wallet2


def normalize_address(address):
    """Normalize a Bitcoin address by stripping whitespace and converting to lowercase."""
    return address.strip().lower()


def add_utxo(utxos, new_utxo):
    """Add a new UTXO to the list of UTXOs."""
    utxos.append(new_utxo)
    return utxos


def find_high_fee(fee_list):
    """Find the first transaction with a fee greater than 0.005 BTC."""
    for index, fee in enumerate(fee_list):
        if fee > 0.005:
            return (index, fee)
    return None


def get_wallet_details():
    """Return basic wallet details as a tuple."""
    return ("satoshi_wallet", 50.0)


def get_tx_status(tx_pool, txid):
    """Get the status of a transaction from the mempool."""
    return tx_pool.get(txid, 'not found')


def unpack_wallet_info(wallet_info):
    """Unpack wallet information from a tuple and return a formatted string."""
    name, balance = wallet_info
    return f"Wallet {name} has balance: {balance} BTC"


def calculate_sats(btc: float) -> int:
    """Convert BTC to satoshis."""
    return int(btc * BTC_TO_SATS)


def generate_address(prefix: str = "bc1q") -> str:
    """Generate a mock Bitcoin address with given prefix."""
    suffix_length = 32 - len(prefix)
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
    return prefix + suffix


def validate_block_height(height: Union[int, float, str]) -> Tuple[bool, str]:
    """Validate a Bitcoin block height."""
    # Only accept actual integers or integer-like floats.
    # Reject strings entirely (as per current test expectation)
    if isinstance(height, str):
        return False, "Block height must be an integer"
    
    try:
        # Check for non-integer floats (like 123.5)
        if isinstance(height, float) and not height.is_integer():
            return False, "Block height must be an integer"
        
        height = int(height)
    except (ValueError, TypeError):
        return False, "Block height must be an integer"
    
    if height < 0:
        return False, "Block height cannot be negative"
    if height > 800000:
        return False, "Block height seems unrealistic"
    
    return True, "Valid block height"


def halving_schedule(blocks: List[int]) -> Dict[int, int]:
    """Calculate block reward for given block heights based on halving schedule."""
    base_reward = 5_000_000_000   # 50 BTC in satoshis (FIXED)
    halving_interval = 210_000
    
    result = {}
    for block in blocks:
        halvings = block // halving_interval
        reward = base_reward >> halvings   # Right shift = divide by 2^halvings
        result[block] = reward
    return result


def find_utxo_with_min_value(utxos: List[Dict[str, int]], target: int) -> Dict[str, int]:
    """Find the UTXO with minimum value that meets or exceeds target."""
    candidates = [u for u in utxos if u.get('value', 0) >= target]
    if not candidates:
        return {}
    return min(candidates, key=lambda u: u['value'])


def create_utxo(txid: str, vout: int, **kwargs) -> Dict[str, Union[str, int]]:
    """Create a UTXO dictionary with optional additional fields."""
    utxo = {"txid": txid, "vout": vout}
    utxo.update(kwargs)
    return utxo