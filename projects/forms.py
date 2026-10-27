from django import forms

class ProjectSearchForm(forms.Form):
    q = forms.CharField(
        required=False, max_length=80, label="Search projects",
        error_messages={"max_length": "Keep your search to 80 characters or fewer."},
        widget=forms.TextInput(attrs={
            "placeholder": "Search projects or technologies", "autocomplete": "off",
            "maxlength": "80", "aria-describedby": "search-feedback",
        }),
    )

    def clean_q(self):
        query = self.cleaned_data["q"]
        if any(ord(character) < 32 for character in query):
            raise forms.ValidationError("Use letters, numbers, and ordinary punctuation in your search.")
        return query
