import unittest
from selenium import webdriver

class DevcloudninjasBootcampLinkTest(unittest.TestCase):
    def setUp(self):
        # choose which webdriver to use
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def test_bootcamp_link(self):
        driver = self.driver
        driver.get("https://bootcamp.devcloudninjas.com")
        # check we get expected page title

        # find the link to Introduction to DevOps section at the bottom of the page

        # check that we get the expected url

    def tearDown(self):
        self.driver.quit()


class DevcloudninjasBootcampSidebarTest(unittest.TestCase):
    def setUp(self):
        # choose which webdriver to use
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def test_bootcamp_sidebar(self):
        driver = self.driver
        driver.get("https://bootcamp.devcloudninjas.com")
        # check that the sidebar is shown (HINT: check html body attributes)

        # check that there is no CLOSE attribute on the body

        # find the sidebar toggle and toggle it

        # after toggling sidebar, check that it is closed


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
