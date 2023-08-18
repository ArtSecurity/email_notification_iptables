import subprocess
import smtplib
import time
from email.mime.text import MIMEText

email_from = 'your_email@gmail.com'
email_password = 'your_email_password'
email_to = 'recipient@example.com'  
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def get_current_iptables_rules():
    iptables_rules = subprocess.check_output(['iptables', '-L'], universal_newlines=True)
    return iptables_rules

def send_email(subject, message):
    msg = MIMEText(message)
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, email_password)
        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)

def main():
    previous_rules = set()

    while True:
        current_rules = get_current_iptables_rules().split('\n')
        current_rules = set(current_rules)

        new_rules = current_rules - previous_rules
        if new_rules:
            message = "New IP tables rules detected:\n" + "\n".join(new_rules)
            send_email("IP Tables Update", message)

            previous_rules = current_rules

        # Adjust the time interval as needed
        time.sleep(600)  # Check every 10 minutes
