from hashlib import sha256 as hash_alg
from datetime import datetime

now = datetime.now

class Block:
    def __init__(self, timestamp, index=0, data=0x0, prev_hash=0x0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
    
    @property
    def hash(self):
        _raw_blk = str(self.index)
        _raw_blk += str(self.timestamp)
        _raw_blk += str(self.data)
        _raw_blk += str(self.prev_hash)
        _hash = hash_alg()
        _hash.update(_raw_blk.encode('utf-8'))
        return _hash.hexdigest()

    def __repr__(self):
        return '''
Block {0}:
    Timestamp: {1}
    Previous Hash: 0x{3}
    Data: {2}
'''.format(self.index, self.timestamp, self.data, self.prev_hash)

class Chain:
    def __init__(self):
        self.chain = [Block(now())]

    def add_block(self, data):
        prev_blk = self.chain[-1]
        next_blk = Block(
                now(), 
                index=prev_blk.index+1, 
                prev_hash=prev_blk.hash, 
                data=data
            )
        self.chain.append(next_blk)

if __name__ == '__main__':
    c = Chain()
    for i in range(20):
        c.add_block('Adding block {}'.format(i+1))
        print("New Block", c.chain[-1])
