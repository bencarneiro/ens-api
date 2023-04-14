from views.models import EthDomain, DomainRegistration
import requests
from api.settings import ETH_REGISTRY_ADDRESS, ETHERSCAN_API_KEY, MASTODON_API_BASE_URL, MASTODON_FIRST_SECRET, MASTODON_LOGIN_EMAIL, MASTODON_LOGIN_PASSWORD, MASTODON_SECOND_SECRET
from django.core.management.base import BaseCommand
from views.views import hash_name, get_token_id
from views.models import EthDomain
import datetime
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/jNqs_iFSQOdvi20Vy6YQLivCUD0PwT27'))
# ens_contract = w3.eth.contract(address=w3.toChecksumAddress(ETH_REGISTRY_ADDRESS), abi=ETH_REGISTRY_ABI)

from mastodon import Mastodon

api = Mastodon(MASTODON_FIRST_SECRET, MASTODON_SECOND_SECRET, api_base_url=MASTODON_API_BASE_URL)
api.log_in(MASTODON_LOGIN_EMAIL, MASTODON_LOGIN_PASSWORD, scopes=["read", "write"])

eth_price_response = requests.get(f"https://api.etherscan.io/api?module=stats&action=ethprice&api_key={ETHERSCAN_API_KEY}")
eth_price = eth_price_response.json()['result']['ethusd']
print(f"today's eth price is {eth_price}")

class Command(BaseCommand):

    help = 'Displays current time'


    def handle(self, *args, **kwargs):
        last_registration = DomainRegistration.objects.latest('tx_block')
        start_block = str(last_registration.tx_block)
        end_block = "99999999"
        sort = "asc"
        offset = "1000"
        page = "1"

        response = requests.get(f"https://api.etherscan.io/api?module=logs&action=getLogs&address={ETH_REGISTRY_ADDRESS}&fromBlock={start_block}&toBlock={end_block}&page={page}&offset={offset}&sort={sort}&topic0=0xca6abbe9d7f11422cb6ca7629fbf6fe9efb1c621f71ce8f02b9f2a230097404f&apikey={ETHERSCAN_API_KEY}").json()
        for log in response['result']:
            try:
                domain_name = bytes.fromhex(log['data'][258:]).decode('utf-8').rstrip('\x00')
            except:
                print(f"ERROR decoding tx {log['transactionHash']}")
                domain_name = "___INVALID_DOMAIN___"
            name_hash = hash_name(domain_name).hex()
            token_id = get_token_id(domain_name)
            registrant = "0x" + log['topics'][2][-40:]
            expiry = datetime.datetime.fromtimestamp(int(log['data'][130:194], 16))
            tx_block = int(log['blockNumber'], 16)
            tx_hash = log['transactionHash']
            tx_hash_index = log['transactionIndex']
            tx_dt = datetime.datetime.fromtimestamp(int(log['timeStamp'], 16))
            cost = int(log['data'][66:130], 16)
            gas_used = int(log['gasUsed'], 16)

            new_domain = EthDomain(
                node = name_hash,
                domain_name = domain_name,
                token_id = token_id
            )
            new_domain.save()
            existing_events = DomainRegistration.objects.filter(tx_hash=tx_hash, node_id=name_hash)
            print(existing_events)
            print(len(existing_events))
            try:
                new_registration = DomainRegistration(
                    node=new_domain,
                    registrant = registrant,
                    expiration_date = expiry,
                    cost = cost,
                    tx_block = tx_block,
                    tx_hash = tx_hash,
                    tx_hash_index = tx_hash_index,
                    tx_dt = tx_dt,
                    gas_used = gas_used
                )
                new_registration.save()
            except Exception as e:
                print(f"ERROR {e}")
            print(f"successfully saved registration of node {name_hash} in transaction {tx_hash}")
            print(existing_events)
            print()
            if len(existing_events) > 0:
                print("DUPLICATE")
                continue
            else:
                usd_price = float(eth_price) * (cost / (10**18))
                print("GONNA POST")
                print(domain_name)
                print(registrant)
                name = w3.ens.name(registrant)
                if not name:
                    name = registrant
                print(expiry)
                print(tx_hash)
                print(cost)
                print(usd_price)
                toot = f"'{domain_name}.eth' just registered until {expiry.strftime('%Y-%m-%d')} by {name} for {round((cost / (10**18)),3)} ETH (${round(usd_price,2)}) --- https://etherscan.io/tx/{tx_hash}"
                api.status_post(toot, visibility="unlisted")
                print(toot)

       