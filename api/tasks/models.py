""" Task models. """

# Django
from django.db import models


class Task(models.Model):
    ''' Task model.
    This model represents each task that the user can add.
    '''

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        # Blank and Null must be True so this field can be added automatically when the task is created.
        # In practice they will never be blank/null.
        blank=True,
        null=True,
    )

    title = models.CharField(
        'task title',
        max_length=45,
    )

    is_completed = models.BooleanField(default=False)

    date = models.DateField(auto_now_add=True)

    limit_date = models.DateField(null=True)

    def __str__(self):
        return self.title