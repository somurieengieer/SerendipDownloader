import logging
from selenium import webdriver
import os


class ChromeDriver:
    driver = None

    # ファイル保存先ディレクトリ
    saveDir = None

    def __init__(self, saveDir=os.getcwd()):
        self.saveDir = saveDir

    # Driverを生成する
    def getDriver(self):

        try:
            # Chrome バージョン
            chopt = webdriver.ChromeOptions()
            prefs = {"download.default_directory": self.saveDir,
                     "download.prompt_for_download": False,
                     "download.directory_upgrade": True,
                     "plugins.plugins_disabled": ["Chrome PDF Viewer"],
                     "plugins.always_open_pdf_externally": True}
            chopt.add_experimental_option("prefs", prefs)
            # SSLエラー対策らしい
            chopt.add_argument('--ignore-certificate-errors')
            chopt.add_argument("--disable-extensions")
            chopt.add_argument("--disable-print-preview")
            # Headlessモードを有効にする場合はTrueを設定
            #    chopt.set_headless(True)
            self.driver = webdriver.Chrome("/Users/user/PycharmProjects/SerendipDownloader/venv/chromedriver",
                                      chrome_options=chopt)
            self.driver.implicitly_wait(3)  # 要素発見までの待ち最大秒数
            return self.driver
        except Exception as e:
            logging.error(e)
            print("Exception...")
            return None

    # プロセス終了までにデストラクタが必ず呼び出される保証なし。呼び出し側で「del インスタンス名」で呼び出し要
    def __del__(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
