from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import SiteSections, InformationCategory, TopPageInformation, Notice, \
    InternetTarif, PhoneTarif, Subscribe, Feedback, OperatorMail
from django.template.context_processors import csrf

import datetime
import json

# Create your views here.

def home(request):

    """ Rendering a roshalonline home page """

    author = "Kineev Alexey"
    site_sections = SiteSections.objects.all()
    info_categories = InformationCategory.objects.all()
    top_page_informers = TopPageInformation.objects.all().order_by('-creation_date')[:3]
    news = Notice.objects.all().order_by('-creation_date')[:9]
    internet_tarifs = InternetTarif.objects.all()
    phone_tarifs = PhoneTarif.objects.all()

    return render(
        request,
        'home.html',
        {
            'sections' : site_sections,
            'categories' : info_categories,
            'top_informers' : top_page_informers,
            'news' : news,
            'internet_tarifs' : internet_tarifs,
            'phone_tarifs' : phone_tarifs,
            'year' : datetime.datetime.now().year,
            'author' : author
        }
    )

def phone_calls(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        phone_direction = PhoneTarif.objects.filter(phone_code__icontains=q)
        results = []
        for ph_dir in phone_direction:
            call_json = {}
            call_json = str(ph_dir.phone_code) + " - " + ph_dir.title
            results.append(call_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mime_type = 'application/json'
    return HttpResponse(data, mime_type)

def calulated_phone_tarif(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST" and request.is_ajax():
        req = request.POST.get('direction', '')
        code_date = int(str.split(req, ' - ')[0])
        phone_tarif = PhoneTarif.objects.filter(phone_code__exact=code_date)
        prices = None
        for t in phone_tarif:
            # prices = "Будний день с 8:00 до 20:00 - " + str(t.first_price) + " руб/мин   Будний день с 20:00 до 8:00 - " \
            #          + str(t.second_price) + " руб/мин   Праздничный или выходной день - " + \
            #          str(t.third_price) + " руб/мин"
            prices = "Будний день с 8:00 до 20:00 - %s руб. за 1 минуту<br />Будний день с 20:00 до 8:00 - %s руб. " \
                     "за 1 минуту <br />Праздничный или выходной день - %s руб. за 1 минуту <br />" % \
                     (str(t.first_price), str(t.second_price), str(t.third_price))
        if(prices != None):
            return HttpResponse(prices)
        else:
            return HttpResponse("К сожалению, телефонного направления с таким кодом не существует. Проверьте "
                                "правильность ввода или корректность телефонного кода", c)
    else:
        return HttpResponse("BAD")

def subscribe(request):

    if request.method == "POST" and request.is_ajax():
        email_from_subscribe_form = request.POST.get('email', '')
        subscrb = Subscribe(
            email=email_from_subscribe_form
        )
        subscrb.save()
        send_mail(
            "Спасибо, что подписались на расслыку от Roshalonline",
            "Уважаемый клиент, Вы осуществили подписку на автоматическую рассылку новостей от комапании Roshalonline"
            " (ООО 'Альтес-Р') с сайта http://www.roshalonline.ru Пожалуйста, не отвечайте на данное письмо."
            " С уважением, команда Roshalonline",
            "roshal_online_test_informer@bk.ru",
            [email_from_subscribe_form],
            fail_silently=False
        )

        return HttpResponse("OK")
    else:
        return HttpResponse("BAD")

def feedback(request):
    if request.method == "POST" and request.is_ajax():
        message_category = request.POST.get('category', '')
        message_user_name = request.POST.get('name', '')
        message_phone = request.POST.get('tel', '')
        message_text = request.POST.get('comment', '')
        new_feedback = Feedback(
            category=message_category,
            user_name=message_user_name,
            user_phone=message_phone,
            message=message_text,
            creation_date=datetime.datetime.now()
        )
        new_feedback.save()

        operator_emails = OperatorMail.objects.values_list('email', flat=True)
        send_mail(
            "Новое обращение от пользователя " + message_user_name + "( " + message_category + " )",
            message_text + " Прошу связаться со мной по телефону - " + str(message_phone),
            "roshal_online_test_informer@bk.ru",
            list(operator_emails),
            fail_silently=False
        )

        return HttpResponse("OK")
    else:
        return HttpResponse("BAD")