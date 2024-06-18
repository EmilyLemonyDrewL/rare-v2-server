# Generated by Django 4.2.8 on 2024-06-18 03:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
                ('image_url', models.CharField(max_length=400)),
                ('content', models.CharField(max_length=1000)),
                ('approved', models.BooleanField(default=False)),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='rareapi.category')),
            ],
        ),
        migrations.CreateModel(
            name='RareUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('bio', models.CharField(max_length=400)),
                ('profile_image_url', models.CharField(max_length=400)),
                ('email', models.CharField(max_length=200)),
                ('created_on', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('uid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserTypeChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('promotion', 'Promotion'), ('demotion', 'Demotion')], default='promotion', max_length=10)),
                ('admin_one_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_one', to='rareapi.rareuser')),
                ('admin_two_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_two', to='rareapi.rareuser')),
                ('modified_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_user', to='rareapi.rareuser')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions_as_follower', to='rareapi.rareuser')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions_as_author', to='rareapi.rareuser')),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.post')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.tag')),
            ],
        ),
        migrations.CreateModel(
            name='PostReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.post')),
                ('rare_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.rareuser')),
                ('reaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.reaction')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='rare_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='rareapi.rareuser'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', through='rareapi.PostTag', to='rareapi.tag'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=140)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.rareuser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='rareapi.post')),
            ],
        ),
    ]
