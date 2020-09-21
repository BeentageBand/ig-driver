import locale
import logging
from configparser import ConfigParser
import json

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
    user = config['PROFILE']['user']
    logger.debug('user: %s' % user);
    uposts = web_driver.get_posts_by_username(user)
    logger.info(uposts)

    posts = []
    tags = json.loads(config['PROFILE']['hashtags'])
    logger.debug(tags)
    for tag in tags:
        posts.extend(web_driver.get_posts_by_hashtag(tag))

    comments = json.loads(config['PROFILE']['comments'])
    logger.debug(comments)
    for post in posts:
        web_driver.like_post(post)
        web_driver.comment_on_post(post, comments=comments)

    del web_driver
