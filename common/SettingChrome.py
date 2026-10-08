from selenium import webdriver  #用于操作浏览器
from selenium.webdriver.chrome.options import Options   #用于设置谷歌浏览器
from selenium.webdriver.chrome.service import Service   #用于管理谷歌驱动
from webdriver_manager.chrome import ChromeDriverManager

def setting_chrome():
    #创建设置浏览器对象
    ChromeOption = Options()

    #禁用沙盒模式(增加兼容性)
    ChromeOption.add_argument('--no-sandbox')

    #保持浏览器打开状态(默认是代码执行完毕自动关闭)
    ChromeOption.add_experimental_option('detach', True)

    #设置浏览器驱动文件路径
    path_driver = '../chromedriver.exe'

    #创建并启动浏览器
    OpenChromeOption = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ChromeOption)

    return OpenChromeOption