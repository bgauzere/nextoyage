from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from .models import Tache, SessionMenage


def index(request):
    task_to_do_list = Tache.objects.all()  # order_by('days_late')
    task_to_do_list = [t for t in task_to_do_list if t.due]
    task_to_do_list.sort(key=lambda t: -t.days_late)
    context = {
        'to_do_list': task_to_do_list,
    }
    return render(request, 'taskmanager/index.html', context)


# def index(request):
#     return HttpResponse("Hello, world. You're at the taskmanager index.")

def done(request):
    tache_id = request.POST['task']
    tache = get_object_or_404(Tache, pk=tache_id)
    context = {
        'tache': tache,
    }
    session = SessionMenage(tache=tache,
                            quand=datetime.today().date(),
                            real_duration=tache.duration)
    session.save()
    return HttpResponseRedirect(reverse('taskmanager:index'))


def stats(request):
    total_minutes_per_week = sum(
        [t.duration * (7/t.frequence_int) for t in Tache.objects.all()])
    context = {
        "total_minutes_per_week": total_minutes_per_week
    }
    return render(request, 'taskmanager/stats.html', context)
