from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "department",
            "location",
            "employment_type",
            "experience_min_years",
            "experience_max_years",
            "description",
            "requirements",
            "required_skills",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 5}),
            "required_skills": forms.HiddenInput(
                attrs={"id": "id_required_skills_hidden"}
            ),
        }

    def clean_required_skills(self):
        raw_value = (self.cleaned_data.get("required_skills") or "").strip()
        parts = raw_value.replace("\n", ",").split(",")
        cleaned = []
        seen = set()
        for part in parts:
            skill = part.strip()
            if not skill:
                continue
            key = skill.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(skill)
        return ", ".join(cleaned)
