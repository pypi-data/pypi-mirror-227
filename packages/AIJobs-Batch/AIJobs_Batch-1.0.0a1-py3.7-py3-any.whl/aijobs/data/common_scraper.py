from typing import Any
import undetected_chromedriver as uc


class CommonScraper(object):
    """
    A common scraper
    """

    def __init__(self):
        pass

    def __parse__(self, url: str | None) -> Any:
        """
        The parse function
        :param url: the query URL
        :return: the object of scraped jobs in this individual page
        """
        pass

    def scrape(
        self,
        start_url: str,
        query: str,
        location: str | None,
        loop_next_page: bool = True,
    ) -> Any:
        """
        Scrape function
        :param start_url: the start url for e.g., https://vn.indeed.com/
        :param query: the job keywords, for e.g., 'ai engineer'
        :param location: the location you want to work, for e.g., 'hanoi'
        :param loop_next_page: Indeed or job sharing pages has pagination, so whether if you want to the scraper to
        loop to the next page
        :return: the object of scraped jobs.
        """
        pass

    def __str__(self):
        return "A common scraper"


class CommonSeleniumScraper(CommonScraper):
    _driver: uc.Chrome | None
    _options: uc.ChromeOptions | None
    _driver_path: str | None = None
    _browser_path: str | None = None

    def __init__(
        self,
        binary: str | None = None,
        headless: bool = True,
        driver_path: str | None = None,
        browser_path: str | None = None,
    ) -> None:
        super().__init__()

        options = uc.ChromeOptions()
        if binary is not None:
            options.binary_location = binary
        # options.headless = True
        if headless:
            options.add_argument("--headless=new")
        self._options = options

        self._driver_path = driver_path
        self._browser_path = browser_path

        self._driver = uc.Chrome(
            use_subprocess=True,
            user_multi_procs=False,
            options=self._options,
            driver_executable_path=self._driver_path,
            browser_executable_path=self._browser_path,
        )

    def __str__(self):
        return "Common Selenium Scraper"

    def close(self) -> None:
        """
        Close the current windows after use
        :return: none
        """
        if self._driver and isinstance(self._driver, uc.Chrome):
            self._driver.close()
