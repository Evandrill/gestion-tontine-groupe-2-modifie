from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name='President'),
        Group(name='Tresorier'),
        Group(name='Membre'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0005_remove_don_donateur_remove_don_enregistre_par_and_more'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]