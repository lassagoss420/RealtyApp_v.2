from django.db import models


class Client(models.Model):
    class Meta:
        db_table = 'clients'
        get_latest_by = "order_date"

    CATEGORY = (
        ('Client', 'Client'),
        ('Agent', 'Agent'),
    )

    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=126, null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True, verbose_name='Phone No.')
    str_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Street Address')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    class Meta:
        db_table = 'listings'
        get_latest_by = "order_date"

    CATEGORY = (
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
        )

    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    title = models.CharField(max_length=255, null=True, blank=True)
    str_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Street Address')
    description = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_client_name(self):
        return self.client.name
