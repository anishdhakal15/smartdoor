from django.db import models

# Create your models here.
class AdminUsers(models.Model):
    post_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=500, default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to='media/image', default="")

    def __str__(self):
        return self.name