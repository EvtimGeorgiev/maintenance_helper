from django import forms

from maintenance_helper.issues.models import Issue


class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('machine', 'description')


class IssueEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('machine', 'description', 'closed_on', 'closed_by')
        widgets = {
            'closed_on': forms.HiddenInput(),
            'closed_by': forms.HiddenInput(),
        }

