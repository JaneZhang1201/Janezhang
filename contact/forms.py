from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    # Honeypot: hidden from people, but simple spam bots fill it in.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Message
        fields = ["name", "email", "message", "liked_site"]
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}
        labels = {"email": "Email (optional, if you'd like a reply)"}

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
