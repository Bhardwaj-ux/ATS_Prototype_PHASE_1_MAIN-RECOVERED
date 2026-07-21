from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="required_skills",
            field=models.TextField(
                blank=True, help_text="Comma-separated skills for the ideal candidate"
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("open", "Open"),
                    ("closed", "Closed"),
                    ("on_hold", "Archived"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
    ]
