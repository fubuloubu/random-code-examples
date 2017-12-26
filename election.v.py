# reigstration_hash is hash of externally-verified information managed by a trusted party
# type is sha3 (max sha3 length is 64 bytes)
voter_registration: {registration_hash: bytes <= 64, votes: num}[address]

# List of valid positions (up to 20)
positions: public( bytes32[20] )

# person (address) -> position map
# Position is ASCII string of 32 bytes max length
ballot_options: public( {registration_hash: bytes <= 64, position: bytes32}[address] )

# Ballots mapped to list of addresses on ballot -> votes
votes: num[address]

# Administrator of poll
admin: public( address )

# Poll duration
duration: public( timedelta )

# Keep track of polling state
poll_open: public( bool )
poll_closing_time: public( timestamp )

def __init__(poll_admin: address, _duration: timedelta, _positions: bytes32[20]):
    self.admin = poll_admin
    self.duration = _duration
    self.poll_open = False
    self.poll_closing_time = block.timestamp # Prevents voting until updated
    self.positions = _positions

# Admin can add ballot options
def register_ballot_option(candidate: address, _hash: bytes <= 64, _position: bytes32):
    assert msg.sender == self.admin

    # Candidate can only be on ballot once
    assert not self.ballot_options[candidate]
    # Position must be in list of positions
    exists = False
    for i in range(self.positions, self.positions + 20):
        exists = _position == self.positions[i]
        if exists:
            break
    assert exists
    
    # Register
    self.ballot_options[candidate] = {registration_hash: _hash, position: _position}

def register_voter(_hash: bytes <= 64 ):
    # Polls can not be open
    assert not self.poll_open
    # Can only register once
    assert not self.voter_registration[msg.sender]

    # Only 1 vote here, but allows weighted voting
    # (Override this function and set self.voter_registration with your own data)
    self.voter_registration[msg.sender] = {registration_hash: _hash, votes: 1}

def delegate(_delegate: address):
    # Polls can not be open
    assert not self.poll_open
    # Both delegate and voter must be registered
    assert self.voter_registration[_delegate]
    assert self.voter_registration[msg.sender]
    
    # Delegate gets voters votes
    self.voter_registration[_delegate].votes += \
            self.voter_registration[msg.sender].votes
    self.voter_registration[msg.sender].votes = 0

def start_poll():
    assert msg.sender == self.admin
    
    # Open the poll and set the closing time from that block
    self.poll_open = True
    self.poll_closing_time = block.timestamp + self.duration

def vote(position: bytes32, choice: address):
    # Polls must be open
    # (Check that both the poll_admin opened it and the duration has not expired)
    assert self.poll_open and block.timestamp < self.poll_closing_time
    # Voter must be registered
    assert self.voter_registration[msg.sender]
    # Ballot option must be valid
    assert position == self.ballot_options[choice].position
    
    # Ensure the voted choice exists in votes array
    if not self.votes[choice]:
        self.votes[choice] = 0
    # Add ballot to list of votes
    self.votes[choice] += self.voter_registration[msg.sender].votes

def close_poll():
    assert msg.sender == self.admin
    # Can only close the poll once openned and the duration has expired
    assert self.poll_open and block.timestamp >= self.poll_closing_time

    # Donations appreciated
    selfdestruct(msg.sender)
