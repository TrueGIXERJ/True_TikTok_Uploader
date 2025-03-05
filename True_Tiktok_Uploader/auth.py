from TrueGIXERJ_Utils.logger import logger
from True_Tiktok_Uploader import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AuthBackend:
    def __init__(self, cookies=None):
        self.cookies = self.get_cookies(path=cookies) if cookies else []
        if not self.cookies:
            raise InsufficientAuth()

    def authenticate_agent(self, driver):
        """
        Authenticates the agent using the browser backend
        """

        logger.info("Authenticating browser with cookies")

        driver.get(config.main_path)

        WebDriverWait(driver, config.long_wait).until(EC.title_contains("TikTok"))

        for cookie in self.cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as _:
                logger.error(f'Failed to add cookie {cookie}')

        return driver

    def get_cookies(self, path: str=None) -> list[dict]:
        try:
            with open(path, "r", encoding="utf-8") as file:
                lines = file.read().split("\n")
        except Exception as e:
            logger.error(f"Error reading cookies file: {e}")
            return []

        return_cookies = []
        for line in lines:
            split = line.split('\t')
            if len(split) < 6:
                continue

            split = [x.strip() for x in split]

            try:
                split[4] = int(split[4])
            except ValueError:
                split[4] = None

            return_cookies.append({
                'name': split[5],
                'value': split[6],
                'domain': split[0],
                'path': split[2],
            })

            if split[4]:
                return_cookies[-1]['expiry'] = split[4]
        return return_cookies
    
class InsufficientAuth(Exception):
    def __init__(self, message=None):
        super().__init__(message or self.__doc__)
