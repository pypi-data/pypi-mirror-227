import os.path

from aijobs import (
    TopCVSeleniumScraper,
    VietnamWorksSeleniumScraper,
    IndeedSeleniumScraper,
    Helper,
)

from argparse import ArgumentParser, Namespace
import json

arg = ArgumentParser("AIJobs -- Tool to collect VN AI Jobs from different sources")
arg.add_argument(
    "--headless", "-H", action="store_true", help="Whether if use headless mode"
)
arg.add_argument(
    "--browser",
    "-b",
    type=str,
    default="./scripts/chrome/GoogleChromePortable64/GoogleChromePortable64/GoogleChromePortable.exe",
    help="Path to the Chrome browser for testing",
)
arg.add_argument(
    "--driver",
    "-d",
    type=str,
    default="./scripts/chrome/undetected_chromedriver.exe",
    help="Path to the UnDetected Chrome Driver for testing",
)
arg.add_argument(
    "--scrapper", "-s", type=str, default="TopCV", help="The name of the scrapper"
)
arg.add_argument(
    "--query",
    "-q",
    nargs="+",
    type=str,
    help="The query to search for jobs",
    required=True,
)
arg.add_argument(
    "--location",
    "-l",
    type=str,
    default="Hanoi, Vietnam",
    help="The location of the jobs",
)
arg.add_argument(
    "--output",
    "-o",
    type=str,
    default="./output",
    help="The directory to save the output JSON files",
)
params = arg.parse_args()


def cmd() -> None:
    browser = os.path.abspath(params.browser)
    driver = os.path.abspath(params.driver)
    if params.scrapper.lower() == "vietnamworks":
        scrapper = VietnamWorksSeleniumScraper(
            browser_path=browser, driver_path=driver, headless=params.headless
        )
        start_url = "https://vietnamworks.com"
    elif params.scrapper.lower() == "indeed":
        scrapper = IndeedSeleniumScraper(
            browser_path=browser, driver_path=driver, headless=params.headless
        )
        start_url = "https://vn.indeed.com"
    elif params.scrapper.lower() == "topcv":
        scrapper = TopCVSeleniumScraper(
            browser_path=browser, driver_path=driver, headless=params.headless
        )
        start_url = "https://www.topcv.vn"
    else:
        raise NotImplementedError(
            "This scrapper is not supported. Please consult to the manager."
        )
    queries = params.query
    location = params.location

    if not os.path.exists(params.output):
        os.makedirs(params.output)
    for query in queries:
        results = scrapper.scrape(
            start_url=start_url, query=query, location=location, loop_next_page=True
        )
        json.dump(
            fp=open(
                f"{params.output}/{params.scrapper}_{query.replace(' ', '+')}_{Helper.get_current_time()}.json",
                "w",
                encoding="utf-8",
            ),
            obj=results,
        )

    scrapper.close()
