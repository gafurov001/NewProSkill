from twilio.rest import Client

from config import conf


def send_sms(text: str = "Hello World", receiver: str = '+998330073223'):
    try:
        client = Client(conf.ACCOUNT_SID, conf.AUTH_TOKEN)
        message = client.messages.create(body=text, from_="+15705548206", to=receiver)
        if message.status in [200, 201]:
            return True
        else:
            return message.status
    except Exception as e:
        return e


def main() -> None:
    send_sms()


if __name__ == "__main__":
    main()




