
# Generated by Django 5.2.3 on 2025-07-03 06:48


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='has_wifi',
        ),
        migrations.AddField(
            model_name='cafe',
            name='keyword',
            field=models.ManyToManyField(blank=True, related_name='keyword', to='tag.tag'),
        ),
    ]
