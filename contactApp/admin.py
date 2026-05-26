from django.contrib import admin
from .models import Ad
from django.utils.safestring import mark_safe
from .models import Resume
# Register your models here.


class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short', 'publishDate')
    search_fields = ('title', 'description')

    def description_short(self, obj):
        return obj.description[:80] + '...' if len(
            obj.description) > 80 else obj.description

    description_short.short_description = '留言内容'


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'personID', 'birth', 'edu', 'school',
                    'major', 'position', 'image_data')

    def image_data(self, obj):
        return mark_safe(u'<img src="%s" width="120px" />' % obj.photo.url)

    image_data.short_description = u'个人照片'


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Ad, AdAdmin)
