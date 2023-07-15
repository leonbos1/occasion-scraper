import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_email(cars: list, credentials, emails):
    from_email = credentials["email"]
    password = credentials["email_password"]

    content = get_mail_content(cars)

    for email in emails:
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = email
        message["Subject"] = "Nieuwe auto's op autoscout24"

        message.attach(MIMEText(content, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, password)
            smtp.sendmail(from_email, email, message.as_string())


def get_mail_content(cars: list):
    content = ""

    content += "<table style='border: 1px solid black; border-collapse: collapse;'>"
    content += "<tr>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Merk</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Model</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Prijs</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Kilometerstand</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Bouwjaar</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>Locatie</th>"
    content += "<th style='border: 1px solid black; padding: 5px;'>URL</th>"
    content += "</tr>"

    for car in cars:
        content += "<tr>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.brand}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.model}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>€{car.price}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.mileage}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.first_registration}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'>{car.location}</td>"
        content += f"<td style='border: 1px solid black; padding: 5px;'><a href='{car.url}'>Link</a></td>"
        # image
        content += f"<td style='border: 1px solid black; padding: 5px;'><img src='data:image/png;base64,{base64.b64encode(car.image).decode('utf-8')}'></td>"

        content += "</tr>"

    return content