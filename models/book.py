from tortoise import fields
from tortoise.models import Model

class Books(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.ForeignKeyField("models.User", related_name='books')
    publication_date = fields.DateField()
    genre = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13)
    average_rating = fields.FloatField()
    num_ratings = fields.IntField()
    description = fields.TextField()
    image_url = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    