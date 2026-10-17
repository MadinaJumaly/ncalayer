# views.py

from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage

def my_view(request):
    message = 'Upload as many files as you want!'

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'list.html', {
        'form': form,
        'documents': documents,
        'message': message,
    })

@csrf_exempt
def sign_document(request):
    import json
    if request.method == "POST":
        data = json.loads(request.body)
        doc_id = data.get('doc_id')
        signature_b64 = data.get('signature')
        email = data.get('email', "")
        doc = Document.objects.get(pk=doc_id)
        filename = doc.docfile.name.split("/")[-1] + ".cms"
        cms_file = ContentFile(base64.b64decode(signature_b64), name=filename)
        doc.cms_file.save(filename, cms_file, save=True)
        # Optionally, send by email immediately
        if email:
            send_signature_by_email(email, doc)
            doc.email_sent = True
            doc.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def send_email_view(request):
    import json
    if request.method == "POST":
        data = json.loads(request.body)
        doc_id = data.get('doc_id')
        email = data.get('email')
        doc = Document.objects.get(pk=doc_id)
        send_signature_by_email(email, doc)
        doc.email_sent = True
        doc.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "POST only"}, status=405)

def send_signature_by_email(email, doc):
    subject = "Your signed document"
    message = "Please find the attached signature (.cms file) for your document."
    mail = EmailMessage(subject, message, to=[email])
    if doc.cms_file:
        mail.attach(doc.cms_file.name, doc.cms_file.read())
    mail.send()
