# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Conflicts(models.Model):
    enchant_name = models.OneToOneField('Enchants', models.DO_NOTHING, db_column='enchant_name', primary_key=True)
    conflict_group = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conflicts'
        unique_together = (('enchant_name', 'conflict_group'),)

class Combinations(models.Model):
    item_name = models.OneToOneField('Items', models.DO_NOTHING, db_column='item_name', primary_key=True)
    enchant_name = models.ForeignKey('Enchants', models.DO_NOTHING, db_column='enchant_name')
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'combinations'
        unique_together = (('item_name', 'enchant_name'),)

class Enchants(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    max_level = models.IntegerField()
    multiplier = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enchants'

class Items(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'items'


