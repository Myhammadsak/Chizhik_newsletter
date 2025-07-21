from asgiref.sync import sync_to_async
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError


async def request_telegram_code(user):
    client = TelegramClient(StringSession(), user.telegram_api_id, user.telegram_api_hash)
    await client.connect()

    sent_code = await client.send_code_request(user.phone_number)
    session_string = client.session.save()
    phone_code_hash = sent_code.phone_code_hash

    await client.disconnect()
    return session_string, phone_code_hash


async def complete_telegram_auth(user, session_string, code, phone_code_hash, password=None):
    client = TelegramClient(StringSession(session_string), user.telegram_api_id, user.telegram_api_hash)
    await client.connect()

    try:
        await client.sign_in(user.phone_number, code, phone_code_hash=phone_code_hash)
    except SessionPasswordNeededError:
        if not password:
            raise Exception("2FA включено. Требуется пароль.")
        await client.sign_in(password=password)

    user.telegram_session_string = client.session.save()
    user.is_telegram_authenticated = True
    await sync_to_async(user.save)()

    await client.disconnect()