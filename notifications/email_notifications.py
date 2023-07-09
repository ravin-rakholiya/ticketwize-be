from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
# from notification.consts import EMAIL_MESSAGES
from django.template.loader import get_template


def send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails):
    mail_content = mail_content
    try:
        with open(settings.ROOT_DIR + txt_template_path) as f:
            full_msg = f.read()
        message = EmailMultiAlternatives(subject=subject, body=full_msg, from_email=from_email, to=to_emails)
        html_template = get_template(html_template_path).render(mail_content)
        message.attach_alternative(html_template, 'text/html')
        message.send()
    except Exception as e:
        print(e)
        pass


def send_mail_without_template(mail_content, subject, from_email, to_emails):
    mail_content = mail_content
    email_res = send_mail(subject, mail_content, from_email, to_emails, fail_silently=False)


def send_login_otp(otp, to_emails, from_email='ravinkumarrakh@gmail.com'):
    subject = "TicketWize: OTP for Sign In"
    mail_content = {'otp': otp}
    txt_template_path = "templates/custom_emails/otp/login_otp.txt"
    html_template_path = "custom_emails/otp/login_otp.html"
    send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails)


def send_email_verify_otp(otp, to_emails, from_email='ravinkumarrakh@gmail.com'):
    subject = "TicketWize: OTP To Verify email"
    mail_content = {'otp': otp}
    txt_template_path = "templates/custom_emails/otp/verify_email.txt"
    html_template_path = "custom_emails/otp/verify_email.html"
    send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails)


def send_signup_otp(otp, to_emails, from_email='ravinkumarrakh@gmail.com'):
    subject = "TicketWize: OTP for Signup"
    mail_content = {'otp': otp}
    txt_template_path = "templates/custom_emails/otp/signup_otp.txt"
    html_template_path = "custom_emails/otp/signup_otp.html"
    send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails)


def send_reset_password_otp(otp, to_emails, from_email='ravinkumarrakh@gmail.com'):
    subject = "TicketWize: OTP to Reset"
    mail_content = {'otp': otp}
    txt_template_path = "templates/custom_emails/otp/reset_password_otp.txt"
    html_template_path = "custom_emails/otp/reset_password_otp.html"
    send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails)


def send_report_user_notification(mail_content, subject, from_email='ravinkumarrakh@gmail.com',
                                  to_emails=["ravinrakholiya559@gmail.com"]):
    subject = "User Reported"
    mail_content = mail_content
    send_mail_without_template(mail_content, subject, from_email, to_emails)
