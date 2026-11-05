# app/models.py
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    signed_pdf = models.FileField(upload_to='signed_pdfs/%Y/%m/%d', null=True, blank=True)
    cms_file = models.FileField(upload_to='cms_sigs/%Y/%m/%d', null=True, blank=True)
