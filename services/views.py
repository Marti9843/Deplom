from django.shortcuts import render

def booking(request):
    return render(request, 'services/booking.html')

def fitness(request):
    return render(request, 'services/fitness.html')

def pool(request):
    return render(request, 'services/pool.html')

def yoga(request):
    return render(request, 'services/yoga.html')

def massage(request):
    return render(request, 'services/massage.html')