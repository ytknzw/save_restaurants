from googleapiclient.discovery import build

from link_check_utils import *
from gmail_utils import *
from const import URL_TEST, URL_PROD_TOKYOKANAGAWA, URL_PROD_NAGANO, URL_PROD_KANSAI,\
    CLIENT_SECRET_FILE, SENDER_ADDRESS, TO_ADDRESS, SUBJECT, TEXT


def main():
    for url in [URL_TEST, URL_PROD_TOKYOKANAGAWA, URL_PROD_NAGANO, URL_PROD_KANSAI]:
        try:
            now, file_path, type_str, nrow = run_link_check(url)
        except:
            print("Link Check Failed!")
        else:
            try:
                # Build service
                creds = gmail_auth(CLIENT_SECRET_FILE)
                service = build('gmail', 'v1', credentials=creds)

                # Create a message with attachment
                message = create_message_with_attachment(sender=SENDER_ADDRESS, to=TO_ADDRESS,
                                                         subject=f"{SUBJECT} {type_str}",
                                                         message_text=f"{url}\n{now}\n{TEXT}", file=file_path)

                # Send the message
                send_message(service=service, user_id="me", message=message)
            except:
                print("Mail Send Failed!")
            else:
                print("Mail Sent Successfully!")


if __name__ == '__main__':
    main()
