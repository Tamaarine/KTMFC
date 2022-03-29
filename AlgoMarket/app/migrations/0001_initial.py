# Generated by Django 4.0.2 on 2022-03-29 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('username', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('image_path', models.CharField(blank=True, max_length=200)),
                ('wallet_address', models.CharField(max_length=200)),
                ('last_updated', models.TimeField(auto_now=True)),
                ('creator', models.BooleanField(default=False)),
                ('services_completed', models.IntegerField(default=0)),
                ('subscriber_count', models.IntegerField(default=0)),
                ('biography', models.CharField(max_length=200)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=1)),
                ('image_path', models.CharField(blank=True, max_length=200)),
                ('amount_available', models.IntegerField(default=-1)),
                ('created', models.TimeField(auto_now_add=True)),
                ('last_updated', models.TimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('pro_price', models.IntegerField(default=0)),
                ('premium_price', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('startDate', models.TimeField()),
                ('fulfillmentDate', models.TimeField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Perk',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('free_amount', models.IntegerField(default=0)),
                ('pro_amount', models.IntegerField(default=0)),
                ('premium_amount', models.IntegerField(default=0)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subscription')),
            ],
        ),
    ]
