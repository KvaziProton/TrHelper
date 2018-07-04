from django.db import models

class UserDict(models.Model):
    kurd = models.CharField(max_length=20, unique=True)
    ru = models.CharField(max_length=20)
    info = models.CharField(max_length=200, blank=True)

    #because we will always look for russian term by kurdish one
    #(and method model.get always return QuerySet object)
    def __str__(self):
        return self.ru

# class PreModeratedDict(models.Model):
#     kurd = models.CharField(max_length=20)
#     ru = models.CharField(max_length=20)
#     info = models.CharField(max_length=200, blank=True)
