import locale
import logging
from configparser import ConfigParser

from driver.webdriver import WebDriver

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
    user = u'ketodogmom'
    uposts = web_driver.get_posts_by_username(user)
    logger.info(uposts)

    posts = uposts
    tags = [u'cetogenicaespañol', u'dietaketo']
    for tag in tags:
        posts.extend(web_driver.get_posts_by_hashtag(tag))

    comments = ['.']
    for post in posts:
        web_driver.like_post(post)
        web_driver.comment_on_post(post, comments=comments)

    del web_driver
