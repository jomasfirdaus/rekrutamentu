from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


class JobPost(models.Model):
    PUBLISH_CHOICES = (
        ('Draft', _('Draft')),
        ('Published', _('Published')),

    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description	= RichTextField(null=False, blank=False, verbose_name=_("Description"))
    requirements	= RichTextField(null=False, blank=False, verbose_name=_("Requirements"))
    attachments = models.FileField(upload_to='job_attachments/', blank=True, null=True, verbose_name=_("Attachments"))
    image = models.ImageField(upload_to='job_images/', blank=True, null=True, verbose_name=_("Image"))
    publish_status = models.CharField(max_length=10, choices=PUBLISH_CHOICES, default='Draft', verbose_name=_("Publish Status"))
    deadline = models.DateField(null=True, blank=True, verbose_name=_("Deadline"))
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return self.title

class UserApplication(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, verbose_name=_("Job Post"))
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Aplicant"))
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Applied At"))
    STATUS_CHOICES = (
        ('Pending', _('Pending')),
        ('Review', _('Review')),
        ('Accepted', _('Accepted')),
        ('Rejected', _('Rejected')),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', verbose_name=_("Status"))
    def __str__(self):
        return f"{self.user} applied for {self.job_post.title} - {self.status}"




def get_file_upload_choices():
    file_choices = (
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('txt', 'Text File'),
        # Add more file types as needed
    )
    return file_choices



class UserAttachment(models.Model):
    application = models.ForeignKey(UserApplication, on_delete=models.CASCADE, verbose_name=_("Application"))
    upload_file = models.FileField(upload_to='Upload/', verbose_name=_("Upload dokumentu  "))

