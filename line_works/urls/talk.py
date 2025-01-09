from urllib.parse import urljoin


class TalkURL:
    HOST = "https://talk.worksmobile.com"

    MY_INFO = urljoin(HOST, "/p/contact/v3/domain/contacts/my")

    SEND_MESSAGE = urljoin(HOST, "/p/oneapp/client/chat/sendMessage")
