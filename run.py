from driver.webdriver import WebDriver
from configparser import ConfigParser
import logging
import locale

logging.basicConfig(format='%(asctime)s:%(name)s-(%(levelname)s)-%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    locale.getpreferredencoding()
    config = ConfigParser()
    config.read('example.ini')
    logger.debug('Read config example.ini with %(username)s as username' % config['LOGIN'])
    web_driver = WebDriver(config['LOGIN']['username'], config['LOGIN']['password'])
    web_driver.login()
    tags = [u'cetogenicaespañol', u'dietaketo']
    for tag in tags:
        web_driver.like_photo_by_tag(tag)

    del web_driver



