import json
import re
import time
from typing import Any, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from aijobs.data.common_scraper import CommonSeleniumScraper

__all__ = ["IndeedSeleniumScraper"]

from aijobs.utils.helpers import Helper

JOB_COUNTER_CLASS_NAME: str = "jobsearch-JobCountAndSortPane-jobCount"
FIND_JOBS_BTN_CLASS_NAME: str = "yosegi-InlineWhatWhere-primaryButton"
JOB_PATTERNS: str = (
    r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});'
)
DEFAULT_LOCATION: str = "Hanoi, Vietnam"
ITEMS_PER_PAGE: int = 10
MAX_PAGES: int = 50
WHAT_INPUT_ID: str = "text-input-what"
WHERE_INPUT_ID: str = "text-input-where"


def __parse_html_source__(html: str):
    html_data = re.findall(JOB_PATTERNS, html)
    if len(html_data) == 0:
        return None
    html_data = json.loads(html_data[0])
    return html_data["metaData"]["mosaicProviderJobCardsModel"]["results"]


class IndeedSeleniumScraper(CommonSeleniumScraper):
    def __init__(
        self,
        binary: str | None = None,
        headless: bool = True,
        driver_path: str | None = None,
        browser_path: str | None = None,
    ) -> None:
        super().__init__(binary, headless, driver_path, browser_path)

    def _bypass_cloudflare_check(self):
        """
        Bypass the check screen of Cloudflare
        :return:
        """
        try:
            element = self._driver.find_element(
                By.XPATH, f"//label[@class='ctp-checkbox-label']"
            )
            element.click()
        except Exception as e:
            print(e)

    def __parse__(
        self, query: str = None, location: str = None, *args, **kwargs
    ) -> Any:
        global job_count
        url = kwargs.get("url", None)
        print(f"Visiting {url} ...")
        try:
            self._driver.get(url)
            self._bypass_cloudflare_check()
            timed_out = False
            # find the total number of jobs
            element = WebDriverWait(self._driver, 60).until(
                presence_of_element_located((By.CLASS_NAME, JOB_COUNTER_CLASS_NAME))
            )
            job_count = int(element.text.split()[0].strip())
        except Exception as e:
            print(e)
            timed_out = True
        if timed_out:
            time.sleep(1)
            try:
                element = self._driver.find_element(
                    By.XPATH, f"//input[@id='{WHAT_INPUT_ID}']"
                )
                element.click()
                element.clear()
                time.sleep(1)
                element.send_keys(query)
                # element = self._driver.find_element(
                #     By.XPATH, f"//input[@id='{WHERE_INPUT_ID}']"
                # )
                # element.click()
                # element.clear()
                # time.sleep(1)
                # element.send_keys(location)
                element = self._driver.find_element(
                    By.CLASS_NAME, FIND_JOBS_BTN_CLASS_NAME
                )
                element.click()

                # find the total number of jobs
                element = WebDriverWait(self._driver, 6).until(
                    presence_of_element_located((By.CLASS_NAME, JOB_COUNTER_CLASS_NAME))
                )
                job_count = int(element.text.split()[0].strip())
            except Exception as e:
                print(e)
                # self._driver.close()
                return None

        # get data from html
        html = self._driver.page_source
        try:
            data = __parse_html_source__(html)
        except Exception as e:
            print(e)
            # self._driver.close()
            return None
        return {"total": job_count, "data": data}

    def _parse_job_(self, view_url: str) -> Tuple[str | None, str | None]:
        """
        Parse a single job page
        :param view_url: the target job page
        :return: the title and description as a tuple
        """
        try:
            self._driver.get(view_url)
            self._bypass_cloudflare_check()
            element = WebDriverWait(self._driver, 6).until(
                presence_of_element_located(
                    (By.XPATH, "//div[@id='jobDescriptionText']")
                )
            )
            description = element.text
            element = self._driver.find_element(
                By.XPATH, "//div[@id='jobDescriptionTitle']"
            )
            title = element.text
            return title, description
        except Exception as e:
            print(e)

            return None, None

    def scrape(
        self,
        start_url: str,
        query: str,
        location: str | None,
        loop_next_page: bool = True,
    ) -> Any:
        page_count = 0
        url = (
            f"{start_url}/?q={query.replace(' ', '+')}&sort=date&l="
            f"{location.replace(' ', '+') if location is not None else DEFAULT_LOCATION}"
        )

        # page 0
        page0 = self.__parse__(url=url, query=query, location=location)
        if page0 is None:
            return None
        total_count = page0["total"]
        pages = total_count // ITEMS_PER_PAGE + (
            1 if total_count % ITEMS_PER_PAGE > 0 else 0
        )
        result = {"total": total_count, "dataList": page0["data"]}
        if loop_next_page:
            updated_url = self._driver.current_url
            while page_count < pages:
                page_count += 1
                page = self.__parse__(
                    url=f"{updated_url}&start={page_count * ITEMS_PER_PAGE}",
                    query=query,
                    location=location,
                )
                if page is None:
                    break
                result["dataList"].extend(page["data"])
        data_list = result["dataList"]
        data_set = {}
        for d in data_list:
            if d["jobkey"] in data_set:
                continue
            data_set[d["jobkey"]] = d

        for k in data_set:
            d = data_set[k]
            if "viewJobLink" not in d:
                data_set[k]["extra"] = None
                continue
            job_url = start_url + d["viewJobLink"]
            print(f"JOB URL: {job_url}")
            title, description = self._parse_job_(view_url=job_url)
            data_set[k]["extra"] = {"title": title, "description": description}
        result["dataList"] = dict(data_set)
        result["total"] = len(data_set)
        result["query"] = query
        result["location"] = None  # location
        # self._driver.close()
        return result

    def __str__(self):
        return "Indeed Selenium Scraper"
