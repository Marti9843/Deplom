from django import forms
from .models import Service, Activity, Trainer


class BookingForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Послуга",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    activity = forms.ModelChoiceField(
        queryset=Activity.objects.none(),
        label="Заняття",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        label="Тренер",
        widget=forms.Select(attrs={'class': 'form-control'})
    )