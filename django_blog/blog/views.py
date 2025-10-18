from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin



def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date_posted')
        company = self.request.GET.get('company')
        if company:
            queryset = queryset.filter(company_name=company)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Post.objects.values_list('company_name', flat=True).distinct()
        context['selected_company'] = self.request.GET.get('company', '')
        return context

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','company_name','year','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','company_name','year','content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
