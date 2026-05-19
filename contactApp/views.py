from django.shortcuts import render


def contact(request):
    return render(request, 'contact.html', {
        'active_menu': 'employ',
        'sub_menu': 'contact',
    })


def recruit(request):
    return render(request, 'recruit.html', {
        'active_menu': 'employ',
        'sub_menu': 'recruit',
    })
