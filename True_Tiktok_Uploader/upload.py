from TrueGIXERJ_Utils.logger import logger
from selenium import webdriver
import os
from True_Tiktok_Uploader import config
from True_Tiktok_Uploader.auth import AuthBackend
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions

def upload_video(filename=None, description=None, cookies='', headless=False):
    """
    Uploads a video to TikTok.
    
    :param filename: path to the video file to upload.
    :param description: caption for the video when posted.
    :param cookies: path to the browser cookies to use for authentication.
    :param headless: whether to run the browser in headless mode or not.
    """
    path = os.path.abspath(filename)
    if not path or not path.split('.')[-1] in ["mp4", "mov", "avi", "wmv", "flv", "webm", "mkv", "m4v", "3gp", "3g2", "gif"]:
        logger.error(f'{path} is invalid')
        return

    auth = AuthBackend(cookies)

    logger.info('Uploading video...')

    logger.info(f'Creating a Chrome browser instance {"in headless mode" if headless else ""}')
    try:
        driver = get_driver(headless)
        driver = auth.authenticate_agent(driver)
    except Exception as e:
        logger.error(f'Failed to initialize WebDriver: {e}')
        return

    logger.info(f'Posting {filename}')
    if description:
        logger.info(f'with description: {description}')

    complete_upload_form(driver, path, description, headless=headless)

def complete_upload_form(driver, path: str, description: str, headless=False):
    """
    Handles the filling out of the upload form on the upload page
    """
    logger.info('Navigating to Upload page')
    driver.get(config.upload_path)
    
    try:
        _set_video(driver, path)
        _set_description(driver, description)
        _post_video(driver)
    finally:
        driver.quit()

def _set_video(driver, path: str) -> None:
    """
    Uploads a video file.
    """
    logger.info('Uploading video file...')
    try:
        driverWait = WebDriverWait(driver, config.long_wait)
        upload_boxWait = EC.presence_of_element_located(
            (By.XPATH, config.upload_video)
        )
        driverWait.until(upload_boxWait)
        upload_box = driver.find_element(
            By.XPATH, config.upload_video
        )
        upload_box.send_keys(path)
        
        # Wait for the "Uploaded" confirmation text to appear
        uploaded_text = WebDriverWait(driver, config.long_wait).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Uploaded')]")
            )
        )
        if uploaded_text:
            logger.success("Video uploaded successfully!")
            return
    except TimeoutException as exception:
        logger.error("TimeoutException occurred:\n", exception)
    except Exception as exception:
        logger.error(str(exception))
        raise FailedToUpload(exception)

def _set_description(driver, description):
    if description is None:
        return

    logger.info('Setting description')

    description = description.encode('utf-8', 'ignore').decode('utf-8')

    saved_description = description

    WebDriverWait(driver, config.short_wait).until(EC.presence_of_element_located(
                    (By.XPATH, config.description)
                ))

    desc = driver.find_element(By.XPATH, config.description)

    desc.click()

    WebDriverWait(driver, config.long_wait).until(lambda driver: desc.text != '')

    desc.send_keys(Keys.END)
    _clear(desc)

    WebDriverWait(driver, config.long_wait).until(lambda driver: desc.text == '')
    
    desc.click()

    time.sleep(1)

    try:
        words = [word for word in description.split(" ") if word]
        for word in words:
            if word[0] == "#" or word[0] == '@':
                desc.send_keys(word)
                time.sleep(5)
                desc.send_keys(Keys.ENTER)
            else:
                desc.send_keys(word + ' ')

    except Exception as exception:
        logger.error(f'Failed to set description: {exception}')
        _clear(desc)
        desc.send_keys(saved_description)

def _post_video(driver) -> None:
    logger.info('Clicking the post button')

    try:
        post = WebDriverWait(driver, config.short_wait).until(EC.element_to_be_clickable((By.XPATH, config.post)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", post)
        post.click()
    except ElementClickInterceptedException:
        logger.info("Trying to click on the button again")
        driver.execute_script('document.querySelector(".btn-post > button").click()')

    # waits for the video to upload
    logger.info('Waiting for video to finish posting...')
    time.sleep(5)

    logger.success('Video posted successfully')

def _clear(element) -> None:
    element.send_keys(2 * len(element.text) * Keys.BACKSPACE)

def get_driver(headless):
    options = ChromeOptions()
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--profile-directory=Default')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--lang=en")
    if headless:
        options.add_argument('--headless=new')

    driver = webdriver.Chrome(options)
    return driver


class FailedToUpload(Exception):
    """
    Custom exception for failed video uploads.
    """
    def __init__(self, message=None):
        super().__init__(message or self.__doc__)
