from typing import Any, Dict, List
from httpx import Client
from bs4 import BeautifulSoup


class ContentScrapper:
    def __init__(self, url: str):
        self.client = Client()
        self.url = url
        self.data: Dict[str, Any] = {}
        self.page_content = self._get_page_content()
        self.page = BeautifulSoup(self.page_content, "html5lib", from_encoding="utf-8")
        self.body = self.page.find("body")

    def _get_page_content(self):
        response = self.client.get(self.url)
        response.raise_for_status()
        return response.content

    def get_document_metadata(self) -> Dict[str, Any]:
        first_table = self.body.find("table")
        first_table_paragraphs = first_table.find_all("p")
        second_table = first_table.find_next("table")
        second_table_paragraphs = second_table.find_all("p")
        eli_main_title = self.body.find("div", class_="eli-main-title")
        document_title = eli_main_title.find("p", {"id": "d1e42-1-1"}).text.strip()
        document_subtitle_content = eli_main_title.find_all("p")[1:]
        document_subtitle = " ".join(
            [p.text.strip() for p in document_subtitle_content]
        )
        preamble_content = self.body.find("div", class_="eli-subdivision").find_all("p")
        preamble = " ".join([p.text.strip() for p in preamble_content])

        return {
            "Doucument source": first_table_paragraphs[0].text,
            "Lang code": first_table_paragraphs[1].text,
            "Document Series": first_table_paragraphs[2].text,
            "Document Number": second_table_paragraphs[0].text,
            "Date": second_table_paragraphs[1].text,
            "Title": document_title,
            "Subtitle": document_subtitle,
            "Preamble": preamble,
        }

    def get_sections(self) -> List[Dict[str, Any]]:
        sections = self.body.find("div", {"id": "enc_1"})

        sections_and_articles = []

        # Section 1
        section_1_title = sections.find("p", {"id": "LPL.01000101-d-001"}).text.strip()
        article_1 = sections.find("div", {"id": "art_1"}).find_all("p")
        article_1_title: str = article_1[1].text.strip()
        article_1_content: str = article_1[2].text.strip()
        sections_and_articles.append(
            {
                "Section Number": 1,
                "Section Title": section_1_title,
                "Article Number": 1,
                "Article Title": article_1_title,
                "Point Number": None,
                "Subpoint Number": None,
                "Content": article_1_content,
            }
        )

        # Section 2
        section_2_title = sections.find("p", {"id": "LPL.01000101-d-002"}).text.strip()
        article_2_divs = sections.find("div", {"id": "art_2"}).find_all("div")
        article_2_title = article_2_divs[0].text.strip()
        for i, element in enumerate(article_2_divs):
            if i == 0:
                continue
            article_2_content = element.text.strip()
            sections_and_articles.append(
                {
                    "Section Number": 2,
                    "Section Title": section_2_title,
                    "Article Number": 2,
                    "Article Title": article_2_title,
                    "Point Number": i,
                    "Subpoint Number": None,
                    "Content": article_2_content[5:],
                }
            )

        # ...
