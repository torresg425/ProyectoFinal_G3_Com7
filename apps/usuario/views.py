from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
 # Create your views here.
 
class RegistroUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('apps.usuario:login')

    def form_valid(self, form):
        # Dejar que CreateView guarde el objeto con super().form_valid(form)
        response = super().form_valid(form)
        # Agregar mensaje (se mantiene a través del redirect)
        messages.success(self.request, 'Registro exitoso. Por favor inicia sesión.')
        return response


class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, 'Login exitoso')
        return reverse('index')   # redirigir al index


class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'

    def get_next_page(self):
        messages.success(self.request, 'Logout exitoso')
        return reverse('index')   # o usar next_page = 'index'
        
