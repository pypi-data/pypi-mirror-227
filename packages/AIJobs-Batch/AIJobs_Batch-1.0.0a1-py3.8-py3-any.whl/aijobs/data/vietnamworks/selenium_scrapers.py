import json
import time
from typing import Any, Callable, Tuple

from bs4 import BeautifulSoup
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    AnyDriver,
    visibility_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

from aijobs.data.common_scraper import CommonSeleniumScraper

__all__ = ["VietnamWorksSeleniumScraper"]

from aijobs.utils.helpers import Helper

SEARCH_BAR_INPUT_FIELD_CLASS: str = "SearchBar-module_inputField"
SEARCH_BAR_INPUT_FIELD_PLACEHOLDER: str = "Tìm kiếm việc làm, công ty, kỹ năng"
SEARCH_BAR_BUTTON_CLASS: str = "SearchBar-module_actionGroup"
BLOCK_LIST_CLASS: str = "block-job-list"
NO_OF_JOBS_CLASS: str = "no-of-jobs"
ITEMS_PER_PAGE: int = 50
MAX_PAGES_TO_SCRAPE: int = 10
REMOVE_ICON_CLASS_NAME: str = "remove-icon"
REMOVE_ICON_ID_NAME: str = "icons/icon-forms/icon-remove-gray"
SORT_U_BUTTON_CLASS_NAME: str = "sort-item-wrapped"
SORT_U_BUTTON_TEXT: str = "Ngày đăng (mới nhất)"


def presence_of_element_located_and_text_non_empty(
    locator: Tuple[str, str]
) -> Callable[[AnyDriver], bool]:
    """An expectation for checking that an element is present on the DOM of a
    page. This does not necessarily mean that the element is visible.
    And the text must be non-empty.

    :param locator: used to find the element
    :return: whether the element is found and the text is not empty
    """

    def _predicate(driver):
        try:
            element = driver.find_element(*locator)
            return element.text is not None and element.text.strip() != ""
        except StaleElementReferenceException:
            return False

    return _predicate


class VietnamWorksSeleniumScraper(CommonSeleniumScraper):
    _start_url: str = "https://vietnamworks.com"

    def __init__(
        self,
        binary: str | None = None,
        headless: bool = True,
        driver_path: str | None = None,
        browser_path: str | None = None,
    ) -> None:
        super().__init__(binary, headless, driver_path, browser_path)

    def _click_sort_button_(self):
        """
        Click Sort U button
        :return:
        """
        try:
            sort_U = self._driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{SORT_U_BUTTON_CLASS_NAME}')]/div[contains(@text, '{SORT_U_BUTTON_TEXT}')]",
            )
            sort_U.click()
            time.sleep(2)
        except Exception as e:
            print(e)

    def _click_delete_icon_(self):
        """
        Click a delete icon
        :return: None
        """
        try:
            delete_button = self._driver.find_element(By.ID, REMOVE_ICON_ID_NAME)
            delete_button.click()
        except Exception as e:
            print(e)

    def __parse__(self, query: str, *args, **kwargs) -> Any:
        try:
            self._driver.get(kwargs.get("url", None))
            element = WebDriverWait(self._driver, 60).until(
                presence_of_element_located(
                    (
                        By.XPATH,
                        f"//div[starts-with(@class, '{SEARCH_BAR_INPUT_FIELD_CLASS}')]",
                    )
                )
            )
            element = self._driver.find_element(
                By.XPATH,
                f"//input[@placeholder='{SEARCH_BAR_INPUT_FIELD_PLACEHOLDER}']",
            )
            element.click()
            self._click_delete_icon_()
            element.clear()
            time.sleep(1)
            element.send_keys(query)
            element = self._driver.find_element(
                By.XPATH,
                f"//div[starts-with(@class, '{SEARCH_BAR_BUTTON_CLASS}')]/button[contains(@class, 'clickable')]",
            )
            element.click()
        except Exception as e:
            print(e)
            # self._driver.quit()
            return None

        try:
            WebDriverWait(self._driver, 60).until(
                visibility_of_element_located((By.XPATH, f"//strong[@title='{query}']"))
            )
            # self._click_sort_button_()
            # Scroll down to get all items in this page
            for i in range(10):
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

            element = self._driver.find_element(
                By.XPATH, f"//div[@class='{BLOCK_LIST_CLASS}']"
            )
            elements = element.find_elements(
                By.XPATH, f"//div[contains(@class, 'view_job_item')]/div"
            )

            jobs = []
            for el in elements:
                html = el.get_attribute("innerHTML")
                company = None
                company_url = None
                job_url = None
                job_name = None
                bs = BeautifulSoup(html, features="lxml")
                links = bs.find_all("a", recursive=True)
                for link in links:
                    href = link.get("href")
                    print(f"HREF: {href}")
                    if href is None or "http" in href:
                        continue
                    if "/nha-tuyen-dung/" in href:
                        company = link.text
                        company_url = self._start_url + href
                    else:
                        job_url = self._start_url + href
                        job_name = link.text
                if (
                    company is None
                    and company_url is None
                    and job_url is None
                    and job_name is None
                ):
                    continue
                jobs.append(
                    {
                        "title": job_name,
                        "url": job_url,
                        "company": company,
                        "company_url": company_url,
                    }
                )
            # self._driver.quit()
            return jobs
        except Exception as e:
            print(e)
            # self._driver.quit()
            return None

    def _parse_job_page_(self, url: str) -> Any:
        """
        Parse a single job pahe
        :param url: the target job page
        :return: a tuple of benefits, description, requirements, locations, tags, and side information about the job
        """
        try:
            self._driver.get(url)
            WebDriverWait(self._driver, 6).until(
                visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'job-description')]")
                )
            )
            element = self._driver.find_element(By.CLASS_NAME, "what-we-offer")
            benefits = element.text
            element = self._driver.find_element(By.CLASS_NAME, "job-description")
            description = element.text
            element = self._driver.find_element(By.CLASS_NAME, "job-requirements")
            requirements = element.text
            element = self._driver.find_element(By.CLASS_NAME, "job-locations")
            locations = element.text
            element = self._driver.find_element(By.CLASS_NAME, "job-tags")
            tags = element.text
            element = self._driver.find_element(By.CLASS_NAME, "tab-sidebar")
            side_info = element.text
            return benefits, description, requirements, locations, tags, side_info
        except Exception as e:
            print(e)
            return None, None, None, None, None, None

    def scrape(
        self,
        start_url: str,
        query: str,
        location: str | None,
        loop_next_page: bool = True,
    ) -> Any:
        jobs = self.__parse__(query, url=start_url)
        if not loop_next_page:
            return jobs
        if jobs is not None:
            count = 2
            updated_url = self._driver.current_url
            while count < MAX_PAGES_TO_SCRAPE:
                try:
                    self._driver.find_element(
                        By.XPATH, "//ul[contains(@class, 'pagination')]"
                    )
                except NoSuchElementException as e:
                    print(e)
                    break
                tmp = self.__parse__(query, url=f"{updated_url}?page={count}")
                count += 1
                if tmp is None:
                    break
                jobs.extend(tmp)

            job_dict = {}
            for job in jobs:
                if job["url"] not in job_dict:
                    job_dict[job["url"]] = job
            jobs = list(job_dict.values())
            print(f"JOBS: {len(jobs)}")

            for k, job in tqdm(enumerate(jobs)):
                job_url = job["url"]
                params = Helper.get_url_params(job_url)
                job["placement"] = (
                    params["placement"] if "placement" in params else None
                )
                (
                    benefits,
                    description,
                    requirements,
                    locations,
                    tags,
                    side_info,
                ) = self._parse_job_page_(job_url)
                job["extra"] = {
                    "benefits": benefits,
                    "description": description,
                    "requirements": requirements,
                    "locations": locations,
                    "tags": tags,
                    "side_info": side_info,
                }
                jobs[k] = job

        # self._driver.close()
        return {
            "total": len(jobs) if jobs is not None else 0,
            "query": query,
            "location": None,
            "dataList": jobs,
        }

    def __str__(self):
        return "VietnamWorks Selenium Scraper"
