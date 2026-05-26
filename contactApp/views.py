from django.shortcuts import render, redirect
from .models import Ad
from django.utils import timezone


def contact(request):
    saved = False
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        message = request.POST.get('message', '').strip()

        if nickname and message:
            Ad.objects.create(
                title=nickname,
                description=message,
                publishDate=timezone.now(),
            )
            saved = True

    return render(request, 'contact.html', {
        'active_menu': 'employ',
        'sub_menu': 'contact',
        'saved': saved,
    })


def recruit(request):
    return render(request, 'recruit.html', {
        'active_menu': 'employ',
        'sub_menu': 'recruit',
    })
