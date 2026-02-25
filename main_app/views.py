from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Cat, Toy
from .forms import FeedingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# def cat_index(request):
#     cats = Cat.objects.all() 
#     return render(request, 'cats/index.html', {'cats': cats})

class CatList(ListView):
    model = Cat

# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id)
#     return render(request, 'cats/detail.html', {'cat': cat})

class CatDetail(DetailView):
    model = Cat

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     toys_cat_doesnt_have = Toy.objects.exclude(id__in = self.object.toys.all().values_list('id'))
     context['feeding_form'] = FeedingForm()
     context['toys'] = toys_cat_doesnt_have
     return context

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # success_url = reverse_lazy('cat-index')

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = reverse_lazy('cat-index')

def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = pk
        new_feeding.save()
    return redirect('cat-detail', pk=pk)

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = reverse_lazy('toy-index')

def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail',pk=cat_id)

def remove_toy(request, cat_id, toy_id):
    # Look up the cat
    # Look up the toy
    # Remove the toy from the cat
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat-detail', pk=cat_id)

