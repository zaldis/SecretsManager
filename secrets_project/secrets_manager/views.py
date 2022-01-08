from django.shortcuts import redirect, render, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView
from django import forms

from .models import Secret


class AuthForm(forms.Form):
    encoding_key = forms.CharField()
    generate_new = forms.BooleanField(required=False, help_text='Old secrets will be removed')


class SecretForm(forms.ModelForm):
    class Meta:
        model = Secret
        fields = ['title', 'password', 'extra']


class LoginView(FormView):
    form_class = AuthForm
    template_name = 'secrets_manager/authenticate.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.session['encoding_key'] = form.cleaned_data['encoding_key']
            return redirect(reverse('secret-list'))
        return super().post(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            del request.session['encoding_key']
        except KeyError:
            pass
        return render(request, 'secrets_manager/logout.html', {})


class SecretCreateView(CreateView):
    model = Secret
    fields = ['title', 'extra']

    def get_success_url(self) -> str:
        return reverse('secret-list')


class SecretCreateListView(ListView):
    model = Secret
    fields = ['title', 'extra']
    context_object_name = 'secrets'
    template_name = 'secrets_manager/secret-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        form = SecretForm()
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        if 'encoding_key' not in request.session:
            return redirect(reverse('login'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SecretCreateView.as_view(
            extra_context={'secrets': self.get_queryset()},
            template_name=self.template_name
        )
        return view(request, *args, **kwargs)


class SecretUpdateView(UpdateView):
    pass


class SecretDeleteView(DeleteView):
    pass
