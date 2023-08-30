import re
import sys
import base64
import requests
import logging
from typing import NamedTuple, Union, List
from datetime import datetime

from cli.colors import colored
from cli.ascii_table import print_file_details

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api2.qrshare.io"


# BASE_URL = "http://localhost:8080"


class TextToQR(NamedTuple):
    n0: int
    x: int
    c: str


class UploadResponse(NamedTuple):
    success: bool
    filename: str
    url: str
    errorMessage: Union[str, None]
    contentType: str
    size: int
    uploadedAt: datetime
    expiresAt: datetime
    jqr: dict


def upload(filename: str) -> UploadResponse:
    print(f"Uploading: {colored(filename)}...")
    with open(filename, "rb") as f:
        data = {"file": (re.split(r"/|\\", filename)[-1], f)}
        response = requests.post(f"{BASE_URL}/api/upload", files=data)
        response_content = response.json()

        logger.debug(f"{response.status_code}\n{response_content}")

        if response.ok:
            return UploadResponse(**response_content)
        else:
            return UploadResponse(success=False, errorMessage=f"{response.status_code}: {response.reason}")


def generate_ascii_qr_code(qr: TextToQR, margin: int = 2) -> List[str]:
    decoded = bytes(base64.b64decode(qr.c)).decode('utf-8')
    binary = ''.join(list(map(lambda b: bin(ord(b)).replace('0b', '').zfill(8), decoded)))
    binary = binary[qr.n0:]

    x = qr.x

    rows = []
    rows.extend(['  ' * (x + margin * 2) for _ in range(margin)])

    for i in range(x):
        row = binary[i * x:(i + 1) * x]
        row = ''.join(list(map(lambda c: '█' * 2 if c == '1' else '  ', row)))
        rows.append(('  ' * margin) + row + ('  ' * margin))

    rows.extend(['  ' * (x + margin * 2) for _ in range(margin)])

    return rows


def main():
    if len(sys.argv) != 2:
        print(f"Usage: qrs <filename>")
        sys.exit(-1)

    response = upload(sys.argv[1])
    code = generate_ascii_qr_code(TextToQR(**response.jqr))
    for line in code:
        print(colored(line))

    print_file_details(response.filename, response.size, response.url)
    print()


if __name__ == "__main__":
    main()
