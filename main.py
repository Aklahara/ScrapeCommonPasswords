from urllib.request import urlopen
from html.parser import HTMLParser
from collections import deque


class MyHTMLParser(HTMLParser):
    IDLE = 0
    FOUND_DIV = 1
    RECORDING = 2

    def __init__(self) -> None:
        super().__init__()
        self.passwords = deque()
        self.status = 0

    def _update_recording(self, tag: str, increment: int) -> None:
        """
        Check the tag here because all the if statements need to check if it is <li> or <div>.
        Cannot bring self.status != 0 in here because self.status is 0 when finding the div.
        """
        if tag in ["li", "div"]:
            self.status += increment

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """
        self.status == self.FOUND_DIV is for <li>;
        any(attr[0] == "class" and attr[1] == "div-col" for attr in attrs) is finding the <div> class "div-col".
        """
        if self.status == self.FOUND_DIV \
                or any(attr[0] == "class" and attr[1] == "div-col" for attr in attrs):
            self._update_recording(tag, 1)

    def handle_endtag(self, tag: str):
        """
        <li> still appears when self.status == 0, so the numbers will go -ve if the if-statement is removed.
        """
        if self.status != self.IDLE:
            self._update_recording(tag, -1)

    def handle_data(self, data: str):
        """
        Finding the right <div> +1, finding <li> +1, so self.status == 2.
        """
        if self.status == self.RECORDING:
            self.passwords.append(data)


url: str = r"https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords"
number_s: list = [5675, 4656]

response = urlopen(url)
html = response.read().decode()

parser = MyHTMLParser()
parser.feed(html)
for num in number_s:
    if num not in range(1, 10_001):
        raise ValueError(
            f"It's 10,000 most common passwords, why would you think {num} is one of them?"
        )
    print(parser.passwords[num - 1])
