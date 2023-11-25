import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CustomLog(Audit):
    class Meta:
        db_table = 'logging'
        ordering = ('-create_datetime',)
        verbose_name_plural = verbose_name = 'Logging'

    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField()
    trace = models.TextField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    error = models.IntegerField(null=True)
    method = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.msg


class ApiLogsModel(Audit):
    time_taken = models.FloatField(default=0)
    task_name = models.CharField(max_length=255, blank=True, null=True, db_index=True)  # Mer, cheque
    request_type = models.CharField(max_length=255, blank=True, null=True)  # get post
    url = models.TextField(blank=True, null=True)
    param = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    files = models.TextField(blank=True, null=True)
    json = models.TextField(blank=True, null=True)  # remove this column later
    response = models.TextField(blank=True, null=True)
    status_code = models.CharField(max_length=5, blank=True, null=True, db_index=True)
    error = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'apilogsmodel'
