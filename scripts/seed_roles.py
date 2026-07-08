from apps.accounts.models import Role

DEFAULT_ROLES = [
    ('admin', 'Admin', 'Full administrative access'),
    ('recruiter', 'Recruiter', 'Can manage jobs and candidates'),
    ('reviewer', 'Reviewer', 'Can review candidates and update statuses'),
]

for code, name, description in DEFAULT_ROLES:
    Role.objects.get_or_create(code=code, defaults={'name': name, 'description': description})

print('Default roles seeded.')