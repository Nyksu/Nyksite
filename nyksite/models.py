from django.db import models
from datetime import date

from django.urls import reverse

class Category(models.Model):
    '''Категории словаря спецификаций фотографии'''
    name = models.CharField("Категория", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        db_table = 'category'
        ordering = ['name']

class Tag(models.Model):
    '''Тэги для поиска среди текстов и фото'''
    title = models.CharField("Тег", max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        db_table = 'tag'

class Type_text(models.Model):
    '''Типы публикаций'''
    title = models.CharField("Тип публикации", max_length=100, unique=True)
    template = models.CharField("Шаблон", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тип публикации'
        verbose_name_plural = 'типы публикаций'
        db_table = 'type_text'
        ordering = ['title']


class Topic(models.Model):
    '''Наименование раздела (подраздела или книги)'''
    type_text = models.ForeignKey(Type_text, verbose_name="Тип публикации", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name="Верхний уровень", related_name='Подразделы', on_delete=models.RESTRICT, blank=True, null=True)
    name = models.CharField("Заголовок раздела", max_length=200)
    url = models.SlugField(max_length=50, unique=True, help_text="адрес URL раздела (роутинг)")
    description = models.TextField("Описание раздела", blank=True, null=True)
    redirect = models.CharField("Редирект", max_length=200, blank=True, null=True, help_text="адрес URL для безусловного перехода")
    visible = models.BooleanField('Видимость', default=True)
    template = models.CharField("Шаблон", max_length=200, default="", blank=True, null=True)

    def __str__(self):
        return "%s > %s " % ("" if self.parent is None else self.parent, self.name)

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'
        db_table = 'topic'
        ordering = ['name']


class Message(models.Model):
    '''Публикации'''
    type_text = models.ForeignKey(Type_text, verbose_name="Тип публикации", on_delete=models.RESTRICT)
    topic = models.ForeignKey(Topic, verbose_name="Раздел", on_delete=models.CASCADE)
    title = models.CharField("Заголовок публикации", max_length=200)
    url = models.SlugField(max_length=50, unique=True, help_text="адрес URL публикации (роутинг)")
    digest = models.CharField("Дайджест", max_length=500, blank=True, null=True, default="")
    content = models.TextField("Контент", blank=True, null=True, default="")
    visible = models.BooleanField('Видимость', default=True)
    date_create = models.DateField("Дата создания", default=date.today)
    date_show = models.DateField("Дата публикации", default=date.today)
    signature = models.CharField("Шаблон", max_length=100, default="", blank=True, null=True)
    book_position = models.PositiveSmallIntegerField("Порядковый номер", default=0, null=True, help_text="порядок в книге")
    _message_tag = models.ManyToManyField(Tag, through='Message_tag', verbose_name="Теги публикуации")

    def __str__(self):
        return "%s (-- %s --)" % (self.title, self.topic)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        db_table = 'message'
        get_latest_by = "date_show"
        ordering = ['book_position', 'date_show', 'title']


class Block(models.Model):
    '''Блоки публикаций'''
    title = models.CharField("Блок публикаций", max_length=200, unique=True)
    description = models.CharField("Описание", max_length=250, null=True, default="", blank=True)
    name = models.SlugField("Имя блока", max_length=50, unique=True, help_text="латиницей псевдоним блока для кода")
    template = models.CharField("Шаблон", max_length=200, default="")
    range = models.PositiveSmallIntegerField("Количество позиций в блоке", default=1, help_text="максимальное число публикаций в блоке")
    _block_position = models.ManyToManyField(Message, through='Block_position', verbose_name="Публикации в блоке")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блок публикаций'
        verbose_name_plural = 'блоки публикаций'
        db_table = 'block'


class Dictonary(models.Model):
    '''Справочник параметров съёмки'''
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.RESTRICT)
    title = models.CharField("Параметр", max_length=100)
    sortnum = models.PositiveSmallIntegerField("Порядковый номер", default=0, help_text="порядок в списке категории")
    other_status = models.BooleanField('Другое значение', default=False, help_text="отметить, если не подошёл ни один вариант")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'параметр'
        verbose_name_plural = 'параметры'
        db_table = 'dictonary'
        ordering = ['sortnum', 'title']


class Image(models.Model):
    '''Фотографии'''
    message = models.ForeignKey(Message, verbose_name="Публикация", on_delete=models.CASCADE)
    filename = models.ImageField("Изображение", upload_to="photos/")
    ordernum = models.PositiveSmallIntegerField("Порядковый номер", default=0, help_text="порядок в серии фотографий. 0 - это главное фото публикации, певое в серии : 1")
    description = models.CharField("Кэпшн", max_length=500, blank=True, null=True, default="")
    series = models.BooleanField('Признак серии фото', default=False)
    fullable = models.BooleanField('Хранение полного размера', default=True)
    miniable = models.BooleanField('Хранение миниатюры', default=False)
    _specifications = models.ManyToManyField(Dictonary, through='Specifications', verbose_name="Параметры кадра")
    _image_tag = models.ManyToManyField(Tag, through='Image_tag', verbose_name="Теги фотографий")

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'
        db_table = 'image'
        ordering = ['ordernum']


class Specifications(models.Model):
    '''Параметры кадра'''
    image = models.ForeignKey(Image, verbose_name="Фотография", on_delete=models.CASCADE)
    dictonary = models.ForeignKey(Dictonary, verbose_name="Параметр фото", on_delete=models.RESTRICT)
    other = models.CharField("Другое", max_length=50, blank=True, null=True, default="")

    def __str__(self):
        return "%s %s (%s)" % (self.other, str(self.dictonary), str(self.image))

    class Meta:
        verbose_name = 'параметр кадра'
        verbose_name_plural = 'параметры кадра'
        db_table = 'specifications'


class Message_tag(models.Model):
    '''Теги публикации'''
    tag = models.ForeignKey(Tag, verbose_name="Тег", on_delete=models.RESTRICT)
    message = models.ForeignKey(Message, verbose_name="Публикация", on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (str(self.tag), str(self.message))

    class Meta:
        verbose_name = 'теги публикации'
        verbose_name_plural = 'теги публикаций'
        db_table = 'message_tag'


class Image_tag(models.Model):
    '''Теги фотографий'''
    image = models.ForeignKey(Image, verbose_name="Фотография", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name="Тег", on_delete=models.RESTRICT)

    def __str__(self):
        return "%s (%s)" % (str(self.tag), str(self.image))

    class Meta:
        verbose_name = 'теги фотографии'
        verbose_name_plural = 'теги фотографий'
        db_table = 'image_tag'



class Block_position(models.Model):
    '''Позиции в блоке публикаций и публикации в них'''
    block = models.ForeignKey(Block, verbose_name="Блок публикаций", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, verbose_name="Публикация", blank=True, null=True, on_delete=models.SET_NULL)
    nompos = models.PositiveSmallIntegerField("Порядковый номер", default=1, help_text="порядок в блоке публикаций")

    def __str__(self):
        return "%s: %s (%s)" % (str(self.nompos), str(self.block), str(self.message))

    class Meta:
        verbose_name = 'позиция публикации в блоке публикаций'
        verbose_name_plural = 'позиции публикаций в блоке публикаций'
        db_table = 'block_position'

