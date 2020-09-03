# Generated by Django 3.1 on 2020-08-31 12:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Блок публикаций')),
                ('description', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Описание')),
                ('name', models.SlugField(help_text='латиницей псевдоним блока для кода', unique=True, verbose_name='Имя блока')),
                ('template', models.CharField(default='', max_length=200, verbose_name='Шаблон')),
                ('range', models.PositiveSmallIntegerField(default=1, help_text='максимальное число публикаций в блоке', verbose_name='Количество позиций в блоке')),
            ],
            options={
                'verbose_name': 'блок публикаций',
                'verbose_name_plural': 'блоки публикаций',
                'db_table': 'block',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'db_table': 'category',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dictonary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Параметр')),
                ('sortnum', models.PositiveSmallIntegerField(default=0, help_text='порядок в списке категории', verbose_name='Порядковый номер')),
                ('other_status', models.BooleanField(default=False, help_text='отметить, если не подошёл ни один вариант', verbose_name='Другое значение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nyksite.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'параметр',
                'verbose_name_plural': 'параметры',
                'db_table': 'dictonary',
                'ordering': ['sortnum', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.ImageField(upload_to='photos/', verbose_name='Изображение')),
                ('ordernum', models.PositiveSmallIntegerField(default=0, help_text='порядок в серии фотографий. 0 - это главное фото публикации, певое в серии : 1', verbose_name='Порядковый номер')),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Кэпшн')),
                ('series', models.BooleanField(default=False, verbose_name='Признак серии фото')),
                ('fullable', models.BooleanField(default=True, verbose_name='Хранение полного размера')),
                ('miniable', models.BooleanField(default=False, verbose_name='Хранение миниатюры')),
            ],
            options={
                'verbose_name': 'фотография',
                'verbose_name_plural': 'фотографии',
                'db_table': 'image',
                'ordering': ['ordernum'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок публикации')),
                ('url', models.SlugField(help_text='адрес URL публикации (роутинг)', unique=True)),
                ('digest', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Дайджест')),
                ('content', models.TextField(blank=True, default='', null=True, verbose_name='Контент')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('date_create', models.DateField(default=datetime.date.today, verbose_name='Дата создания')),
                ('date_show', models.DateField(default=datetime.date.today, verbose_name='Дата публикации')),
                ('signature', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Шаблон')),
                ('book_position', models.PositiveSmallIntegerField(default=0, help_text='порядок в книге', null=True, verbose_name='Порядковый номер')),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'публикации',
                'db_table': 'message',
                'ordering': ['book_position', 'date_show', 'title'],
                'get_latest_by': 'date_show',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Type_text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Тип публикации')),
                ('template', models.CharField(max_length=200, verbose_name='Шаблон')),
            ],
            options={
                'verbose_name': 'тип публикации',
                'verbose_name_plural': 'типы публикаций',
                'db_table': 'type_text',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Заголовок раздела')),
                ('url', models.SlugField(help_text='адрес URL раздела (роутинг)', unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание раздела')),
                ('redirect', models.CharField(blank=True, help_text='адрес URL для безусловного перехода', max_length=200, null=True, verbose_name='Редирект')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('template', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Шаблон')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='nyksite.topic', verbose_name='Верхний уровень')),
                ('type_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.type_text', verbose_name='Тип публикации')),
            ],
            options={
                'verbose_name': 'раздел',
                'verbose_name_plural': 'разделы',
                'db_table': 'topic',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Specifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Другое')),
                ('dictonary', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nyksite.dictonary', verbose_name='Параметр фото')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.image', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'параметр кадра',
                'verbose_name_plural': 'параметры кадра',
                'db_table': 'specifications',
            },
        ),
        migrations.CreateModel(
            name='Message_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.message', verbose_name='Публикация')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nyksite.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'теги публикации',
                'verbose_name_plural': 'теги публикаций',
                'db_table': 'message_tag',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='_message_tag',
            field=models.ManyToManyField(through='nyksite.Message_tag', to='nyksite.Tag', verbose_name='Теги публикуации'),
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.topic', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='message',
            name='type_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nyksite.type_text', verbose_name='Тип публикации'),
        ),
        migrations.CreateModel(
            name='Image_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.image', verbose_name='Фотография')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='nyksite.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'теги фотографии',
                'verbose_name_plural': 'теги фотографий',
                'db_table': 'image_tag',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='_image_tag',
            field=models.ManyToManyField(through='nyksite.Image_tag', to='nyksite.Tag', verbose_name='Теги фотографий'),
        ),
        migrations.AddField(
            model_name='image',
            name='_specifications',
            field=models.ManyToManyField(through='nyksite.Specifications', to='nyksite.Dictonary', verbose_name='Параметры кадра'),
        ),
        migrations.AddField(
            model_name='image',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.message', verbose_name='Публикация'),
        ),
        migrations.CreateModel(
            name='Block_position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nompos', models.PositiveSmallIntegerField(default=1, help_text='порядок в блоке публикаций', verbose_name='Порядковый номер')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nyksite.block', verbose_name='Блок публикаций')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nyksite.message', verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'теги фотографии',
                'verbose_name_plural': 'теги фотографий',
                'db_table': 'block_position',
            },
        ),
        migrations.AddField(
            model_name='block',
            name='_block_position',
            field=models.ManyToManyField(through='nyksite.Block_position', to='nyksite.Message', verbose_name='Публикации в блоке'),
        ),
    ]