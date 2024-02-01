// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./GNE.sol";

contract CertificateBridge is ERC1155, Ownable, ChainlinkClient {
    using Chainlink for Chainlink.Request;

    address private GNEAddress;
    GNE private GNEInstance;

    uint32 tokenId;
    uint32 tokenData;

    constructor(address GNEAddress) ERC1155("CO2") {
        GNEAddress = GNEAddress;
        GNEInstance = GNE(GNEAddress);

        // We want to do http get request to the api https://arvan.nparsa.ir/credittotoken/TOKEN_ID
        setChainlinkToken(0xa36085F69e2889c224210F603D836748e7dC0088); // Kovan LINK token
        setChainlinkOracle(0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8); // Kovan LINK oracle
        setJobId("6d1bfe27e7034b1d87b5270556b17277"); // Kovan job id
    }

    function mint(address account, uint256 id) public onlyOwner {
        _mint(account, id, 1, "");
    }

    function burn(address account, uint256 id) public onlyOwner {
        _burn(account, id, 1);
    }

    function updateCredit(uint256 tokenId) public {
        // We want to do http get request to the api https://arvan.nparsa.ir/credittotoken/TOKEN_ID
        Chainlink.Request memory request = buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfill.selector
        );
        request.add("get", string(abi.encodePacked("https://arvan.nparsa.ir/credittotoken/", tokenId)));
        request.add("path", "credit");
        sendChainlinkRequestTo(oracle, request, fee);
    }
    
    function fulfill(bytes32 _requestId, bytes32 _credit) public recordChainlinkFulfillment(_requestId) {
        // We want to do http get request to the api https://arvan.nparsa.ir/credittotoken/TOKEN_ID
        tokenData = uint32(_credit >> 224);
    }

    function certToPool(uint256 tokenID) public {
        require(msg.sender == ownerOf(tokenID), "You are not the owner of this certificate");
        // We want to do http get request to the api https://arvan.nparsa.ir/certToPool/TOKEN_ID
        Chainlink.Request memory request = buildChainlinkRequest(
            jobId,
            address(this),
            this.cerToPoolfulfill.selector
        );
        request.add("get", string(abi.encodePacked("https://arvan.nparsa.ir/certToPool/", tokenID, "/", msg.sender)));
        request.add("path", "approved");
        sendChainlinkRequestTo(oracle, request, fee);
    }

    function cerToPoolfulfill(bytes32 _requestId, bytes32 _approved) public recordChainlinkFulfillment(_requestId) {
        // We want to do http get request to the api https://arvan.nparsa.ir/certToPool/TOKEN_ID
        if (uint32(_approved >> 224) != 1) {
            require(false, "Certificate is not approved");
        }
    }

    function withdraw(uint256 tokenID) public {
        // We want to do http get request to the api https://arvan.nparsa.ir/withdraw/TOKEN_ID
        Chainlink.Request memory request = buildChainlinkRequest(
            jobId,
            address(this),
            this.withdrawfulfill.selector
        );
        request.add("get", string(abi.encodePacked("https://arvan.nparsa.ir/withdraw/", tokenID)));
        request.add("path", "amount");
        sendChainlinkRequestTo(oracle, request, fee);
    }

    function withdrawfulfill(bytes32 _requestId, bytes32 _amount) public recordChainlinkFulfillment(_requestId) {
        // We want to do http get request to the api https://arvan.nparsa.ir/withdraw/TOKEN_ID-TokenData
        uint32 amount = uint32(_amount >> 224);
        GNEInstance.transfer(msg.sender, amount);
    }

}
