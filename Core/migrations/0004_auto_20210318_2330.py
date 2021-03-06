# Generated by Django 3.1.5 on 2021-03-18 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_remove_product_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='orders_detail',
            name='product_images_id',
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, default='no_photo.jpg', upload_to='Product_Images/'),
        ),
        migrations.DeleteModel(
            name='Product_Image',
        ),
        migrations.DeleteModel(
            name='User_Detail',
        ),
    ]
