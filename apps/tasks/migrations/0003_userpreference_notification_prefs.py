from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userpreference"),
    ]

    operations = [
        migrations.AddField(
            model_name="userpreference",
            name="notification_prefs",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
