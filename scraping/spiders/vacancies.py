import scrapy


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?search=python"]
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


    def parse(self, response):
        pass
