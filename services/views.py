from django.shortcuts import render
from django.http import JsonResponse
from .models import Service, Activity, Trainer
from .forms import BookingForm


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Тут обробка даних форми
            return JsonResponse({'success': True})

        return JsonResponse({'errors': form.errors}, status=400)

    # GET-запит - показуємо пусту форму
    form = BookingForm()
    return render(request, 'services/booking.html', {'form': form})


def load_activities(request):
    """AJAX-ендпоїнт для завантаження занять по обраній послузі"""
    service_id = request.GET.get('service_id')
    if not service_id:
        return JsonResponse({'error': 'Missing service_id parameter'}, status=400)

    activities = Activity.objects.filter(service_id=service_id).values('id', 'name')
    return JsonResponse(list(activities), safe=False)


# Існуючі представлення
def fitness(request):
    return render(request, 'services/fitness.html')


def pool(request):
    return render(request, 'services/pool.html')


def yoga(request):
    return render(request, 'services/yoga.html')


def massage(request):
    return render(request, 'services/massage.html')