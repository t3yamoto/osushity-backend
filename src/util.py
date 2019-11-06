import pytz
from datetime import datetime

LOCAL_TIMEZONE = pytz.timezone("Japan")


def parse_last_modified(last_modified: str) -> datetime:
    utc = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S GMT").replace(
        tzinfo=pytz.utc
    )
    jst = utc.astimezone(LOCAL_TIMEZONE)
    return jst


if __name__ == "__main__":
    parse_last_modified("Mon, 07 Nov 2019 01:15:29 GMT")

