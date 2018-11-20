from django.contrib import admin
from .models import SiteSections, InformationCategory, TopPageInformation, Notice, \
    InternetTarif, PhoneTarif, Subscribe, Feedback, OperatorMail, UserAlert, PhoneTarifFromCSV
from django.forms import ModelForm, Textarea


models = [
    SiteSections,
    InformationCategory,
    TopPageInformation,
    Notice,
    InternetTarif,
    PhoneTarif,
    Subscribe,
    OperatorMail,
    Feedback,
    UserAlert,
    PhoneTarifFromCSV
]

class TopPageInformationForm(ModelForm):
    class Meta:
        model = TopPageInformation
        widgets = {
            'message': Textarea(attrs={'cols': 50, 'rows': 10}),
        }
        fields='__all__'

class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        widgets = {
            'message' : Textarea(attrs={'cols': 50, 'rows': 10}),
        }
        fields = '__all__'

class CustomFormsInAdmin(admin.ModelAdmin):
    form = TopPageInformationForm
    form = NoticeForm


admin.site.site_header = "Панель администрирования портала roshalonline.ru"
admin.site.register(models, CustomFormsInAdmin)