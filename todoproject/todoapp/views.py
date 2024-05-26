from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import TodoForm
from .models import Task


# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'obj'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'Taskdetail.html'
    context_object_name = 'i'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority')

    def get_success_url(self):
        return reverse_lazy('cbvdetails', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvtask')


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        obj = Task(name=name, priority=priority)
        obj.save()

    # Ensure obj1 includes the latest data
    obj1 = Task.objects.all()
    return render(request, 'home.html', {'obj': obj1})


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'delete.html', {'task': task})


def update(request, id):
    task = Task.objects.get(id=id)
    form = TodoForm(request.POST or None, instance=task)  # Corrected the 'request.Files' to 'request.FILES'
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'update.html', {'form': form, 'task': task})
