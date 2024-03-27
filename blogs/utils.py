from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email_to_owner(user, title, file_path):
    subject = "New Blog Uploaded"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["himanshu.tech51+owner@gmail.com"]
    text_content = "A new blog has been uploaded. Check it out!"
    context = {
        'user': user,
        'title': title,
    }
    html_content = render_to_string('blog_add_mail.html', context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_file(file_path)
    msg.attach_alternative(html_content, "text/html")
    msg.send()