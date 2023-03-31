from views.models import EthDomain, DomainRegistration
import requests
from api.settings import ETH_REGISTRY_ADDRESS, ETH_REGISTRY_ABI, ETHERSCAN_API_KEY, BASE_REGISTRAR_ADDRESS, NFT_TRANSFER_TOPIC
from django.core.management.base import BaseCommand
from views.views import hash_name, get_token_id
from views.models import EthDomain
import datetime
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/jNqs_iFSQOdvi20Vy6YQLivCUD0PwT27'))
# ens_contract = w3.eth.contract(address=w3.toChecksumAddress(ETH_REGISTRY_ADDRESS), abi=ETH_REGISTRY_ABI)




# OK Takeaways
# The main eth registrar can only be scraped for 
# 1 new registrations
# 2 renewals
# we will have to scrape a different contract for 
# 1 transfers of NFT ownership
# transfers of NFT Registration
# Changing the resolved address
# Sales on 3rd party marketplaces ( Will this be accounted for by scraping )

# if you want to go through all the logs and decode the hexbytes into decmial data
# https://docs.etherscan.io/api-endpoints/logs
# Then you can filter logs by topic ^ see docs
# but you could pull one thousand registration events at a time by using this API endpoint
# insead of the current implementation where we pull every transaction on the ENS contract. 


class Command(BaseCommand):

    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
        parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):

        start_block = kwargs['start_block']
        end_block = kwargs['end_block']
        sort = "asc"
        offset = "1000"
        page = "1"
        new_start_block = False


        keep_going = True

        while keep_going:
            if new_start_block:
                start_block = str(new_start_block)
            print(f"making request starting at block #{start_block}")
            response = requests.get(f"https://api.etherscan.io/api?module=logs&action=getLogs&address={BASE_REGISTRAR_ADDRESS}&fromBlock={start_block}&toBlock={end_block}&page={page}&offset={offset}&sort={sort}&topic0={NFT_TRANSFER_TOPIC}&apikey={ETHERSCAN_API_KEY}").json()
            

            for log in response['result']:
                print(log)

            if len(response['result']) != 1000:
                keep_going = False
            else:
                new_start_block = int(response['result'][-1]['blockNumber'], 16)
                print("overwriting new start block")

                print(start_block)
                print(new_start_block)
        
        