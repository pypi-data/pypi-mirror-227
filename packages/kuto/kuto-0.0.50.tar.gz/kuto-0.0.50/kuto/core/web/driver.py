"""
@Author: kang.yang
@Date: 2023/5/12 20:49
"""
import time

from playwright.sync_api import sync_playwright, expect

from kuto.utils.common import screenshot_util, calculate_time
from kuto.utils.log import logger


class PlayWrightDriver:

    def __init__(self, browserName: str, headless: bool = False, state: dict = None):
        self.browserName = browserName
        self.headless = headless

        self.playwright = sync_playwright().start()
        if browserName == 'firefox':
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browserName == 'webkit':
            self.browser = self.playwright.webkit.launch(headless=headless)
        else:
            self.browser = self.playwright.chromium.launch(headless=headless)
        if state:
            self.context = self.browser.new_context(storage_state=state, no_viewport=True)
        else:
            self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()

    @calculate_time
    def switch_tab(self, locator):
        logger.info("开始切换tab")
        with self.page.expect_popup() as popup_info:
            locator.click()
        self.page = popup_info.value

    @calculate_time
    def open_url(self, url):
        logger.info(f"访问页面: {url}")
        self.page.goto(url)

    @calculate_time
    def storage_state(self, path=None):
        logger.info("保存浏览器状态信息")
        if not path:
            raise ValueError("路径不能为空")
        self.context.storage_state(path=path)

    @property
    @calculate_time
    def page_content(self):
        """获取页面内容"""
        logger.info("获取页面内容")
        content = self.page.content()
        logger.info(content)
        return content

    @calculate_time
    def set_cookies(self, cookies: list):
        logger.info("添加cookie并刷新页面")
        self.context.add_cookies(cookies)
        self.page.reload()

    @calculate_time
    def screenshot(self, file_name=None, position=None):
        return screenshot_util(self.page, file_name=file_name, position=position)

    @calculate_time
    def close(self):
        logger.info("关闭浏览器")
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    @calculate_time
    def assert_title(self, title: str, timeout: int = 5):
        logger.info(f"断言页面标题等于: {title}")
        expect(self.page).to_have_title(title, timeout=timeout * 1000)

    @calculate_time
    def assert_url(self, url: str, timeout: int = 5):
        logger.info(f"断言页面url等于: {url}")
        expect(self.page).to_have_url(url, timeout=timeout * 1000)

    # def assertContent(self, text, count=3):
    #     logger.info(f"断言页面文本包括: {text}")
    #     url = self.page.url
    #     self.page.wait_for_url(url)  # 必须调用这个方法，不然获取content可能会报错
    #     result = False
    #     for item in range(count):
    #         page_content = self.page_content
    #         if text in page_content:
    #             result = True
    #             break
    #         time.sleep(1)
    #     assert result, f"页面内容不包含文本: {text}"


if __name__ == '__main__':
    driver1 = PlayWrightDriver(browserName="chrome")
    driver1.open_url("https://patents.qizhidao.com/search/simple-result?from=simple&searchBtntype=searchBtn&businessSource=PC%E6%9F%A5%E4%B8%93%E5%88%A9&statement=%E4%BC%81%E7%9F%A5%E9%81%93")
    time.sleep(5)
    print(driver1.page.url)

