from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(
                    choices=[('mindmap', 'Mind Map'), ('flowchart', 'Flowchart')],
                    max_length=20,
                )),
                ('data', models.JSONField(default=dict)),
                ('thumbnail', models.TextField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
    ]
