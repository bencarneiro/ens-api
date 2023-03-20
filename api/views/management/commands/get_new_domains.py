from views.models import EthDomain
import requests
from api.settings import ETH_REGISTRY_ADDRESS, ETH_REGISTRY_ABI, ETHERSCAN_API_KEY
from django.core.management.base import BaseCommand
from views.views import hash_name
from views.models import EthDomain
from datetime import datetime
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/jNqs_iFSQOdvi20Vy6YQLivCUD0PwT27'))
ens_contract = w3.eth.contract(address=w3.toChecksumAddress(ETH_REGISTRY_ADDRESS), abi=ETH_REGISTRY_ABI)




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
        sort = "desc"
        offset = "100"
        page = "1"
        response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_REGISTRY_ADDRESS}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort={sort}&apikey={ETHERSCAN_API_KEY}").json()
        for transaction in response['result']:
            # if ("register" in transaction['functionName']) and (transaction['txreceipt_status']=="1"):
            if True:
        #     print(transaction)
                tx_block = transaction['blockNumber']
                tx_hash = transaction['hash']
                tx_dt = datetime.fromtimestamp(int(transaction['timeStamp']))

                name_hash = None
                domain_name = None
                registrant = None
                expiration_date = None
                cost = None

                receipt = w3.eth.get_transaction_receipt(transaction['hash'])
                registered_names = ens_contract.events.NameRegistered().processReceipt(receipt)
                renewed_names = ens_contract.events.NameRenewed().processReceipt(receipt)
                # print("registered_names")
                # print(registered_names)
                # print("renewed_names")
                # print(renewed_names)

                # renewed_names
                # (AttributeDict({'args': AttributeDict({'label': b'\xec-[z%\x19"w\xa8\xef$\xe5\x92\x98\xa7T\xf3\xab@\xf1\xf1\x05\xc1\xee7\x03\x07\x9fa\xc0h\x1f', 'name': 'squatchy', 'cost': 8361306034214821, 'expires': 1827991631}), 'event': 'NameRenewed', 'logIndex': 226, 'transactionIndex': 72, 'transactionHash': HexBytes('0x865ba3efef3791f4301465953cc584b8989dad192891452d1c57f862b0f8013e'), 'address': '0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5', 'blockHash': HexBytes('0x3b05016829fdf6fbcfa0466df45162bd136bd93f0a6d27400689605b3f984e05'), 'blockNumber': 16856812}),)
                # parse with 
                # for event in renewed_names:


                for event in registered_names:
                    # print(event['args'])
                    domain_name = event['args']['name']
                    name_hash = hash_name(domain_name)
                    cost = int(event['args']['cost'])
                    owner = event['args']['owner']
                    expiry = datetime.fromtimestamp(int(event['args']['expires']))
                
                if domain_name:
                    new_domain = EthDomain(
                        name_hash = name_hash,
                        domain_name = domain_name,
                        registrant = owner,
                        expiration_date = expiry,
                        cost = cost,
                        tx_block = tx_block,
                        tx_hash = tx_hash,
                        tx_dt = tx_dt
                    )
                    new_domain.save()
                else:
                    print("no registration to record")


