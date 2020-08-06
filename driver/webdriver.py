import logging
import time
from logging import Logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.ui import WebDriverWait



class WebDriver:
    logger: Logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    WAIT_TIME_SECS = 2
    SCROLL_LIMIT = 1

    def __init__(self, username, password, driver=webdriver.Chrome()):
        self.IG_PREFIX = u'https://www.instagram.com'
        self.username = username
        self.password = password
        self.driver = driver

    def __del__(self):
        self.driver.quit()

    @staticmethod
    def _inspect(find_element, path):
        try:
            return find_element(path)
        except NoSuchElementException as e:
            logger.warning(e)
            return ''

    def _write_in_textbox(self, path, input_keys, by=By.XPATH, timeout=WAIT_TIME_SECS):
        wait = WebDriverWait(self.driver, timeout)
        present_elem = presence_of_element_located((by, path))
        elem = wait.until(present_elem, 'Element not found')
        if elem:
            elem.clear()
            elem.send_keys(input_keys)
        else:
            logger.warning('Skip writing in textbook')

    def _scroll_and_get(self, timeout=WAIT_TIME_SECS, times=SCROLL_LIMIT):
        prev, curr = 0, 1
        it = 0
        while prev != curr and it < times:
            it += 1
            prev = curr;
            curr = self.driver.execute_script('''window.scrollTo(0, document.body.scrollHeight);
                                                 return document.body.scrollHeight;''')
            logger.debug("scrolling...")
            time.sleep(timeout)

    def _click_element(self, path, by=By.XPATH, timeout=WAIT_TIME_SECS, warning_msg=''):
        wait = WebDriverWait(self.driver, timeout)
        clickable = element_to_be_clickable((by, path))
        wait.until(clickable, warning_msg).click()

    def login(self):
        logger.info('Logging in...')
        self.driver.get(self.IG_PREFIX + '/accounts/login')
        self._write_in_textbox('//input[@name="username"]', self.username, timeout=3 * WAIT_TIME_SECS)
        self._write_in_textbox('//input[@name="password"]', self.password, timeout=3 * WAIT_TIME_SECS)
        self._click_element('button[type=submit]', by=By.CSS_SELECTOR,
                            warning_msg='Skip click login button', timeout=2 * WAIT_TIME_SECS)
        self._click_element("//button[contains(text(), 'Not Now')]", warning_msg='Skip click not now pop-up')

    def like_photo_by_tag(self, hashtag):
        logger.info(u'Liking pics in tag %s' % hashtag)
        self.driver.get(u'%s/explore/tags/%s/' % (self.IG_PREFIX, hashtag))
        self._scroll_and_get(timeout=2 * WAIT_TIME_SECS)
        time.sleep(5 * WAIT_TIME_SECS)
        hrefs = self._inspect(lambda x: self.driver.find_elements_by_xpath(x), '//a[@href]')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        logger.info('%s photos: %d' % (hashtag, len(pic_hrefs)))
        logger.info(pic_hrefs)
        pic_hrefs = [href for href in pic_hrefs if '%s/p/' % self.IG_PREFIX in href]
        logger.info(pic_hrefs)

        for pic in pic_hrefs:
            self.driver.get(pic)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(WAIT_TIME_SECS)
            try:
                wait = WebDriverWait(self.driver, WAIT_TIME_SECS)
                inspected = presence_of_element_located((By.XPATH, '//*[name()="svg" and @aria-label="Like"]'))
                wait.until(inspected, 'Unable to like').click()
                logger.info('Liking %s ...' % pic)
                time.sleep(18 * WAIT_TIME_SECS)
            except Exception as e:
                logger.error(e)
                time.sleep(2 * WAIT_TIME_SECS)
