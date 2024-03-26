from client import Client
from data.config import private_key, ftm_rpc

client = Client(private_key=private_key, rpc=ftm_rpc)

playerid = client.active_player(contract_address="0x058ec56aba13f7fee3ae9c9b91b3bb03bc336143")
#claimedrewards = client.daily_claimed_rewards(contract_address="0x058ec56aba13f7fee3ae9c9b91b3bb03bc336143", playerID=playerid)
# player_info = client.players_info(contract_address="0x058ec56aba13f7fee3ae9c9b91b3bb03bc336143",
#                                                playerID=playerid)

print(playerid)
#print(player_info)
client.start_action(contract_address="0x058ec56aba13f7fee3ae9c9b91b3bb03bc336143",
                                               playerID=playerid)
