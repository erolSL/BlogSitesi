from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):

    list_display = ['title', 'publishingDate', 'slug']
    list_display_links = ['title', 'publishingDate']
    list_filter = ['publishingDate']
    search_fields = ['title', 'content']

    """
        Eğer admin panelinin üzerinde değişiklik yapmak istiyorsak bunu aktifleştirmeliyiz
        Fakat list_display_link ten eklenen özellik çıkarılmalı
    """
    # list_editable = ['title']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
