from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class TitleAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
