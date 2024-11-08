

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl


class EmailSender:
    def __init__(self):
        pass
    
    def send_email(job, personal_info, resume_filename):
        greetings = "Dear " + job['recruiter_name'] + ',' if job['recruiter_name'] else 'Dear Hiring Team,'
        skills = job['skills'] if job['skills_present'] else personal_info['skills']
        mail_subject = "`Job application` - "+ job['title'] +" at " + job['company']
        mail_body = (greetings + "\n\n"
                 "I hope this message finds you in good spirits.\n\n"
                 "My name is " + personal_info['name'] + ", and I'm excited to submit my application for the " + job['title'] + " position at " + job['company'] + ". With my specialized skills " + skills + " and experience in this industry, I am confident in my ability to bring a fresh perspective and make a meaningful impact on your company.\n\n"
                 + personal_info['content'] +
                 "Best regards,\n"
                 + personal_info['name'] + "\n"
                 + personal_info['contact'] + "\n"
                 + personal_info['linkedin_url'] + "\n")

        message = MIMEMultipart()
        message["From"] = personal_info['name']
        message["To"] = job['recruiter_email']
        message["Subject"] = mail_subject

        message.attach(MIMEText(mail_body, "plain"))

        with open(resume_filename, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(resume_filename))
            
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(resume_filename)}"'
        message.attach(part)

        context = ssl.create_default_context()

        smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
        smtpserver.starttls()
        smtpserver.login(personal_info['email'], personal_info['password'])
        smtpserver.sendmail(personal_info['email'], job['recruiter_email'], message.as_string())