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
        response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_REGISTRY_ADDRESS}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort={sort}&apikey={ETHERSCAN_API_KEY}&order=desc").json()
        for transaction in response['result']:
            if ("register" in transaction['functionName']) and (transaction['txreceipt_status']=="1"):
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
                print(registered_names)

                for event in registered_names:
                    print(event['args'])
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


