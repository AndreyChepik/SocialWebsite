from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # привязываем пользователя к картинке
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # перенаправляем на страницу с сохраненным изображением
            return redirect(new_item.get_absolute_url())
    else:
        # инициируется форма с информацией из гет запроса
        # эта информация будет поступать из букмарклета с помощью JS.
        # сюда будет входить url и title
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})
