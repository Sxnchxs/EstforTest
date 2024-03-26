from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account
from typing import Optional
import requests

import json

from data.config import PLAYER_ABI, GAME_ABI


class Client:
    # Load GameAbi to itteract
    with open(GAME_ABI) as f:
        default_abi = f.read()

    def __init__(
            self,
            private_key: str,
            rpc: str
    ):
        self.private_key = private_key
        self.rpc = rpc
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.rpc))
        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)
        self.account = self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.private_key))


    # Get playerID from wallet address
    def active_player(self, contract_address: str)->int:
        return int(self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=Client.default_abi
        ).functions.activePlayer(self.address).call())
    
    # Get list of claimed rewards from playerID
    def daily_claimed_rewards(self, contract_address: str, playerID: int)->list:
        return list(self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=Client.default_abi
        ).functions.dailyClaimedRewards(playerID).call())
    
    # Get player info from playerID
    def players_info(self, contract_address: str, playerID: int)->list:
        return list(self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=Client.default_abi
        ).functions.players(playerID).call())
    
    def start_action(self, contract_address: str, playerID: int):

        _attire = {
            "attire": {
                "head": 0,
                "neck": 0,
                "body": 0,
                "arms": 0,
                "legs": 0,
                "feet": 0,
                "ring": 0,
                "reserved1": 0
            },
            "actionId": 506,
            "regenerateId": 0,
            "choiceId": 0,
            "rightHandEquipmentTokenId": 2561,
            "leftHandEquipmentTokenId": 0,
            "timespan": 86400,
            "combatStyle": 0
        }
        _queuedActions = [_attire]
        _queuedStatus = 2

        a = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=Client.default_abi
        ).functions.startActions(playerID, _queuedActions, _queuedStatus).build_transaction({
            'from': self.address,
            'gas': int(self.w3.eth.get_block('latest')["gasUsed"]),
            'gasPrice': int(self.w3.eth.gas_price * 1.3),
            'nonce': self.w3.eth.get_transaction_count(self.address)
        })
        
        print(a["gas"])
        print(a["gasPrice"])
        # print(a['data'])
        
        
        
        signed_tx = self.w3.eth.account.sign_transaction(a, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt:
            print('Transaction successfull')
            print(tx_hash.hex)
