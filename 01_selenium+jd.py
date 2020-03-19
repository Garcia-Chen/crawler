import pymongo
import time

from selenium import webdriver
class JDspider(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # 创建浏览器对象
        self.browser=webdriver.Chrome(options=options)
        # 访问京东首页
        self.browser.get('https://www.jd.com/')
        self.i=0
        self.conn=pymongo.MongoClient('localhost',27017)
        self.db=self.conn['jddb']
        self.myset=self.db['jdset']

    def search_shangpin(self,things):
        # 获取搜索框
        kw = self.browser.find_element_by_xpath('//*[@id="key"]')
        kw.clear()
        kw.send_keys(things)
        # 获取搜索按钮
        self.browser.execute_script(
            'window.scrollTo(0,0)'
        ) #滚动到顶部
        su = self.browser.find_element_by_xpath('//*[contains(@id,"search")]/div//button')

        # // *[ @ id = "search-2014"] / div / button
        # 点击搜索按钮
        # // *[ @ id = "search-2014"] / div / button
        # //*[@id="search"]/div/div[2]/button
        su.click()

    # 等待页面加载
    def load_page(self):
        time.sleep(2)  # 需要等待几秒,不然加载不出来容易拿到空数据
        self.browser.execute_script(
            'window.scrollTo(1,document.body.scrollHeight)'
        )
        time.sleep(2)

    # 获取的单个页面的商品信息
    def get_shangpin(self):
        self.load_page()
        shangpin_list = self.browser.find_element_by_xpath('//*[@id="J_goodsList"]/ul')
        shangpin_list=shangpin_list.find_elements_by_xpath('./li')
        for shangpin in shangpin_list:
            item = {}
            # print(type(shangpin)) #<class 'selenium.webdriver.remote.webelement.WebElement'>
            # print(shangpin) #<selenium.webdriver.remote.webelement.WebElement (session="7d269c533e3a40a3522ff99a2c21c34b", element="0.0676625271558855-1")>

            # 接下来的代码会报错   AttributeError: 'WebElement' object has no attribute 'xpath'
            # item['price'] = shangpin.xpath('./div/div[@class="p-price"]/text()')
            # item['name'] = shangpin.xpath('./div/div[@class="p-name p-name-type-2"]/text()')
            # item['comm'] = shangpin.xpath('./div/div[@class="p-commit"/text()')
            # item['shop'] = shangpin.xpath('./div/div[@class="p-shop"]/text()')

            # 接下来的代码数据有时会错位
            # shanpin_info = shangpin.text.split('\n')
            # item['price'] = shanpin_info[0]
            # item['name'] = shanpin_info[1]
            # item['store'] = shanpin_info[3]
            # item['comm'] = shanpin_info[2]
            # print(item)
            item['price'] = shangpin.find_element_by_xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]').text.replace('\n',' ')
            item['name'] = shangpin.find_element_by_xpath('./div/div[contains(@class,"p-name")]').text.replace('\n',' ')
            item['comm'] = shangpin.find_element_by_xpath('./div/div[@class="p-commit"]').text
            item['shop'] = shangpin.find_element_by_xpath('./div/div[@class="p-shop"]').text
            print(item)
            self.myset.insert_one(item) #存入mongodb
        self.get_next()

    def get_next(self):
        while True:
            try:
                next=self.browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[@class="pn-next"]')
                next.click()
                self.get_shangpin()
            except Exception as e:
                break

    def run(self):
        while True:
            things=input('请输入需要搜索的商品:')
            if not things:
                print("浏览结束,欢迎下次再来")
                self.browser.quit()
                break
            self.search_shangpin(things)
            self.get_shangpin()


if __name__=='__main__':
    spider=JDspider()
    spider.run()
