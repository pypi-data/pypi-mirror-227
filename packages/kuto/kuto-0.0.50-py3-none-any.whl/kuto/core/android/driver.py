import os
import re
import time
import subprocess
import requests
import six
import uiautomator2 as u2

from kuto.utils.common import screenshot_util, calculate_time
from kuto.utils.exceptions import PkgIsNull, DeviceNotFoundException
from kuto.utils.log import logger


class AndroidDriver(object):

    def __init__(self, device_id=None, pkg_name=None):
        self.pkg_name = pkg_name
        if not self.pkg_name:
            raise PkgIsNull('应用包名不能为空')
        self.device_id = device_id
        if not self.device_id:
            raise DeviceNotFoundException('设备id不能为空')

        self.d = u2.connect(self.device_id)

    @calculate_time
    def get_app_info(self):
        logger.info("获取应用信息")
        info = self.d.app_info(self.pkg_name)
        logger.info(info)
        return info

    @calculate_time
    def get_device_info(self):
        logger.info(f"获取设备信息")
        info = self.d.device_info
        logger.info(info)
        return info

    @property
    @calculate_time
    def page_content(self):
        logger.info("获取页面xml")
        info = self.d.dump_hierarchy()
        logger.info(info)
        return info

    @calculate_time
    def assert_act(self, activity_name: str, timeout=5):
        logger.info(f"断言 activity 等于 {activity_name}")
        assert self.d.wait_activity(activity_name, timeout=timeout)

    # def assertContent(self, text, count=3):
    #     logger.info(f"断言页面文本包括: {text}")
    #     result = False
    #     for item in range(count):
    #         page_content = self.page_content
    #         if text in page_content:
    #             result = True
    #             break
    #         time.sleep(1)
    #     assert result, f"页面内容不包含文本: {text}"

    @calculate_time
    def uninstall_app(self):
        logger.info(f"卸载应用")
        self.d.app_uninstall(self.pkg_name)

    @staticmethod
    @calculate_time
    def download_apk(src):
        """下载安装包"""
        start = time.time()
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中...')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                end = time.time()
                logger.info(f'下载成功: {file_path}，耗时: {end - start}s')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("static {!r} not found".format(src))

    @calculate_time
    def install_app(self, apk_path, auth=True, new=True):
        """
        安装应用，push改成adb命令之后暂时无法支持远程手机调用
        @param apk_path: 安装包链接，支持本地路径以及http路径
        @param auth: 是否进行授权
        @param new: 是否先卸载再安装
        """
        start = time.time()
        logger.info(f"安装应用: {apk_path}")
        # 卸载
        if new is True:
            self.uninstall_app(self.pkg_name)

        # 下载
        source = self.download_apk(apk_path)

        # 把安装包push到手机上
        target = "/static/local/tmp/_tmp.apk"
        cmd = f'adb -s {self.device_id} push {source} {target}'
        subprocess.check_call(cmd, shell=True)

        # 安装
        cmd_list = ['pm', 'install', "-r", "-t", target]
        if auth is True:
            cmd_list.insert(4, '-g')
        logger.debug(f"{' '.join(cmd_list)}")
        cmd_str = f'adb -s {self.device_id} shell {" ".join(cmd_list)}'
        subprocess.check_call(cmd_str, shell=True)

        # 删除下载的安装包
        if 'http' in apk_path:
            os.remove(source)

        end = time.time()
        logger.info(f'安装成功，耗时: {end - start}s')

    @calculate_time
    def start_app(self, stop=True):
        """启动应用
        @param stop: 是否先关闭应用再启动
        """
        logger.info(f"启动应用")
        self.d.app_start(self.pkg_name, stop=stop, use_monkey=True)

    @calculate_time
    def stop_app(self):
        logger.info("关闭应用")
        self.d.app_stop(self.pkg_name)

    @calculate_time
    def screenshot(self, file_name=None, position: str = None):
        return screenshot_util(self.d, file_name=file_name, position=position)

    @calculate_time
    def back(self):
        logger.info("返回上一页")
        self.d.press('back')

    @calculate_time
    def click_alerts(self, alert_list: list):
        logger.info(f"点击弹窗: {alert_list}")
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()

    @calculate_time
    def swipe(self, direction: str = None):
        logger.info(f"swipe {direction}")
        key_range = ["left", "right", "up", "down"]
        if direction not in key_range:
            raise KeyError(f"direction取值只能是 {key_range} 其中一个")
        self.d.swipe_ext(direction)


if __name__ == '__main__':
    driver1 = AndroidDriver(
        device_id="UJK0220521066836",
        pkg_name="1111"
    )
    driver1.swipe("up")



