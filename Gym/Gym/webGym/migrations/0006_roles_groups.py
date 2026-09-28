from django.db import migrations


ROLES = [
    {
        'name': 'Оператор проходной',
        'perms': ['can_manage_gate', 'can_manage_trainers'],
    },
    {
        'name': 'Тренер',
        'perms': [],
    },
]


def create_roles(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')
    # Data-миграция выполняется до post_migrate-сигнала, поэтому ContentType
    # и Permission для abonement ещё могут отсутствовать. Создаём их здесь.
    ct, _ = ContentType.objects.get_or_create(app_label='webGym', model='abonement')
    perm_names = ['add_abonement', 'change_abonement', 'view_abonement', 'delete_abonement',
                  'can_manage_gate', 'can_manage_trainers']
    for codename in perm_names:
        Permission.objects.get_or_create(
            codename=codename, content_type=ct, defaults={'name': codename},
        )
    for role in ROLES:
        group, _ = Group.objects.get_or_create(name=role['name'])
        group.permissions.clear()
        for perm_codename in role['perms']:
            perm = Permission.objects.filter(codename=perm_codename, content_type=ct).first()
            if perm:
                group.permissions.add(perm)


def delete_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[r['name'] for r in ROLES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('webGym', '0005_abonement_trainer_visit'),
    ]

    operations = [
        migrations.RunPython(create_roles, delete_roles),
    ]