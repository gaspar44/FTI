from sage.all import *

MAX_TARGET = "F" * 64


# Get a hex string with the SHA256 sum of the message
def UAB_btc_hash(message):
    import hashlib
    return hashlib.sha256(message.encode('utf-8')).hexdigest()


# Convert a hex string to an integer value
def UAB_hexString_to_int(hexString):
    return int(hexString, base=16)


# Returns the string concatenation of the integers in list
def UAB_concatenate_ints_as_strings(list):
    return "".join(str(e) for e in list)


#########################################################################################
#
# DATA STRUCTURES
#
#########################################################################################

# Transaction structure
class transaction_struct():

    # Initialize
    def __init__(self, h=None):
        if h:
            self.transaction_hash = h
        else:
            self.transaction_hash = UAB_btc_hash(str(ZZ.random_element()))

    # Show transaction content
    def print_me(self):
        print("Transaction")
        print("  transaction_hash:", self.transaction_hash)

    # Serialize transaction structure
    def serialize(self):
        return UAB_concatenate_ints_as_strings([self.transaction_hash])

    # Get transaction hash
    def get_hash(self):
        return self.transaction_hash


# Block header structure
class block_header_struct():

    # Initialize
    def __init__(self):
        self.version = 2
        self.previous_block_hash = None
        self.merkle_root = None
        self.time = None
        self.target = None
        self.nonce = None

    # Show block header content
    def print_me(self):
        print("Block header")
        print("  version:", self.version)
        print("  previous_block_hash:", self.previous_block_hash)
        print("  merkle_root:", self.merkle_root)
        print("  time:", self.time)
        print("  target:", self.target)
        print("  nonce:", self.nonce)

    # Serialize block header
    def serialize(self):
        s = [self.version, self.previous_block_hash, self.merkle_root, self.time, self.target, self.nonce]
        return UAB_concatenate_ints_as_strings(s)


# Block structure
class block_struct():

    # Initialize
    def __init__(self):
        self.block_header = None
        self.txs = []

    # Show block content
    def print_me(self):
        print("Block")
        print("  block_header:", )
        self.block_header.print_me()
        print("  txs:", [tx.get_hash() for tx in self.txs])

    # Serialize block
    def serialize(self):
        s = [self.block_header, self.txs]
        return UAB_concatenate_ints_as_strings(s)

    # Get block hash
    def get_hash(self):
        return UAB_btc_hash(self.block_header.serialize())


# Blockchain structure
class blockchain_struct():

    # Initialize
    def __init__(self):
        self.blocks = []

    # Show blockchain content
    def print_me(self):
        for block in self.blocks:
            block.print_me()

    # Add a new block to the blockchain
    def add_block(self, block):
        self.blocks.append(block)

    # Get block list
    def get_blocks(self):
        return self.blocks

def UAB_compute_merkle_root(tx_list):
    n = len(tx_list)
    if n == 0:
        return transaction_struct(UAB_btc_hash(""))

    elif n & (n - 1) != 0:
        print("verga")

    for i in range(pow(2, len(tx_list)) - 1):
        print(i)