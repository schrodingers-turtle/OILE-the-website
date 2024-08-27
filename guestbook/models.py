from django.db.models import Model, CharField

class Post(Model):
    name = CharField(max_length=5)
    message = CharField(max_length=10000)

    def __str__(self):
        return f'{self.name} - "{self.message}"'
