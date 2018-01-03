contract Consulting
{
    // Providing services
    address consultant;
    // Paying for services rendered
    address recipient;

    // Duration of services
    uint duration;
    // Time between payouts
    uint payoutPeriod;
    // ether/block payrate
    uint rate;
    // Amount of services
    uint amount;

    // sha256 Hash of the terms of the agreement
    bytes32 termsHash;

    function Consulting(address _recipient,
                        uint _duration,
                        ether _rate,
                        uint _payoutPeriod,
                        bytes32 _termsHash)
        public
    {
        consultant = msg.sender;
        recipient = _recipient;
        duration = _duration;
        rate = _rate;
        amount = duration * rate;
        payoutPeriod = _payoutPeriod;
        termsHash = _termsHash;
    }

    function acceptContract()
        onlyRecipient()
        payable
    {
        require(msg.sender == recipient);
        require(msg.value >= amount);
        lastPayout = block.timestamp;
        uint256 refund = msg.value - amount;
        recipient.transfer(refund);
    }

    function getPayout()
    {
        require(msg.sender == consultant);
        require(block.timestamp >= lastPayout + payoutPeriod);
        uint256 payout = rate * (block.timestamp - lastPayout);
        lastPayout = block.timestamp;
        consultant.transfer(payout);
    }

    // Cancel at any time
    function cancelContract()
    {
        require(msg.sender == consultant
             || msg.sender == recipient);
        // Pay half of services rendered
        uint256 payout = rate * (block.timestamp - lastPayout);
        consultant.transfer(payout/2);
        selfdestruct(recipient);
    }
}
