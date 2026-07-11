from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_userpreference_notification_prefs"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="job_title",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="user",
            name="location",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bengaluru", "Bengaluru"),
                    ("delhi", "Delhi"),
                    ("gurugram", "Gurugram"),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="linkedin_url",
            field=models.URLField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/%Y/%m/"),
        ),
    ]
