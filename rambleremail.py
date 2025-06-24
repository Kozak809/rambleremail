from imapclient import IMAPClient
import email
import time

HOST = 'imap.rambler.ru'

def process_new_messages(server):
    messages = server.search(['UNSEEN'])
    for uid, message_data in server.fetch(messages, ['RFC822']).items():
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        print(f"\nНовое письмо от: {email_message['From']}")
        print(f"Тема: {email_message['Subject']}")
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    print(f"Содержимое:\n{part.get_payload(decode=True).decode(errors='replace')}")
        else:
            print(f"Содержимое:\n{email_message.get_payload(decode=True).decode(errors='replace')}")

def connect_and_check(username, password):
    with IMAPClient(HOST) as server:
        server.login(username, password)
        server.select_folder('INBOX')
        print("Подключено к серверу.")
        
        while True:
            try:
                process_new_messages(server)
            except Exception as e:
                print(f"Ошибка при обработке сообщений: {e}")
            time.sleep(10)  # Проверяем каждые 10 секунд

if __name__ == '__main__':  # <-- тут была ошибка: должно быть __name__, а не name
    try:
        creds = input("Введите учетные данные в формате email:пароль > ")
        if ':' not in creds:
            print("Неверный формат! Используйте email:пароль")
            exit(1)
        
        username, password = creds.split(':', 1)
        connect_and_check(username, password)
    except KeyboardInterrupt:
        print("Завершаю работу.")