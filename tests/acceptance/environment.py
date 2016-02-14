"""
Environment setup for Acceptance tests using behave.
"""
from django.core.management import call_command
from selenium.webdriver import Firefox  # PhantomJS
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def monkey_patch_selenium():
    """Provide short versions (aliases) for finding by CSS selectors.
    ``find()`` and ``find_all()`` then work like jQuery's ``$()`` function.
    """
    WebDriver.find = WebDriver.find_element_by_css_selector
    WebElement.find = WebElement.find_element_by_css_selector
    WebDriver.find_all = WebDriver.find_elements_by_css_selector
    WebElement.find_all = WebElement.find_elements_by_css_selector


def before_all(context):
    """Set up the context object before tests are started."""
    monkey_patch_selenium()

    context.browser = Firefox()  # use PhantomJS() for faster, invisible test runs


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    """Provide initial data (fixtures) for each test"""
    call_command('organice', 'bootstrap', verbosity=0)


def after_all(context):
    """Tear down open resources after tests have completed."""
    context.browser.quit()
