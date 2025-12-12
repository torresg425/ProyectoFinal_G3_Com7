from django.shortcuts import redirect
from .models import Noticia, Comentario
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from .forms import ComentarioForm


# Create your views here.

#def noticias(request):
#    noticias = Noticia.objects.all()
#    return render (request, 'noticas.html', {'noticias' : noticias})

## Vista basada en clases
class NoticiaListView(ListView):
    model = Noticia
    template_name = "noticias/noticias.html"
    context_object_name = 'noticias'
    

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = "noticias/noticia_individual.html"
    context_object_name = 'noticias'
    pk_url_kwarg = 'id'
    queryset = Noticia.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(noticias_id = self.kwargs['id'])
        return context
    
    def noticia(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit = False)
            comentario.usuario = request.user
            comentario.noticias_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.noticias:noticia_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
        
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html' 
    success_url = 'comentario/comentarios/'  
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.noticias_id = self.kwargs['noticias_id']
        return super().form_valid(form)     

    
