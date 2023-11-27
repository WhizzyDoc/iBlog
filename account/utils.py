import re
import random
from django.conf import Settings
from django.core.mail import send_mail

def send_reply_email(sender, receiver, name, reply, site):
    subject = f"{site} Re:"
    message = ''
    from_email = "encrane04@gmail.com"  # Sender's email
    recipient_list = [receiver]  # List of recipient emails
    html_message = f"""
    <h4>Dear {name},<h4><br><br>
    {reply}
    """

def send_password_email(receiver, name, new_password):
    subject = f"Password Reset Request"
    message = ''
    from_email = 'encrane04@gmail.com'  # Sender's email
    recipient_list = [receiver]  # List of recipient emails
    html_message = f"""
    <div style="text-align:left; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
    <h4>Dear {name},<h4><br><br>
    <p>You have requested a password reset. your new temporary password is <span style="color:blue;font-weight:600">{new_password}</span></p>
    <p>Kindly change your password after logging in.</p><br><br>
    <h4>Best Regards,<h4>
    <h4>KosmosHR.</h4>
    </div>
    """
    fail_silently = False
    send_mail(subject, message, from_email, recipient_list, fail_silently, html_message=html_message)
    
def send_new_account_email(receiver, name):
    subject = f"iBlog Registration Successful"
    message = ''
    from_email = 'rigantech@gmail.com'  # Sender's email
    recipient_list = [receiver]  # List of recipient emails
    html_message = f"""
    <div style="text-align:left; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
    <h4>Dear {name},<h4><br><br>
    <p>Your account has been successfully created on <b>iBlog</b>.</p>
    <p>If you are seeing this email, it means you have registered your account on <b>iBlog</b></p>.
    <br><br>
    <h4>Best Regards,<h4>
    <h4>iBlog Admin.</h4>
    </div>
    """
    fail_silently = False
    send_mail(subject, message, from_email, recipient_list, fail_silently, html_message=html_message)

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def generate_token():
    key = ''
    for i in range(60):
        rand_char = random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
        key += rand_char
    return key

def sterilize(s):
    s = ''.join(letter for letter in s if letter.isalnum())
    return s

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
        return False
    return True

def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9]+$'
    if re.match(pattern, username):
        return True
    else:
        return False