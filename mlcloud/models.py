from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    url = models.ImageField(upload_to='static/images/')
    tags = models.ManyToManyField("Tag", blank=True)
    train = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.pk)

class Tag(models.Model):
    name = models.CharField(max_length=100)