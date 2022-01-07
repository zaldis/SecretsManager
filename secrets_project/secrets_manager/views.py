from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Secret


class SecretCreateView(CreateView):
    pass


class SecretListView(ListView):
    pass


class SecretCreateListView(CreateView, ListView):
    model = Secret
    fields = ['title', 'password', 'extra']
    context_object_name = 'secrets'
    template_name = 'secrets_manager/secret-list.html'


class SecretUpdateView(UpdateView):
    pass


class SecretDeleteView(DeleteView):
    pass
