from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.setting import WEB_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
class UIclient:
    def __init__(self,driver):
        self.driver = driver
        self.base_url = WEB_URL
        self.wait = WebDriverWait(self.driver, 10)

    def build_url(self, page_path: str) -> str:
        """拼接完整页面url"""
        # 去掉右边 / ，防止拼接出错
        base = self.base_url.rstrip("/")
        # 去掉左边  / ，防止暴力拼接
        path = page_path.lstrip("/")
        return f"{base}/{path}"

    def go_to_page(self, page_path: str):
        """直接跳转页面：拼接url + driver.get()一步完成"""
        full_url = self.build_url(page_path)
        self.driver.get(full_url)
        return full_url

    # 输入
    def send_key_input(self,locator,text):
        el = WebDriverWait(self.driver,10).until(EC.presence_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    # 点击
    def click_element(self,locator):
        el = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        el.click()

    # 等待跳转
    def wait_url_contains(self, url_segment: str):
        """等待url包含片段，只做等待，不做断言"""
        self.wait.until(EC.url_contains(url_segment))

    # 获取提示文案
    def get_tip_text(self, locator):
        """获取提示文案"""
        el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )
        return el.text
