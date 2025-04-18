import time
from mailjet_rest import Client
import psutil


api_key = ''
api_secret = ""

# Thresholds
CPU_THRESHOLD = 2      # in %
RAM_THRESHOLD = 10     # in %
DISK_THRESHOLD = 50    # in %

def send_alert(subject, message):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                'From': {
                    'Email': "manasseh.ameyow@amalitechtraining.org",
                    'Name': "24/7 System Monitoring"
                },
                'To': [
                    {
                        'Email': "manasseh919@gmail.com",
                        'Name': "Admin"
                    }
                ],
                'Subject': subject,
                'TextPart': message,
                'HTMLPart': message  # Just a string
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print(f"Email sent successfully: {result.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_system():
    current_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    alert_message = ""

    if cpu_usage > CPU_THRESHOLD:
        alert_message += f"CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"
    if ram_usage > RAM_THRESHOLD:
        alert_message += f"RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"
    if disk_usage > DISK_THRESHOLD:
        alert_message += f"Disk space is low: {100 - disk_usage}% free (Threshold: {DISK_THRESHOLD}% free)\n"

    if alert_message:
        send_alert(f"System Alert - {formatted_time}", alert_message)
    else:
        print("All systems are normal.")
        print(f"CPU usage: {cpu_usage}%")
        print(f"RAM usage: {ram_usage}%")
        print(f"Disk space: {100 - disk_usage}% free")
        print(f"Time: {formatted_time}")


check_system()
