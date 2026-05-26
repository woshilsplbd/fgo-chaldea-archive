from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ad
from django.utils import timezone


def contact(request):
    saved = request.GET.get('saved', '') == '1'

    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        message = request.POST.get('message', '').strip()

        if nickname and message:
            try:
                record = Ad.objects.create(
                    title=nickname,
                    description=message,
                    publishDate=timezone.now(),
                )
            except Exception as e:
                return HttpResponse(f'保存失败: {e}', status=500)
        return redirect('/contactApp/contact/?saved=1')

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
