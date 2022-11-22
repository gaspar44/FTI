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

class merkle_node():
    def __init__(self, transaction_hash, father=None, left=None, right=None):
        self.father = father
        self.left = left
        self.right = right
        self.transaction_hash = transaction_hash

def UAB_create_tree(tx_list):
    n = list(factor(len(tx_list)))[0][1]
    tree = []

    for i in range(n + 1):
        tree.append([])
    merkle_nodes = []
    for i in range(len(tx_list)):
        merkle = merkle_node(tx_list[i].transaction_hash)
        merkle_nodes.append(merkle)

    tree[n] = merkle_nodes

    for i in range(n, 0, -1):
        actual_level = tree[i]
        next_level = []

        for j in range(0, len(actual_level), 2):
            left_node = actual_level[j]
            right_node = actual_level[j + 1]

            concatenate_hash = UAB_concatenate_ints_as_strings([left_node.transaction_hash, right_node.transaction_hash])
            new_hash = UAB_btc_hash(concatenate_hash)

            merkle_father = merkle_node(new_hash, father=None, left=left_node, right=right_node)
            left_node.father, right_node.father = merkle_father, merkle_father

            next_level.append(merkle_father)

        tree[i - 1] = next_level

    return tree[0][0]


def UAB_validate_inclusion_simplified(tx, merkle_root, merkle_path):
    if len(merkle_path) == 0:
        return merkle_root == tx.transaction_hash

    start_node = merkle_node(tx.transaction_hash)

    for element in merkle_path:
        new_node = merkle_node(element[1])
        if element[0] == 0:
            message = UAB_btc_hash(UAB_concatenate_ints_as_strings([start_node.transaction_hash, new_node.transaction_hash]))
            parent_node = merkle_node(message, left=start_node, right=new_node)

        else:
            message = UAB_btc_hash(UAB_concatenate_ints_as_strings([new_node.transaction_hash, start_node.transaction_hash]))
            parent_node = merkle_node(message, left=new_node, right=start_node)

        start_node.father, new_node.father = parent_node, parent_node
        start_node = parent_node

    return start_node.transaction_hash == merkle_root
def UAB_compute_merkle_root(tx_list):
    actual_list = tx_list
    n = len(actual_list)
    if n == 0:
        return UAB_btc_hash("")

    elif n == 1:
        return tx_list[0].transaction_hash

    elif n & (n - 1) != 0:
        n = len(actual_list)
        while n & (n - 1) != 0:
            actual_list.append(actual_list[n - 1])
            n = len(actual_list)

    return UAB_create_tree(actual_list).transaction_hash

def test_case_1a(name, tx_list, exp_merkle):
    merkle = UAB_compute_merkle_root(tx_list)
    print("Test", name + ":", merkle == exp_merkle)

def test_case_1b(name, tx, merkle_root, merkle_path, exp_result):
    r = UAB_validate_inclusion_simplified(tx, merkle_root, merkle_path)
    print("Test", name + ":", r == exp_result)


tx1 = transaction_struct("1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464")
tx2 = transaction_struct("cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873")
tx3 = transaction_struct("6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b")
tx4 = transaction_struct("615bdd17c2556f82f384392ea8557f8cc88b03501c759e23093ab0b2a9b5cd48")
tx5 = transaction_struct("19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7")
tx6 = transaction_struct("d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35")
tx7 = transaction_struct("e5e0093f285a4fb94c3fcc2ad7fd04edd10d429ccda87a9aa5e4718efadf182e")
tx8 = transaction_struct("5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9")
tx9 = transaction_struct("03b26944890929ff751653acb2f2af795cee38f937f379f52ed654a68ce91216")
tx10 = transaction_struct("163f9d874bf45bcce929f64cc69e816219b0f000e374076c1d3efe0a26ca6b6e")

def first_case():
    exp_merkle = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    test_case_1a("1a.1", [], exp_merkle)

    exp_merkle = "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464"
    test_case_1a("1a.2", [tx1], exp_merkle)

    exp_merkle = "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d"
    test_case_1a("1a.3", [tx1, tx2], exp_merkle)

    exp_merkle = "1d61fc2b1cb988a0bddd5dc00f942e468c2957f8527a1189b79531b46680d852"
    test_case_1a("1a.4", [tx1, tx2, tx3, tx4], exp_merkle)

    exp_merkle = "a1095d369acb94778091ceccbb75719ae5f9941107d1f965174c6aebcb48d631"
    test_case_1a("1a.5", [tx1, tx2, tx3, tx4, tx5, tx6, tx7, tx8], exp_merkle)

    exp_merkle = "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317"
    test_case_1a("1a.6", [tx1, tx2, tx3], exp_merkle)

    exp_merkle = "9c7c326461af1854e747665a6c1657248c26cef66680301907952cc7aef43c7d"
    test_case_1a("1a.7", [tx1, tx2, tx3, tx4, tx5, tx6, tx7], exp_merkle)

    exp_merkle = "0e044c1cf28cb3361dacb8a55275f03963d9a210676e3cae337828751149e494"
    test_case_1a("1a.8", [tx1, tx2, tx3, tx4, tx5, tx6], exp_merkle)

    exp_merkle = "9bce55c90dbd3c65086549d556feea84f4b022a6e9d9d29824e3daf237656906"
    test_case_1a("1a.9", [tx1, tx2, tx3, tx4, tx5], exp_merkle)

def second_case():
    test_case_1b("1b.1", tx1, "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464", [], True)
    test_case_1b("1b.2", tx1, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873")], True)
    test_case_1b("1b.3", tx2, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d",
                 [(1, "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464")], True)
    test_case_1b("1b.4", tx1, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873"),
                  (0, "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")], True)
    test_case_1b("1b.5", tx3, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317",
                 [(0, "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"),
                  (1, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d")], True)
    test_case_1b("1b.6", tx6, "a1095d369acb94778091ceccbb75719ae5f9941107d1f965174c6aebcb48d631",
                 [(1, "19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7"),
                  (0, "96511d2d18696af94fc302da346d749fbbd99181c0dbe668a57f2fe92f18d580"),
                  (1, "1d61fc2b1cb988a0bddd5dc00f942e468c2957f8527a1189b79531b46680d852")], True)
    test_case_1b("1b.7", tx1, "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c474", [], False)
    test_case_1b("1b.8", tx1, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d",
                 [(1, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873")], False)
    test_case_1b("1b.9", tx1, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef3653125",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873")], False)
    test_case_1b("1b.10", tx2, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365312d",
                 [(0, "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464")], False)
    test_case_1b("1b.11", tx2, "ad3ee4ac443155d71fa2cd251075c50dda10a3991ffea21ea264400ef365313d",
                 [(1, "1bad6b8cf97131fceab8543e81f7757195fbb1d36b376ee994ad1cf17699c464")], False)
    test_case_1b("1b.12", tx1, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317",
                 [(1, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873"),
                  (0, "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")], False)
    test_case_1b("1b.13", tx1, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb874"),
                  (0, "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")], False)
    test_case_1b("1b.14", tx1, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a317",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873"),
                  (0, "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a370d")], False)
    test_case_1b("1b.15", tx1, "33bbe18031d03aa444e5ce1426d8a992e83210d77af4fec16ef32e779987a417",
                 [(0, "cf3bae39dd692048a8bf961182e6a34dfd323eeb0748e162eaf055107f1cb873"),
                  (0, "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")], False)