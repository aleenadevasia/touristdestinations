from django import forms
from . models import *
from django.forms import inlineformset_factory



class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class TouristDestinationForm(forms.ModelForm):
    class Meta:
        model = TouristDestination
        fields = ['place_name', 'weather', 'state', 'district', 'category', 'google_map_link', 'description', 'main_image', 'landmark']

    def __init__(self, *args, **kwargs):
        super(TouristDestinationForm, self).__init__(*args, **kwargs)
        # Exclude nullable fields from the form
        self.fields['weather'].required = False
        self.fields['google_map_link'].required = False
        self.fields['description'].required = False
        self.fields['main_image'].required = False
        self.fields['landmark'].required = False


class DestinationSubImageForm(forms.ModelForm):
    class Meta:
        model = DestinationSubImage
        fields = ['image']

# DestinationSubImageFormSet = inlineformset_factory(TouristDestination, DestinationSubImage, form=DestinationSubImageForm, extra=1)
