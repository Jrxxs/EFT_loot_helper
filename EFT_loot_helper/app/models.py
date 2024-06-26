from django.db import models

# Create your models here.

# class ItemTypes(models.Model):

#     class Types(models.TextChoices):
#         'ammo'
#         'ammoBox'
#         'any'
#         'armor'
#         'armorPlate'
#         'backpack'
#         'barter'
#         'container'
#         'glasses'
#         'grenade'
#         'gun'
#         'headphones'
#         'helmet'
#         'injectors'
#         'keys'
#         'markedOnly'
#         'meds'
#         'mods'
#         'noFlea'
#         'pistolGrip'
#         'preset'
#         'provisions'
#         'rig'
#         'suppressor'
#         'wearable'

#     type = models.CharField(verbose_name="item_type", choices=Types)


class CachedItem(models.Model):
    name = models.CharField(verbose_name='item_name', max_length=255)
    itemId = models.CharField(verbose_name='Item_id', max_length=255, unique=True) # id in cache
    # types = models.ManyToManyField(ItemTypes, related_name="item_types")

    def __str__(self) -> str:
        return self.name