import json
import time
from typing import Any

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait

from aijobs.data.common_scraper import CommonSeleniumScraper
from aijobs.utils.helpers import Helper

__all__ = ["TopCVSeleniumScraper"]

INPUT_PLACEHOLDER_TEXT: str = "Vị trí ứng tuyển"
FIND_JOBS_BTN_CLASS_NAME: str = "btn-search-job"
TOTAL_SEARCH_JOB_CLASS_NAME: str = "total-job-search"
JOB_LIST_CLASS_NAME: str = "job-list-default"
JOB_ITEM_CLASS_NAME: str = "job-item-default"
NUM_ITEMS_PER_PAGE: int = 25
MAX_PAGES: int = 10

JOB_DESCRIPTION_CLASS_NAME: str = "job-detail__information-detail--content"
JOB_DESCRIPTION_CLASS_NAME_1: str = "job-description"
JOB_INFO_SECTION_CLASS_NAME: str = "job-detail__info--section-content"
JOB_INFO_SECTION_TITLE_CLASS_NAME: str = "job-detail__info--section-content-title"
JOB_INFO_SECTION_VALUE_CLASS_NAME: str = "job-detail__info--section-content-value"
JOB_INFO_RIGHT_SIDE_CLASS_NAME: str = "box-general-group-info"
JOB_INFO_RIGHT_SIDE_TITLE_CLASS_NAME: str = "box-general-group-info-title"
JOB_INFO_RIGHT_SIDE_VALUE_CLASS_NAME: str = "box-general-group-info-value"
JOB_INFO_CATEGORY_CLASS_NAME: str = "box-category"
JOB_INFO_CATEGORY_TITLE_CLASS_NAME: str = "box-title"
JOB_INFO_CATEGORY_TAG_CLASS_NAME: str = "box-category-tag"
JOB_INFO_DEADLINE_CLASS_NAME: str = "job-detail__info--deadline"
BRAND_JOB_DESCRIPTION_CLASS_NAME: str = "job-data"
BRAND_JOB_ATTR_CLASS_NAME: str = "box-main"
BRAND_JOB_ATTR_CLASS_NAME_1: str = "box-item"
BRAND_JOB_ADDR_CLASS_NAME: str = "box-address"

# FIX: 2023-08-19 topCV is showing a popup that prevents the driver to click on the search button
CLOSE_BUTTON_20230819_CLASS_NAME: str = "close"
CLOSE_MODAL_20230819_CLASS_NAME: str = "modal-content"

# FIX: SORT UP BUTTON on CREATED DATETIME
SORT_U_BUTTON_FOR_NAME: str = "sort-value-new"


class TopCVSeleniumScraper(CommonSeleniumScraper):
    def __init__(
        self,
        binary: str | None = None,
        headless: bool = True,
        driver_path: str | None = None,
        browser_path: str | None = None,
    ):
        super().__init__(binary, headless, driver_path, browser_path)

    def _click_sort_button_(self):
        """
        Click on the sort U button
        :return:
        """
        try:
            sort_U = self._driver.find_element(
                By.XPATH, f"//label[@for='{SORT_U_BUTTON_FOR_NAME}']"
            )
            sort_U.click()
            time.sleep(3)
        except Exception as e:
            print(e)

    def _close_topcv_advertisement_20230819(self):
        """
        Click on close button on advertisement popups
        :return:
        """
        try:
            element = self._driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{CLOSE_MODAL_20230819_CLASS_NAME}')]/button[contains(@class,'{CLOSE_BUTTON_20230819_CLASS_NAME}')]",
            )
            element.click()
        except Exception as e:
            print("No advertisement found.")
            return

    def __parse__(self, query: str = None, *args, **kwargs) -> Any:
        url = kwargs.get("url", None)
        print(f"Visiting {url} ...")
        try:
            self._driver.get(url)
            self._close_topcv_advertisement_20230819()
            element = WebDriverWait(self._driver, 60).until(
                presence_of_element_located(
                    (By.XPATH, f"//input[@placeholder='{INPUT_PLACEHOLDER_TEXT}']")
                )
            )
            element.clear()
            time.sleep(1)
            element.send_keys(query)
            element = self._driver.find_element(By.CLASS_NAME, FIND_JOBS_BTN_CLASS_NAME)
            element.click()
        except Exception as e:
            print(e)
            # self._close_topcv_advertisement_20230819()
            # self._driver.quit()
            return None

        current_url = self._driver.current_url
        items = []
        print(f"getting job list ... ")
        try:
            WebDriverWait(self._driver, 60).until(
                presence_of_element_located(
                    (By.CLASS_NAME, TOTAL_SEARCH_JOB_CLASS_NAME)
                )
            )
            # Scroll down to get all items in this page
            for i in range(10):
                self._driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
            num_items = int(
                self._driver.find_element(
                    By.CLASS_NAME, TOTAL_SEARCH_JOB_CLASS_NAME
                ).text
            )
            if num_items > 0:
                num_pages = min(
                    num_items // NUM_ITEMS_PER_PAGE
                    + (0 if num_items % NUM_ITEMS_PER_PAGE == 0 else 1),
                    MAX_PAGES,
                )
                elements = self._driver.find_elements(
                    By.XPATH,
                    f"//div[@class='{JOB_LIST_CLASS_NAME}']/div[contains(@class,'{JOB_ITEM_CLASS_NAME}')]",
                )
                for element in elements:
                    html = element.get_attribute("innerHTML")
                    root = BeautifulSoup(html, features="lxml")
                    # topcv_job_id = root.get("data-job-id")
                    company = None
                    company_url = None
                    job = None
                    job_url = None
                    titles = root.find_all(
                        lambda tag: tag.name == "h3"
                        and "title" in tag.get("class", []),
                        recursive=True,
                    )
                    if len(titles) > 0:
                        job = titles[0].text.strip()
                        job_urls = titles[0].find_all(lambda tag: tag.name == "a")
                        if len(job_urls) > 0:
                            job_url = job_urls[0].get("href")
                    companies = root.find_all(
                        lambda tag: tag.name == "a"
                        and "company" in tag.get("class", []),
                        recursive=True,
                    )
                    if len(companies) > 0:
                        company = companies[0].get("data-original-title", None)
                        company_url = companies[0].get("href", None)
                    if (
                        company is None
                        and company_url is None
                        and job is None
                        and job_url is None
                    ):
                        continue
                    items.append(
                        {
                            # "job_id": topcv_job_id,
                            "company": company,
                            "company_url": company_url,
                            "title": job,
                            "url": job_url,
                        }
                    )
                for i in range(1, num_pages):
                    new_url = (
                        f"{current_url}{'&' if '?' in current_url else '?'}page={i + 1}"
                    )
                    self._driver.get(new_url)
                    WebDriverWait(self._driver, 60).until(
                        presence_of_element_located(
                            (By.CLASS_NAME, TOTAL_SEARCH_JOB_CLASS_NAME)
                        )
                    )
                    # Scroll down to get all items in this page
                    for j in range(10):
                        self._driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                    elements = self._driver.find_elements(
                        By.XPATH,
                        f"//div[@class='{JOB_LIST_CLASS_NAME}']/div[contains(@class,'{JOB_ITEM_CLASS_NAME}')]",
                    )
                    for element in elements:
                        html = element.get_attribute("innerHTML")
                        root = BeautifulSoup(html, features="lxml")
                        # topcv_job_id = root.get("data-job-id")
                        company = None
                        company_url = None
                        job = None
                        job_url = None
                        titles = root.find_all(
                            lambda tag: tag.name == "h3"
                            and "title" in tag.get("class", []),
                            recursive=True,
                        )
                        if len(titles) > 0:
                            job = titles[0].text.strip()
                            job_urls = titles[0].find_all(lambda tag: tag.name == "a")
                            if len(job_urls) > 0:
                                job_url = job_urls[0].get("href")
                        companies = root.find_all(
                            lambda tag: tag.name == "a"
                            and "company" in tag.get("class", []),
                            recursive=True,
                        )
                        if len(companies) > 0:
                            company = companies[0].get("data-original-title", None)
                            company_url = companies[0].get("href", None)
                        if (
                            company is None
                            and company_url is None
                            and job is None
                            and job_url is None
                        ):
                            continue
                        items.append(
                            {
                                # "job_id": topcv_job_id_job_id,
                                "company": company,
                                "company_url": company_url,
                                "title": job,
                                "url": job_url,
                            }
                        )
        except Exception as e:
            print(e)
            # self._driver.quit()
            return None

        return items

    def _parse_item_(self, item_url: str = None) -> Any:
        """
        Parse an item page
        :param item_url: the target job page
        :return: an object of the job
        """
        print(f"Visiting {item_url} ...")
        try:
            self._driver.get(item_url)
            self._close_topcv_advertisement_20230819()
            element = WebDriverWait(self._driver, 60).until(
                presence_of_element_located(
                    (
                        By.XPATH,
                        f"//div[contains(@class, '{JOB_DESCRIPTION_CLASS_NAME}')]/div[contains(@class, '{JOB_DESCRIPTION_CLASS_NAME_1}')]",
                    )
                )
            )
            job_description = element.text.strip()
            elements = self._driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, '{JOB_INFO_SECTION_CLASS_NAME}')]",
            )
        except Exception as e:
            print(e)
            return None

        attributes = {}
        for element in elements:
            html = element.get_attribute("innerHTML")
            root = BeautifulSoup(html, features="lxml")
            try:
                attribute_names = root.find_all(
                    lambda tag: tag.name == "div"
                    and JOB_INFO_SECTION_TITLE_CLASS_NAME in tag.get("class", [])
                )
                if len(attribute_names) == 0:
                    continue
                attribute_name = attribute_names[0].text.strip()
                attribute_data = root.find_all(
                    lambda tag: tag.name == "div"
                    and JOB_INFO_SECTION_VALUE_CLASS_NAME in tag.get("class", [])
                )
                if len(attribute_data) == 0:
                    continue
                attribute = attribute_data[0].text.strip()
                attributes[attribute_name] = attribute
            except Exception as e:
                print(e)
                continue
        try:
            elements = self._driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, '{JOB_INFO_RIGHT_SIDE_CLASS_NAME}')]",
            )
            for element in elements:
                html = element.get_attribute("innerHTML")
                root = BeautifulSoup(html, features="lxml")
                try:
                    attribute_names = root.find_all(
                        lambda tag: tag.name == "div"
                        and JOB_INFO_RIGHT_SIDE_TITLE_CLASS_NAME in tag.get("class", [])
                    )
                    if len(attribute_names) == 0:
                        continue
                    attribute_name = attribute_names[0].text.strip()
                    attribute_data = root.find_all(
                        lambda tag: tag.name == "div"
                        and JOB_INFO_RIGHT_SIDE_VALUE_CLASS_NAME in tag.get("class", [])
                    )
                    if len(attribute_data) == 0:
                        continue
                    attribute = attribute_data[0].text.strip()
                    attributes[attribute_name] = attribute
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)

        try:
            elements = self._driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, '{JOB_INFO_CATEGORY_CLASS_NAME}')]",
            )
            for element in elements:
                html = element.get_attribute("innerHTML")
                root = BeautifulSoup(html, features="lxml")
                try:
                    attribute_names = root.find_all(
                        lambda tag: tag.name == "div"
                        and JOB_INFO_CATEGORY_TITLE_CLASS_NAME in tag.get("class", [])
                    )
                    if len(attribute_names) == 0:
                        continue
                    attribute_name = attribute_names[0].text.strip()
                    tags = [
                        t.text.strip()
                        for t in root.find_all(
                            lambda tag: tag.name == "a"
                            and JOB_INFO_CATEGORY_TAG_CLASS_NAME in tag.get("class", [])
                        )
                    ]
                    attributes[attribute_name] = tags
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)

        deadline = None
        try:
            element = self._driver.find_element(
                By.CLASS_NAME, JOB_INFO_DEADLINE_CLASS_NAME
            )
            deadline = element.text.replace("Hạn nộp hồ sơ: ", "").strip()
        except Exception as e:
            print(e)

        return {
            "description": job_description,
            "attributes": attributes,
            "deadline": deadline,
        }

    def _parse_brand_item_(self, item_url: str = None) -> Any:
        """
        Parse a brand job page
        :param item_url: the target brand
        :return: an object of the job
        """
        print(f"Visiting {item_url} ...")
        try:
            self._driver.get(item_url)
            self._close_topcv_advertisement_20230819()
            element = WebDriverWait(self._driver, 60).until(
                presence_of_element_located(
                    (
                        By.XPATH,
                        f"//div[contains(@class, '{BRAND_JOB_DESCRIPTION_CLASS_NAME}')]",
                    )
                )
            )
            job_description = element.text.strip()
            elements = self._driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, '{BRAND_JOB_ATTR_CLASS_NAME}')]/div[contains(@class, '{BRAND_JOB_ATTR_CLASS_NAME_1}')]",
            )
        except Exception as e:
            print(e)
            return None

        attributes = {}
        for element in elements:
            html = element.get_attribute("innerHTML")
            root = BeautifulSoup(html, features="lxml")
            try:
                attribute_name = root.find_all(lambda tag: tag.name == "strong")[
                    0
                ].text.strip()
                attribute = root.find_all(lambda tag: tag.name == "span")[
                    0
                ].text.strip()
                attributes[attribute_name] = attribute
            except Exception as e:
                print(e)
                continue
        try:
            elements = self._driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, '{BRAND_JOB_ADDR_CLASS_NAME}')]",
            )
            for element in elements:
                html = element.get_attribute("innerHTML")
                root = BeautifulSoup(html, features="lxml")
                try:
                    attribute_name = root.find_all(lambda tag: tag.name == "p")[
                        0
                    ].text.strip()
                    attribute = root.find_all(lambda tag: tag.name == "div")[
                        0
                    ].text.strip()
                    attributes[attribute_name] = attribute
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)

        return {"description": job_description, "attributes": attributes}

    def scrape(
        self,
        start_url: str,
        query: str,
        location: str | None,
        loop_next_page: bool = True,
    ) -> Any:
        jobs = self.__parse__(query=query, url=start_url)
        job_dict = {}
        for job in jobs:
            if job["url"] not in job_dict:
                job_dict[job["url"]] = job
        items = list(job_dict.values())
        print(f"JOBS: {len(items)}")
        # pprint.pprint(items)
        result = []
        if items is not None:
            for item in items:
                job_url = item["url"]
                if "/brand/" not in job_url:
                    extra_info = self._parse_item_(item_url=job_url)
                else:
                    extra_info = self._parse_brand_item_(item_url=job_url)
                result.append({"basic": item, "extra": extra_info})
        return {
            "total": len(result),
            "query": query,
            "location": None,
            "dataList": result,
        }

    def __str__(self):
        return "TopCV Selenium Scrapper"
