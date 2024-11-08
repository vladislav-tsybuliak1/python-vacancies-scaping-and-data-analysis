import time
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response, HtmlResponse, TextResponse
from selenium import webdriver
from selenium.common import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from scraping.items import Vacancy


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_url = "https://jobs.dou.ua/vacancies/?search=python"
    headers = {"User-Agent": "Mozilla/5.0"}

    custom_settings = {
        "FEEDS": {
            "vacancies.csv": {
                "format": "csv",
                "encoding": "utf-8",
                "overwrite": True,
            }
        }
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def close(self, reason) -> None:
        self.driver.close()

    def start_requests(self) -> Request:
        self.driver.get(self.start_url)

        while True:
            try:
                more_button = self.driver.find_element(
                    By.XPATH,
                    "//div[@class='more-btn']/a[text()='Більше вакансій']"
                )
                more_button.click()
                time.sleep(2)
            except (
                TimeoutException,
                NoSuchElementException,
                ElementClickInterceptedException,
                ElementNotInteractableException
            ):
                break

        html = self.driver.page_source
        response = TextResponse(
            url=self.start_url,
            body=html,
            encoding="utf-8"
        )
        yield from self.parse(response)

    def parse(self, response: Response, **kwargs) -> Iterable[Request]:
        links = response.css(".l-vacancy .title .vt::attr(href)").getall()
        self.log(f"Total vacancies amount: {len(links)}")

        for url in response.css(".l-vacancy .title .vt::attr(href)").getall():
            self.log(f"Found URL: {url}")
            yield response.follow(
                url=url,
                headers=self.headers,
                callback=self.parse_details
            )

    def parse_details(self, response: Response) -> Vacancy:
        title = response.css(".l-vacancy .g-h2::text").get()

        vacancy_section = response.css("div.b-typo.vacancy-section")
        text_content = vacancy_section.xpath(".//text()").getall()
        description = (
            " ".join(text_content).replace("\xa0", " ").strip()
        )

        company = response.css(".b-compinfo .l-n > a::text").get()

        placing_date = response.css("div.date::text").get().strip()

        location = response.css(".place::text").get().strip()

        try:
            salary = (
                response.css("span.salary::text").get()
                .replace("\xa0", " ").strip()
            )
        except:
            salary = None

        return Vacancy(
            title=title,
            description=description,
            company=company,
            placing_date=placing_date,
            location=location,
            salary=salary
        )
