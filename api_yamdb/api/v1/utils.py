import uuid
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_YAMDB


def get_and_send_confirmation_code(user):
    user.update(confirmation_code=str(uuid.uuid4()).split("-")[0])
    send_mail(
        'Код подтверждения',
        (f'Код подтверждения для пользователя "{user[0].username}":'
         f' {user[0].confirmation_code}'),
        EMAIL_YAMDB,
        [user[0].email]
    )
