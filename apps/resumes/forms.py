from django import forms
from .models import ResumeFile


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeFile
        fields = ['application', 'file']

    def clean_file(self):
        file = self.cleaned_data['file']
        allowed = ['.pdf', '.doc', '.docx']
        lower_name = file.name.lower()
        if not any(lower_name.endswith(ext) for ext in allowed):
            raise forms.ValidationError('Only PDF, DOC, and DOCX files are allowed.')
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size cannot exceed 5 MB in Phase 1.')
        return file