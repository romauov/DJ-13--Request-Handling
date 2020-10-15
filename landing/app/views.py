from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing_src = request.GET.get('from-landing')
    if landing_src:
        counter_click[landing_src] += 1
    print(counter_click) #у меня почему-то не работают эти принты, в чём может быть причина?
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    landing_src = request.GET.get('from-landing', 'no-landing')
    if landing_src == 'original':
        counter_show[landing_src] += 1
        print(counter_show)
        return render(request, 'landing.html')
    if landing_src == 'test':
        counter_show[landing_src] += 1
        print(counter_show)
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    try:
        test_ratio = counter_click['test'] / counter_show['test']
    except:
        test_ratio = 0

    try:
        original_ratio = counter_click['original'] / counter_show['original']
    except:
        original_ratio = 0

    return render(request, 'stats.html', context={
        'test_conversion': test_ratio,
        'original_conversion': original_ratio,
    })
