from urllib.parse import urljoin


class AuthURL:
    HOST = "https://auth.worksmobile.com"

    LOGIN_PROCESS_V2 = urljoin(HOST, "/login/loginProcessV2")
