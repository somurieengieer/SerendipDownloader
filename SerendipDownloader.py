from bs4 import BeautifulSoup
import os
from time import sleep
import re
from mylib import ChromeDriver
import glob
import getpass


MAX_RETRY = 20            # アクセスエラー時のリトライ回数
ERROR_WAIT_SECONDS = 180  # アクセスエラー時の待ち秒数
SAVE_DIR = os.getcwd() + "/books"  # ファイル保存先ディレクトリ

# 臨時コメントアウト

# メールアドレスとパスワードを標準入力
email = input('your Amazon e-Mail: ')
password = getpass.getpass("your Amazon password: ")

bookList = None


#ログイン処理を行う。
def login(driver):

    # SerendipID・パスワード入力ページ
    url_loginPage = 'https://serendip-service.com/login/index'

    driver.get(url_loginPage)

    # (FYI) bellow line is same mean with -> driver.find_element_by_name("user_id").send_keys(email)
    driver.find_element_by_xpath("//input[@name='user_id']").send_keys(email)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(3)


# 書籍一覧画面を表示してから当メソッド呼び出す。
# 書籍一覧画面上の全書籍URLのlistと、次ページがあれば次ページのURLを返す。
def get_book_information_url_list(driver):

    # 画面遷移が完全に終えてから動く
    sleep(1)
    soup = BeautifulSoup(driver.page_source, "html5lib")
    li_all = soup.find("div", attrs={"id": "search_result"}).find("ol").find_all("li")
    href_list = []

    # 画面上の書籍ページへの全リンクを格納
    for li in li_all:
        href_list.append(li.a.get("href"))

    # 次ページがあれば再帰呼び出し
    if move_next_page(driver):
        href_list.extend(get_book_information_url_list(driver))

    return href_list


# 次ページがあれば次ページへ遷移してTrueを返す。ない場合はFalseを返す
def move_next_page(driver):
    active_value = driver.find_element_by_xpath('//*[@id="search_result"]/form/ul/li[@class="active"]/button').get_attribute("value")
    li_all = driver.find_elements_by_xpath('//*[@id="search_result"]/form/ul/li')
    for li in li_all:
        button = None
        try:
            button = li.find_element_by_tag_name("button")
        except:
            print("Button element had not been existed")

        if button is not None and int(button.get_attribute("value")) > int(active_value):
            button.click()
            return True
    return False


# driverと書籍ページのURLを渡すとPDFをダウンロードする
def getBookInformation(driver, book_information_url):
    sleep(1)
    driver.get(book_information_url)
    soup = BeautifulSoup(driver.page_source, "html5lib")
    # findの返り値はDOM要素であるため、再度find関数を使用可能
    # findの返り値は「bs4.element.ResultSet」であり、Listと同様に扱うことが可能
    dom_summary = soup.find("div", attrs={"class": "book_summary clearfix"}).find("h2")
    # 小要素をループで回す
    for ch in dom_summary:
        book_title = ch
        break
    book_href = driver.find_element_by_xpath('//*[@id="detail_book_genre_navi"]/div/a').get_attribute('href')
    repatter = re.compile(r'\/([0-9]{1,4})_')
    book_id = repatter.findall(book_href)[0]

    # ダウンロードボタンをクリック
    sleep(1)
    driver.find_element_by_xpath('//*[@id="detail_book_genre_navi"]/div/a').click()
#    driver.get(book_href) # こちらでもOK

    sleep(1)
    os.rename(SAVE_DIR + "/" + book_id + "_book_pdf.pdf", SAVE_DIR + "/" + book_id + "_" + book_title + ".pdf")


def main():
    cDriver = ChromeDriver.ChromeDriver(saveDir=SAVE_DIR)
    driver = cDriver.getDriver()
    login(driver)

    # カテゴリ別のURLリスト（末尾に1〜5の数値が着く）
    index_url = "https://serendip-service.com/search/category/"

    try:
        for i in range(1, 6):
            print("range: " + str(i))
            driver.get(index_url + str(i))
            global bookList
            if bookList is None:
                bookList = get_book_information_url_list(driver)
            print(bookList)
            count = 0
            for book_url in bookList:
                count = count+1
                if count > len(glob.glob(SAVE_DIR+"/*")):
                    getBookInformation(driver, book_url)
    except:
        raise
    finally:
        del driver


# 何十回かアクセスするとアクセスエラーになるため、ドライバーを再生成してリトライする
for i in range(MAX_RETRY):
    try:
        main()
    except:
        # アクセスエラー時の休息秒数
        sleep(ERROR_WAIT_SECONDS)
