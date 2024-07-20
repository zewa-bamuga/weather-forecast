import random
import smtplib
import string
from email.message import EmailMessage

from app.domain.common.models import User


def Generate_Password(min_length=8, max_length=8):
    length = random.randint(min_length, max_length)
    password = generate_valid_password(length)
    return password


def generate_valid_password(length):
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    if not any(char.isdigit() for char in password):
        return generate_valid_password(length)
    if not any(char.islower() for char in password):
        return generate_valid_password(length)
    if not any(char.isupper() for char in password):
        return generate_valid_password(length)

    return password


async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #e0f7fa;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #00796b;">Добро пожаловать на сайт прогноза погоды!</h2>
            <p>Мы рады приветствовать вас на нашей платформе, где вы всегда можете получить актуальный прогноз погоды для вашего города.</p>
            <p>Наслаждайтесь точными и актуальными прогнозами погоды каждый день!</p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        "Дорогой пользователь платформы Отдела Образовательных Программ! Мы рады приветствовать тебя! Твой Отдел Образовательных Программ <3")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def send_password_reset_email(email: str, code: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Сброс пароля"
    msg['From'] = email_address
    msg['To'] = email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Сброс пароля</h2>
            <p>Здравствуйте,</p>
            <p>Вы запросили сброс пароля на платформе Отдела Образовательных Программ.</p>
            <p>Код для сброса пароля:</p>
            <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
            <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
            <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля: {code}\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
    )
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
