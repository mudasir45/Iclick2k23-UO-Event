from django.core.mail import EmailMessage 
from django.conf import settings



        
def send_info_mails(subeject, template, receiverMailList):
        email = EmailMessage(
            subeject,
            template, 
            settings.EMAIL_HOST_USER,
            receiverMailList
        )
        email.fail_silently = False
        email.send()
        return True