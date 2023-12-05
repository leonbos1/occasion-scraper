import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..extensions import email, email_password

def send_email(cars: list, emails, subject):
    from_email = email
    password = email_password

    content = get_mail_content(cars)

    for mail in emails:
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = mail
        message["Subject"] = f"Nieuwe auto's op autoscout24.nl - {subject}"

        message.attach(MIMEText(content, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, password)
            smtp.sendmail(from_email, mail, message.as_string())


def get_mail_content(cars: list):
    if len(cars) == 0:
        return "Geen nieuwe auto's gevonden"
    
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
        content += f"<td style='border: 1px solid black; padding: 5px;'><img src='{car.base_image}'></td>"

        content += "</tr>"

    return content