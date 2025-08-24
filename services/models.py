from django.db import models


class Service(models.Model):
    SERVICE_TYPES = [
        ('group', 'Групове'),
        ('individual', 'Індивідуальне')
    ]
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class Activity(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    photo = models.ImageField(upload_to='trainers/')
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.full_name