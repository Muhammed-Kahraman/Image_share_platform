from django.db import models


# Create your models here.
from Image.validators import validate_file_extension


class Image(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=50, editable=True)
    image = models.ImageField(validators=[validate_file_extension], editable=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title + ": " + str(self.image).replace("videos/", "").replace(".jpg", "")

    class Meta:
        ordering = ['-created_date']


