from django.contrib import admin

from .models import Post, Comment, UserPostMark


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


class UserMarkAdmin(admin.ModelAdmin):
    fields = ['post_id',
              'user_id',
              'mark_positive'
              ]
    list_display = ('post_id',
                    'user_id',
                    'mark_positive',
                    'id')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserPostMark, UserMarkAdmin)
