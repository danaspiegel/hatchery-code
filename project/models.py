from django.db import models

from countries import COUNTRIES

ADDRESS_TYPES = (
    ('W', 'Work'),
    ('H', 'Home'),
    ('O', 'Other'),
)

class Person(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=100)
    
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

class Address(models.Model):
    person = models.ForeignKey('Person', related_name='addresses')
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPES, db_index=True)

    street_address_1 = models.CharField(max_length=100)
    street_address_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, db_index=True)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2, choices=COUNTRIES, db_index=True)
    
    is_primary_address = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __unicode__(self):
        return u'{0}: {1}, {2}, {3}, {4}'.format(self.get_country_display(),
                                            self.street_address_1,
                                            self.city, self.state_province,
                                            self.postal_code)
