from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label='')

    language = forms.ChoiceField(choices=[
        # ('fr', 'French'),
        ('en', 'English'),
        # ('es', 'Spanish'),
        # ('it', 'Italian'),
        # ('pt', 'Portuguese'),
    ])
    product = forms.ChoiceField(choices=[
        ('classic', 'Classic'),
        ('shop', 'Shop'),
    ])
