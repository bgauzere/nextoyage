from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

from .models import Tache, SessionMenage


def index(request):
    task_to_do_list = Tache.objects.all()  # order_by('days_late')
    task_to_do_list = [t for t in task_to_do_list if t.due]
    task_to_do_list.sort(key=lambda t: -t.days_late)
    progression = get_progression()
    context = {
        'to_do_list': task_to_do_list,
        'progression': progression
    }
    return render(request, 'taskmanager/index.html', context)


# def index(request):
#     return HttpResponse("Hello, world. You're at the taskmanager index.")

def get_progression():
    total_minutes_per_week = get_total_per_week()
    total_minutes_last_7_days = get_total_last_7_days()
    return f"{(total_minutes_last_7_days/total_minutes_per_week)*100:.0f}"


def get_total_per_week():
    return sum([t.duration * (7/t.frequence_int) for t in Tache.objects.all()])


def get_minutes_by_days(nb_last_days=7):
    days = []
    minutes = []
    for i in range(nb_last_days, -1, -1):
        minutes_for_day = sum([s.real_duration for s in
                               SessionMenage.objects.filter(quand=timezone.now()-timezone.timedelta(days=i))])
        minutes.append(minutes_for_day)
        days.append(
            (timezone.now()-timezone.timedelta(days=i)).strftime("%A"))
    return days, minutes


def get_total_last_7_days():
    return sum([s.real_duration for s in
                SessionMenage.objects.filter(quand__gte=timezone.now()-timezone.timedelta(days=7))])


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
    total_minutes_per_week = get_total_per_week()
    total_minutes_last_7_days = get_total_last_7_days()
    progression = get_progression()
    days, minutes = get_minutes_by_days()
    print(days)
    context = {
        "days": days,
        "minutes_per_day": minutes,
        "progression": progression,
        "total_minutes_last_7_days": total_minutes_last_7_days,
        "total_minutes_per_week": round(total_minutes_per_week),

    }

    return render(request, 'taskmanager/stats.html', context)
