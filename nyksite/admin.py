from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Type_text, Topic, Message, Block, Dictonary, Image, \
    Specifications, Message_tag, Image_tag, Block_position

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Type_text)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Block)
admin.site.register(Dictonary)
admin.site.register(Image)

admin.site.register(Specifications)
admin.site.register(Message_tag)
admin.site.register(Image_tag)
admin.site.register(Block_position)