from django.db import models
import os

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    class Meta: 
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        products = self.product_set.all()
        for product in products:
            product.delete()
        super(Categories, self).delete(using=None, keep_parents=False)
    
class Size(models.Model):
    category_id = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    size = models.IntegerField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.size)

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=2000)
    category_id = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    size_id = models.ManyToManyField(Size)
    image = models.FileField(upload_to='Product_Images/', blank=True, default='no_photo.jpg')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image.name != 'no_photo.jpg':
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
                super(Product, self).delete(*args, **kwargs)

class Order(models.Model):
    shipping_address = models.CharField(max_length=100)
    total_payment = models.DecimalField(max_digits=8, decimal_places=2)
    contact_person = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, null=True)
    quantity = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Orders_Detail(models.Model):
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    size_id = models.ForeignKey(to=Size, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.order_id)

