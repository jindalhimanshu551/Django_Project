from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_email_to_owner():
    subject = "New Blog Uploaded"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["himanshu.tech51+owner@gmail.com"]
    text_content = "A new blog has been uploaded. Check it out!"
    html_content = "<p>A new blog has been uploaded. <a href='http://127.0.0.1:8000/blogs/'>Check it out!</a></p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()