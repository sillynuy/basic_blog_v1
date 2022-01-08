from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    fields = ['date_published',
              'headline',
              'pos_marks',
              'neg_marks',
              'rating'
              ]
    list_display = ('headline',
                    'date_published',
                    'pos_marks',
                    'neg_marks',
                    'rating')


class CommentAdmin(admin.ModelAdmin):
    fields = ['post_id',
              'author',
              'date_published',
              'text'
              ]
    list_display = ('post_id',
                    'author',
                    'date_published',
                    'text'
                    )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
