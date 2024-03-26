from web3 import Web3
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