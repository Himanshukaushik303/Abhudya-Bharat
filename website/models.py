from django.db import models
from django.contrib.auth.models import User
import os


class Path_and_rename:
    def __init__(self, path):
        self.path = path

    def wrapper(self, instance, filename):
        ext = filename.split(".")[-1]
        # get filename
        if self.path == "product_images":
            filename = "{}.{}.{}".format(instance.product, instance.product.id, ext)
            print(filename)
        elif self.path == "product_video":
            filename = "{}.{}".format(instance.product_name, ext)
            # set filename as random string
        else:
            filename = "{}.{}".format(instance.ent_full_name, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


# Create your models here.
STATUS = ((0, "pending"), (1, "active"), (-1, "rejected"))
USE = ((0, "in"), (1, "out"))


class Categories(models.Model):
    category = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return self.category


class Bussiness_Partner(models.Model):
    bp_full_name = models.CharField(max_length=100, null=False)
    bp_designation = models.CharField(max_length=100, null=False)
    bp_email = models.EmailField(max_length=254)
    bp_number = models.DecimalField(max_digits=10, decimal_places=0)
    company_name = models.CharField(max_length=100, null=False)
    company_address = models.TextField()
    communication_address = models.TextField()
    incorporation_year = models.DecimalField(max_digits=4, decimal_places=0)
    founder_full_name = models.CharField(max_length=100, null=False)
    founder_email = models.EmailField(max_length=254)
    founder_number = models.DecimalField(max_digits=10, decimal_places=0)
    user = models.OneToOneField(
        User, related_name="bp", on_delete=models.CASCADE, null=True
    )
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.company_name


class Product(models.Model):
    product_id = models.IntegerField(unique=True, null=False, default=1)
    product_name = models.CharField(max_length=100, null=False)
    product_description = models.TextField()
    product_price = models.IntegerField(default=0)
    product_video = models.FileField(
        upload_to=Path_and_rename("product_video").wrapper, null=True
    )
    company = models.ForeignKey(Bussiness_Partner, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Categories, related_name="products")
    status = models.IntegerField(choices=USE, default=0)

    def __str__(self):
        return self.product_name


class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(
        upload_to=Path_and_rename("product_images").wrapper
    )
    product_img_description = models.TextField()

    def __str__(self):
        return self.product.product_name + " Image"


class FAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.product.product_name + " FAQ"


class Entrepreneurs(models.Model):
    ent_full_name = models.CharField(max_length=100, null=False)
    ent_email = models.EmailField(max_length=254)
    ent_number = models.DecimalField(unique=True, max_digits=10, decimal_places=0)
    ent_area = models.CharField(max_length=200, null=False)
    ent_pincode = models.DecimalField(max_digits=6, decimal_places=0)
    ent_address = models.TextField()
    ent_aadhar = models.DecimalField(unique=True, max_digits=12, decimal_places=0)
    ent_photo = models.ImageField(upload_to=Path_and_rename("entrepreneurs").wrapper)
    ent_address_proof = models.FileField(
        upload_to=Path_and_rename("entrepreneurs").wrapper
    )
    user = models.OneToOneField(
        User, related_name="ent", on_delete=models.CASCADE, null=True
    )
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.ent_full_name
