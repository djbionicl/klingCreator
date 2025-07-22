import requests
import json


class Authorizator:

    @property
    def cookies(self) -> str:
        return ";".join(
            [f"{Cookie.name}={Cookie.value}" for Cookie in self.__Session.cookies]
        )

    def __init__(self, sid: str = "ksi18n.ai.portal"):
        self.__SID = sid
        self.__Session = requests.Session()

    def auth(self, email: str, password: str) -> dict | None:
        AUTH_ENDPOINT = "https://id.klingai.com/pass/ksi18n/web/login/emailPassword"

        Payload = {
            "sid": self.__SID,
            "email": email,
            "password": password,
            "language": "en",
            "isWebSig4": False,
        }
        Headers = {"Content-Type": "application/x-www-form-urlencoded"}

        Response = self.__Session.post(AUTH_ENDPOINT, data=Payload, headers=Headers)

        if not Response.ok:
            print(Response.text)
            raise Exception(f"Unable to authorizate. Code: {Response.status_code}.")

        try:
            Data = json.loads(Response.text)
            self.__Session.cookies.set(
                "ksi18n.ai.portal_st", Data["ksi18n.ai.portal_st"]
            )
        except:
            pass
