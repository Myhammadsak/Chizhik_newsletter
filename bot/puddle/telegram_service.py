import os
import random
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio

log_store = {}


def log_message(username, message):
    if username not in log_store:
        log_store[username] = []
    log_store[username].append(message)


async def send_newsletter_for_user_data(session_string, api_id, api_hash, chat_links, text,
                                        file, file2, file3, file4, file5, username):
    client = TelegramClient(StringSession(session_string), api_id, api_hash)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            log_message(username, "Сессия недействительна")
            return

        log_message(username, "Начинаем рассылку")

        processed_links = []
        current_index = 0

        while current_index < len(chat_links):
            link = chat_links[current_index].strip()
            log_message(username, f"Пытаемся отправить в {link}")

            try:
                delay = random.randint(10, 16)
                await asyncio.sleep(delay)

                entity = None

                # Обработка инвайт-ссылок (начинаются с +)
                if link.startswith(("https://t.me/+", "t.me/+", "+")):
                    try:
                        invite_hash = link.split("+")[-1].split("/")[-1]
                        await client(ImportChatInviteRequest(invite_hash))
                        log_message(username, f"Вступили по инвайту в {link}")
                        entity = await client.get_entity(f"https://t.me/+{invite_hash}")
                    except errors.UserAlreadyParticipantError:
                        log_message(username, f"Уже в группе ({link})")
                        entity = await client.get_entity(f"https://t.me/+{invite_hash}")
                    except Exception as e:
                        log_message(username, f"Ошибка вступления в {link}: {str(e)}")
                        current_index += 1
                        continue

                else:
                    try:
                        normalized_link = link.replace("@", "").replace("https://t.me/", "").replace("t.me/", "")
                        entity = await client.get_entity(normalized_link)

                        try:
                            await client(JoinChannelRequest(entity))
                            log_message(username, f"Вступили в публичную группу {link}")
                        except errors.UserAlreadyParticipantError:
                            log_message(username, f"Уже в группе ({link})")
                    except Exception as e:
                        log_message(username, f"Ошибка вступления в {link}: {str(e)}")
                        current_index += 1
                        continue

                if not entity:
                    log_message(username, f"Не удалось получить entity для {link}")
                    current_index += 1
                    continue

                files = []
                for f in [file, file2, file3, file4, file5]:
                    if f and hasattr(f, 'path') and os.path.exists(f.path):
                        files.append(f.path)

                try:
                    if files and text:
                        await client.send_message(entity, text, file=files)
                        log_message(username, f"Отправлено текст+файл в {link}")
                    elif files:
                        await client.send_message(entity, file=files)
                        log_message(username, f"Отправлен файл в {link}")
                    elif text:
                        await client.send_message(entity, text)
                        log_message(username, f"Отправлен текст в {link}")
                    else:
                        log_message(username, f"Нечего отправлять в {link}")
                        current_index += 1
                        continue

                    processed_links.append(link)
                    current_index += 1

                except errors.FloodWaitError as e:
                    log_message(username, f"Флуд-контроль при отправке: ждем {e.seconds} сек.")
                    await asyncio.sleep(e.seconds)
                    continue
                except errors.ChatWriteForbiddenError:
                    log_message(username, f"Нет прав на отправку в {link}")
                    current_index += 1
                    continue
                except Exception as e:
                    log_message(username, f"Ошибка отправки в {link}: {str(e)}")
                    current_index += 1
                    continue

            except Exception as e:
                log_message(username, f"Общая ошибка обработки {link}: {str(e)}")
                current_index += 1
                continue

    except Exception as e:
        log_message(username, f"Критическая ошибка: {str(e)}")
    finally:
        await client.disconnect()
        log_message(username, f"Рассылка завершена. Обработано групп: {len(processed_links)}/{len(chat_links)}")