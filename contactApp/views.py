from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AdForm
from .models import Ad
from django.utils import timezone


def contact(request):
    saved = request.GET.get('saved', '') == '1'
    form = AdForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            Ad.objects.create(
                title=form.cleaned_data['nickname'],
                description=form.cleaned_data['message'],
                contact_info=form.cleaned_data['contact_info'],
                publishDate=timezone.now(),
            )
        except Exception as e:
            return HttpResponse(f'保存失败: {e}', status=500)
        return redirect('/contactApp/contact/?saved=1')

    return render(request, 'contact.html', {
        'active_menu': 'employ',
        'sub_menu': 'contact',
        'saved': saved,
        'form': form,
    })


def recruit(request):
    return render(request, 'recruit.html', {
        'active_menu': 'employ',
        'sub_menu': 'recruit',
    })
