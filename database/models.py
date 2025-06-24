from tortoise import fields
from tortoise.models import Model

class CitizenRequest(Model):
    id = fields.UUIDField(pk=True)
    nom_complet = fields.CharField(max_length=255)
    telephone = fields.CharField(max_length=50)
    email = fields.CharField(max_length=255, null=True)
    superficie = fields.CharField(max_length=50)
    nature = fields.CharField(max_length=100)
    situation = fields.TextField()
    statut = fields.CharField(max_length=50, default="demande_soumise")
    date_soumission = fields.DatetimeField(auto_now_add=True)
    donnees_geo = fields.JSONField(null=True)
    documents = fields.JSONField(null=True)
