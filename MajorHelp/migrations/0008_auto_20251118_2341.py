from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('MajorHelp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]