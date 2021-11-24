from django.db import models
from django.contrib.auth.models import User
from wall.utils import send_transaction
import hashlib

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    img = models.ImageField(upload_to='pics')

    # identificativo univoco del messaggio
    hash = models.CharField(max_length=32, default=None, null=True)
    # identificativo della transazione associata
    tx_id = models.CharField(max_length=66, default=None, null=True)

    def write_on_chain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.tx_id = send_transaction(self.hash)
        self.save()

    def __str__(self):
        return self.title + ' | ' + str(self.author)





