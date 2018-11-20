from django.db import models
from django.core.mail import EmailMessage
from django.core.validators import RegexValidator
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import *
import sys, os

valid_symbols = RegexValidator(r'^[a-z]*$', "Допустимы только строчные латинские символы")


class SiteSections(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[valid_symbols],
        verbose_name="Название раздела сайта",
        help_text="Укажите название раздела для сайта. Только строчные латинские буквы. Максимум 30 символов"
    )
    description = models.CharField(
        max_length=50,
        default=None,
        verbose_name="Описание",
        help_text="Введите описание для данной секции сайта. Максимум 50 символов"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел сайта",
        verbose_name_plural = "Разделы сайта"


class InformationCategory(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[valid_symbols],
        verbose_name="Название",
        help_text="Укажите название категории для новостей. Только строчные латинские буквы. Максимум 30 символов"
    )
    description = models.CharField(
        max_length=50,
        default=None,
        verbose_name="Описание",
        help_text="Введите описание данной категории. Максимум 50 символов"
    )
    image = models.ImageField(
        default=None,
        upload_to="images/default_category_news_images/",
        verbose_name="Изображение по умолчанию",
        help_text="Выберите изображение для категории, которое будет применяться ко "
                  " всем новостям категории без указания изображения ."
                  "Рекомендуемый размер изображения - 640 на 400 пикселей"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория новостей",
        verbose_name_plural = "Категории новостей"


class TopPageInformation(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name="Заголовок",
        help_text="Укажите заголовок информера. Максимум 30 символов"
    )
    description = models.CharField(
        default=None,
        max_length=30,
        verbose_name="Краткое описание",
        help_text="Укажите описание информера. Максимум 30 символов"
    )
    message = models.CharField(
        max_length=300,
        verbose_name="Сообщение",
        help_text="Тело сообщения для информера. Максимум 300 символов"
    )
    image = models.ImageField(
        upload_to="images/top_page_images/",
        verbose_name="Изображение",
        help_text="Рекомендуемый размер изображения - 920 на 720 пикселей"
    )
    link_to_site_section = models.ForeignKey(
        SiteSections,
        on_delete=models.CASCADE,
        verbose_name="Ссылка на раздел сайта",
        help_text="Выберите на какой раздел сайта будет ссылаться информер"
    )
    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заметка в заголовке страницы",
        verbose_name_plural = "Заметки в заголовке страницы"


# class Notice(models.Model):
#     category = models.ForeignKey(
#         InformationCategory,
#         on_delete=models.CASCADE,
#         verbose_name="Категория",
#         help_text="Выберите категорию, в которую попадет данная новость"
#     )
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name="Дата создания"
#     )
#     title = models.CharField(
#         max_length=70,
#         verbose_name="Заголовок",
#         help_text="Укажите заголовок новости. Максимум 30 символов"
#     )
#     preview_title = models.CharField(
#         max_length=50,
#         verbose_name="Заголовок для превью",
#         help_text="Укажите заголовок для превью новости. Максимум 50 символов"
#     )
#     use_default_image = models.BooleanField(
#         default=None,
#         verbose_name="Изображение по умолчанию",
#         help_text="Укажите использовать ли изображение по умолчанию исходя из категории новости"
#     )
#     image = models.ImageField(
#         default=None,
#         blank=True,
#         null=True,
#         upload_to="images/news_images/",
#         verbose_name="Изображение",
#         help_text="Рекомендуемый размер изображения - 640 на 400 пикселей (иначе изображение будет масштабироваться "
#                   "автоматически с возможной потерей качества)."
#     )
#     link_to_site_section = models.ForeignKey(
#         SiteSections,
#         on_delete=models.CASCADE,
#         verbose_name="Ссылка на раздел сайта",
#         help_text="Выберите на какой раздел сайта будет ссылаться данная новость"
#     )
#     description_for_link_to_site_section = models.CharField(
#         default=None,
#         max_length=50,
#         verbose_name="Описание для ссылки на раздел сайта",
#         help_text="Укажите описание для ссылки на соответствующий раздел сайта"
#     )
#     message = models.CharField(
#         max_length=500,
#         verbose_name="Сообщение",
#         help_text="Тело сообщения для новости. Максимум 500 символов"
#     )
#
#     def __str__(self):
#         return self.title
#
#     def save(self):
#         upload_image = Image.open(self.image)
#         output = BytesIO()
#         upload_image = upload_image.resize((640, 400))
#
#         upload_image.save(output, format='PNG', quality=100)
#         output.seek(0)
#
#         self.image = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.image.name.split('.')[0], 'image/png', sys.getsizeof(output), None)
#
#         super(Notice, self).save()
#
#     class Meta:
#         verbose_name = "Новость",
#         verbose_name_plural = "Новости"

class Notice(models.Model):
    category = models.ForeignKey(
        InformationCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Выберите категорию, в которую попадет данная новость"
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    title = models.CharField(
        max_length=70,
        verbose_name="Заголовок",
        help_text="Укажите заголовок новости. Максимум 30 символов"
    )
    preview_title = models.CharField(
        max_length=50,
        verbose_name="Заголовок для превью",
        help_text="Укажите заголовок для превью новости. Максимум 50 символов"
    )
    use_default_image = models.BooleanField(
        default=None,
        verbose_name="Изображение по умолчанию",
        help_text="Укажите использовать ли изображение по умолчанию исходя из категории новости"
    )
    image = models.ImageField(
        default=None,
        blank=True,
        null=True,
        upload_to="images/news_images/",
        verbose_name="Изображение",
        help_text="Рекомендуемый размер изображения - 640 на 400 пикселей (иначе изображение будет масштабироваться "
                  "автоматически с возможной потерей качества)."
    )
    link_to_site_section = models.ForeignKey(
        SiteSections,
        on_delete=models.CASCADE,
        verbose_name="Ссылка на раздел сайта",
        help_text="Выберите на какой раздел сайта будет ссылаться данная новость"
    )
    description_for_link_to_site_section = models.CharField(
        default=None,
        max_length=50,
        verbose_name="Описание для ссылки на раздел сайта",
        help_text="Укажите описание для ссылки на соответствующий раздел сайта"
    )
    message = models.CharField(
        max_length=500,
        verbose_name="Сообщение",
        help_text="Тело сообщения для новости. Максимум 500 символов"
    )

    def __str__(self):
        return self.title

    if not use_default_image:
        def save(self):
            upload_image = Image.open(self.image)
            output = BytesIO()
            upload_image = upload_image.resize((640, 400))
            upload_image.save(output, format='PNG', quality=100)
            output.seek(0)

            self.image = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.image.name.split('.')[0], 'image/png', sys.getsizeof(output), None)

            super(Notice, self).save()

    class Meta:
        verbose_name = "Новость",
        verbose_name_plural = "Новости"


class InternetTarif(models.Model):
    CHOICES_TYPE = (
        ("ethernet-tarifs", "Тариф по технологии Ethernet"),
        ("adsl-tarifs", "Тариф по технологии ADSL")
    )
    type = models.CharField(
        default=None,
        max_length=100,
        choices=CHOICES_TYPE,
        verbose_name="Тип подключения",
        help_text="Выберите тип подключенияьф данного тарифа"
    )
    title = models.CharField(
        max_length=30,
        verbose_name="Название",
        help_text="Укажите название для тарифа. Только строчные латинские буквы. Максимум 50 символов"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость",
        help_text="Укажите стоимость для данного тарифа. Максимальное значени 9999.99"
    )
    link_speed = models.CharField(
        max_length=30,
        verbose_name="Скорость",
        help_text="Укажите скорость доступа по данному тарифу"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тариф Интренет",
        verbose_name_plural = "Тарифы Интернет"


class PhoneTarif(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название направления",
        help_text="Укажите название для телефонного направления (страну, регион, населенный пункт)"
    )
    phone_code = models.IntegerField(
        verbose_name="Код направления",
        help_text="Укажите код для данного телефонного направления"
    )
    first_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость в будние дни",
        help_text="Укажите стоимость в будние дневные дни для данного тарифа. Максимальное значени 9999.99"
    )
    second_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость в вечерние часы",
        help_text="Укажите стоимость в вечернее и ночное время для данного тарифа. Максимальное значени 9999.99"
    )
    third_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость в выходные",
        help_text="Укажите стоимость в выходные и праздничные дни для данного тарифа. Максимальное значени 9999.99"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "МГ/МН тариф",
        verbose_name_plural = "МГ/МН тарифы"

class PhoneTarifFromCSV(models.Model):
    file = models.FileField(
        default=None,
        blank=None,
        null=False,
        upload_to="import/phone_tarifs/",
        verbose_name="Файл импорта МГ/МН тарифов",
        help_text="Импорт возможен только из CSV файла с разделителем ';'."
                  "Также перед импортом обязательно проверяйте кодировку (строго utf-8) структуру CSX файла на "
                  "соответствие формату - "
                  "'Название направления;Код;Стоимость в будни;Стоимость в вечернее время;Стоимость в праздники'. "
                  "В случае несоответствия формату импорт не будет выполнен либо будет выполнен с ошибками. "
    )

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Импорт МГ/МН тарифов из внешнего CSV файла"
        verbose_name_plural = "Импорт МГ/МН тарифов из внешнего CSV файла"

class Subscribe (models.Model):
    email = models.EmailField(
        max_length=100,
        verbose_name="E-mail адрес",
        help_text="Введите коректный электронный адрес для подписки"
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name="Электронный адрес для подписки",
        verbose_name_plural="Список электронных адресов для подписки"


class OperatorMail(models.Model):
    email = models.EmailField(
        max_length=100,
        verbose_name="E-mail адрес",
        help_text="Укажите электронный адрес на который следует отправлять уведомления"
    )
    description = models.CharField(
        max_length=300,
        verbose_name="Комментарий",
        help_text="Прокомментируйте принадлежность данного E-mail адреса"
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name="Электронный адрес для уведомлений",
        verbose_name_plural="Список электроных адресов для уведомлений"

class Feedback(models.Model):
    CHOICES_CATEGORIES = (
        ("Общие вопросы", "Общие вопросы"),
        ("Подключить услугу", "Подключить услугу"),
        ("Технические неполадки", "Технические неполадки")
    )
    category = models.CharField(
        max_length=100,
        choices=CHOICES_CATEGORIES,
        verbose_name="Категория обращения",
        help_text="Укажите категорию обращения пользователя"
    )
    user_name = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        help_text="Укажите как обращаться к пользователю"
    )
    user_phone = models.IntegerField(
        verbose_name="Контактный телефон пользователя",
        help_text="Укажите контактный телефон пользователя"
    )
    message = models.CharField(
        max_length=500,
        verbose_name="Сообщение пользователя",
        help_text="Введите текст сообщения пользователя"
    )
    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания",
        help_text="Дата создания обращения"
    )

    def __str__(self):
        return self.user_name + "   " + self.message[:10]

    class Meta:
        verbose_name="Обращение от пользователя",
        verbose_name_plural="Все обращения от пользователей"

class UserAlert(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок уведомления",
        help_text="Укажите заголовок для уведомления. Он будет являться темой электронного письма"
    )
    message = models.CharField(
        max_length=500,
        verbose_name="Сообщение",
        help_text="Тело сообщения уведомления. Максимум 500 символов"
    )
    image = models.ImageField(
        default=None,
        blank=True,
        null=True,
        upload_to="images/user_alerts_images/",
        verbose_name="Прикрепленное изображение",
        help_text="Рекомендуемый размер изображения - 640 на 400 пикселей до 1 мегабйта. В противном случае возможны "
                  "перебои доставки, связанные с ограничениями почтовых клиентов"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Уведомление для подписчиков"
        verbose_name_plural="Уведомления для подписчиков"

@receiver(post_save, sender=UserAlert, dispatch_uid="send_user_alert")
def send_user_alert(sender, instance, **kwargs):
    subscr_emails = list(Subscribe.objects.values_list('email', flat=True))
    # image = instance.image
    if subscr_emails:
        for subscriber in subscr_emails:
            email = EmailMessage()
            email.subject = instance.title
            email.body = instance.message
            email.from_email = "roshal_online_test_informer@bk.ru"
            email.to = [subscriber, ]
            if instance.image:
                email.attach_file(instance.image.path)
            email.send()

@receiver(post_save, sender=PhoneTarifFromCSV, dispatch_uid="import_phone_tarifs")
def import_phone_tarifs(sender, instance, **kwargs):
    if not os.path.basename(instance.file.name).split('.')[1].lower() == "csv":
        return
    file = open(instance.file.path, encoding='utf-8')
    for line in file:
        print(line)
        phone_tarif_model = PhoneTarif()
        info = line.split(';')
        if not info[4].index("(") == -1:
            third_price_correct = info[4][:info[4].index("(")]
            info[4] = third_price_correct
        phone_tarif_model.title = info[0].strip()
        phone_tarif_model.phone_code = int(info[1].strip())
        phone_tarif_model.first_price = Decimal(info[2].strip())
        phone_tarif_model.second_price = Decimal(info[3].strip())
        phone_tarif_model.third_price = Decimal(info[4].strip())
        phone_tarif_model.save()