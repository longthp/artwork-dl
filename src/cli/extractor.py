from .settings import DOMAINS
from bs4 import BeautifulSoup
from typing import Callable
import dataclasses
import httpx
import pathlib
import re
import urllib.parse

@dataclasses.dataclass
class Artwork:
    title: str
    url: str


class UrlFilterer:
    def __init__(
        self,
        allowed_domains: set[str] | None = None,
        allowed_schemes: set[str] | None = None
    ) -> None:
        self.allowed_domains = allowed_domains
        self.allowed_schemes = allowed_schemes

    def filter_url(self, url: str) -> tuple[str, str] | None:
        parsed = urllib.parse.urlsplit(url)
        domain = parsed.netloc

        if (self.allowed_schemes is not None
                and parsed.scheme not in self.allowed_schemes):
            print(f"[warn] Invalid scheme: {url}")
            return None
        if (self.allowed_domains is not None
                and domain not in self.allowed_domains):
            print(f"[warn] URL not supported: {url}")
            return None

        return (url, domain)


class ArtworkExtractor:
    def __init__(
        self,
        client: httpx.Client,
        url: str,
        filter_url: Callable[[str], str | None],
        image_root: pathlib.Path
    ) -> None:
        self.url = url
        self.client = client
        self.filter_url = filter_url
        self.image_root = image_root

    @staticmethod
    def make_request(client: httpx.Client, url: str) -> tuple[httpx.Response, BeautifulSoup]:
        try:
            response = client.request(method="GET", url=url)
            response.raise_for_status()

            soup = BeautifulSoup(markup=response.text, features="html.parser")

            return (response, soup)

        except httpx.HTTPStatusError:
            print(f"[error] Request error: {url}")

    def write_image(self, image_content: bytes, title: str) -> int:
        image_ext = ".jpg"
        image_path = self.image_root / (title + image_ext)
        print(f"[download] {image_path}")

        if image_path.exists():
            print(f"[warn] File existed: {image_path}")
        else:
            with open(file=image_path, mode="wb") as f:
                f.write(image_content)

    def extract_artwork(self, soup: BeautifulSoup) -> Artwork:
        selectors = {
            "image": "meta[name$=':image'], meta[property$=':image']",
            "title": "meta[name$=':title'], meta[property$=':title']",
        }

        image_tags = soup.select(selector=selectors["image"])
        title_tags = soup.select(selector=selectors["title"])

        try:
            image_url = image_tags[0].get(key="content", default=None)
            title_content = title_tags[0].get(key="content", default=None)

            return Artwork(title=title_content, url=image_url)

        except AttributeError:
            print("Not found")

    def force_dimensions(self, domain: str, url: str) -> str:
        if (domain == DOMAINS["APPLE_MUSIC"]
                or domain == DOMAINS["DEEZER"]):
            new_url = re.sub(pattern=r'\d+x\d+[a-z]*(-60)?', repl="1400x1400", string=url)
            return new_url

        return url

    def run(self) -> None:
        url, domain = self.filter_url(self.url) or (None, None)

        if url is not None:
            _, soup = self.make_request(client=self.client, url=url)
            artwork = self.extract_artwork(soup)

            artwork_url = self.force_dimensions(domain=domain, url=artwork.url)
            print(f"[extract] {artwork_url}")

            response, _ = self.make_request(client=self.client, url=artwork_url)
            self.write_image(image_content=response.content, title=artwork.title)


def main(url: str) -> None:
    # url = "https://www.deezer.com/us/album/334062617"

    filterer = UrlFilterer(
        allowed_domains=set(DOMAINS.values()),
        allowed_schemes=set(["https", "http"])
    )

    with httpx.Client() as client:
        extractor = ArtworkExtractor(
            client=client,
            url=url,
            filter_url=filterer.filter_url,
            image_root=pathlib.Path("D:/Music/artwork/tmp")
        )
        extractor.run()


if __name__ == "__main__":
    main()
