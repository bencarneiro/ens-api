from django.shortcuts import render
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/jNqs_iFSQOdvi20Vy6YQLivCUD0PwT27'))

# Create your views here.

def hash_name(desired_name):
    # call this function without the .eth
    # and for now call it without any subdomains
    x0 = 0
    x1 = w3.keccak(text='eth')
    eth = w3.solidityKeccak(['uint256', 'bytes32'], [x0, x1])  # this is .eth
    namehash = w3.keccak(text=desired_name)
    return w3.solidityKeccak(['bytes32', 'bytes32'], [eth, namehash])  # this is vitalik.eth
