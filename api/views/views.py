from django.shortcuts import render
from web3 import Web3
from views.models import EthDomain, DomainRegistration, DomainRenewal
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/jNqs_iFSQOdvi20Vy6YQLivCUD0PwT27'))
import datetime
import pytz

utc=pytz.UTC

# Create your views here.

def hash_name(desired_name):
    # call this function without the .eth
    # and for now call it without any subdomains
    x0 = 0
    x1 = w3.keccak(text='eth')
    eth = w3.solidityKeccak(['uint256', 'bytes32'], [x0, x1])  # this is .eth
    namehash = w3.keccak(text=desired_name)
    return w3.solidityKeccak(['bytes32', 'bytes32'], [eth, namehash])  # this is vitalik.eth

def get_token_id(name):
    return int.from_bytes(Web3.solidityKeccak(['string'], [name]), "big")

@csrf_exempt
def search_domains(request):
    domain_list = EthDomain.objects.all()
    if "q" in request.GET and request.GET['q']:
        domain_list = domain_list.filter(domain_name__contains=request.GET['q'])
    response = {
        'length': len(domain_list),
        'status': "success",
        "data": list(domain_list.values())
    }
    return JsonResponse(response)

@csrf_exempt
def get_domain_details(request):
    domain_obj = EthDomain.objects.get(domain_name=request.GET['name'])
    registrations = DomainRegistration.objects.filter(node_id=domain_obj.node)
    renewals = DomainRenewal.objects.filter(node_id=domain_obj.node)
    utc=pytz.UTC
    last_expiry = datetime.datetime.fromtimestamp(0).replace(tzinfo=utc)
    
    for registration in registrations:
        if registration.expiration_date.replace(tzinfo=utc) > last_expiry:
            last_expiry = registration.expiration_date.replace(tzinfo=utc)
    for renewal in renewals:
        if renewal.expiration_date.replace(tzinfo=utc) > last_expiry:
            last_expiry = renewal.expiration_date.replace(tzinfo=utc)
    if datetime.datetime.now().replace(tzinfo=utc) > last_expiry:
        expired = True
    else: 
        expired = False
    response = {
        'status': "success",
        'domain': domain_obj.domain_name,
        'link': f"https://app.ens.domains/name/{domain_obj.domain_name}.eth",
        'token_id': domain_obj.token_id,
        'node': domain_obj.node,
        "registrations": list(registrations.values()),
        "renewals": list(renewals.values()),
        'expiry': last_expiry,
        'expired': expired
    }
    return JsonResponse(response)