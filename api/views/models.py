from django.db import models

# Create your models here.

class EthDomain(models.Model):

    name_hash = models.CharField(primary_key=True, max_length=128)
    domain_name = models.TextField()
    registrant = models.CharField(max_length=64, blank=False, null=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    cost = models.BigIntegerField(null=False)
    tx_block = models.IntegerField(null=False)
    tx_hash = models.CharField(max_length=128, blank=False, null=False)
    tx_dt = models.DateTimeField(null=False, blank=False)


    class Meta:
        managed = True
        db_table = 'eth_domain'

class DomainRenewal(models.Model):

    name_hash = models.CharField(primary_key=True, max_length=128)
    domain_name = models.TextField()
    # registrant = models.CharField(max_length=64, blank=False, null=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    cost = models.BigIntegerField(null=False)
    tx_block = models.IntegerField(null=False)
    tx_hash = models.CharField(max_length=128, blank=False, null=False)
    tx_dt = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'domain_renewal'