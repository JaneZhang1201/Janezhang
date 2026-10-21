from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MessageForm


def contact(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for your message!")
        # Redirect so refreshing the page doesn't send the message twice.
        return redirect("contact")
    return render(request, "contact/contact.html", {"form": form})
