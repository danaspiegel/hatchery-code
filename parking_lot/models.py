from django.db import models

LOT_TYPES = (
    ('S', 'Street Lot'),
    ('M', 'Multi-level Above Ground'),
    ('O', 'Multi-level Below Ground'),
)

SPOT_SIZES = (
    ('S', 'Standard'),
    ('C', 'Compact'),
    ('T', 'Truck'),
    ('U', 'Unusable'),
)

ORIENTATIONS = (
    ('N', 'North'),
    ('NE', 'North East'),
    ('E', 'East'),
)

class Lot(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    lot_type = models.CharField(max_length=1, choices=LOT_TYPES, db_index=True)
    open_time = models.TimeField('Lot opens')
    close_time = models.TimeField('Lot closes')
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'

    @property
    def is_open(self):
        return self.open_time <= datetime.datetime.utcnow() <= self.close_time
    
    @property
    def spot_count(self):
        return self.spots.count()
    
    @property
    def spot_count_by_level(self):
        return self.spots.order_by('level').\
               values_list('level').annotate(models.Count('level'))

    def __unicode__(self):
        return self.name

    
class Spot(models.Model):
    lot = models.ForeignKey('Lot', related_name='spots')
    level = models.IntegerField(default=0)
    designation = models.CharField(max_length=2, blank=True)
    size = models.CharField(max_length=1, choices=SPOT_SIZES, db_index=True)
    orientation = models.CharField(max_length=2, choices=ORIENTATIONS)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    class Meta:
        verbose_name = 'Parking Spot'
        verbose_name_plural = 'Parking Spots'

    def __unicode__(self):
        return u'{0}-{1}'.format(self.level, self.designation)
