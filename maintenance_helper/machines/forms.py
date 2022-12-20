from django import forms

from maintenance_helper.machines.models import Machine


class MachineEditForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ('name', 'type', 'image', 'detailed_info')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.ImageField(),

            'detailed_info': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
