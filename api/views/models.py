from django.db import models

# Create your models here.

class EthDomain(models.Model):

    node = models.CharField(primary_key=True, max_length=128)
    domain_name = models.TextField(null=False)
    token_id = models.TextField(null=False)
    class Meta:
        managed = True
        db_table = 'eth_domain'


class DomainRegistration(models.Model):

    node = models.ForeignKey(EthDomain, on_delete=models.DO_NOTHING)
    registrant = models.CharField(max_length=64, blank=False, null=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    cost = models.BigIntegerField(null=False)
    tx_block = models.IntegerField(null=False)
    tx_hash = models.CharField(max_length=128, blank=False, null=False)
    tx_hash_index = models.CharField(max_length=16, blank=False, null=False)
    tx_dt = models.DateTimeField(null=False, blank=False)
    gas_used = models.BigIntegerField(default=0)


    class Meta:
        managed = True
        db_table = 'domain_registration'


class DomainRenewal(models.Model):

    node = models.ForeignKey(EthDomain, on_delete=models.DO_NOTHING)
    domain_name = models.TextField()
    # renewer = models.CharField(max_length=64, blank=False, null=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    cost = models.BigIntegerField(null=False)
    tx_block = models.IntegerField(null=False)
    tx_hash = models.CharField(max_length=128, blank=False, null=False)
    tx_hash_index = models.CharField(max_length=16, blank=False, null=False)
    tx_dt = models.DateTimeField(null=False, blank=False)
    gas_used = models.BigIntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'domain_renewal'

class DomainTransfer(models.Model):

    node = models.ForeignKey(EthDomain, on_delete=models.DO_NOTHING)
    marketplace_contract_address = models.CharField(max_length=64, blank=False, null=False)
    buyer = models.CharField(max_length=64, blank=False, null=False)
    seller = models.CharField(max_length=64, blank=False, null=False)
    eth_price = models.DecimalField( max_digits=65, decimal_places=0)
    weth_price = models.DecimalField( max_digits=65, decimal_places=0)
    usdc_price = models.DecimalField( max_digits=65, decimal_places=0)
    dai_price = models.DecimalField( max_digits=65, decimal_places=0)
    spot_price = models.DecimalField( max_digits=65, decimal_places=0)
    tx_block = models.IntegerField(null=False)
    tx_hash = models.CharField(max_length=128, blank=False, null=False)
    tx_hash_index = models.CharField(max_length=16, blank=False, null=False)
    tx_dt = models.DateTimeField(null=False, blank=False)
    gas_used = models.BigIntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'domain_transfer'