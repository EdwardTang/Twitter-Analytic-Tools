import time
import html2text
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from TwitterScraper.items import TwitterScraperItem
# import beautiful soup
from bs4 import BeautifulSoup
#selenium macro headless driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class TwitterScraper(scrapy.Spider):
    name = "timeline"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com/CIT_PUC"+"/with_replies"] #paste in twitter stream URL
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
        	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        	"(KHTML, like Gecko) Chrome/15.0.87"
        )
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        # self.driver = webdriver.PhantomJS(executable_path='/usr/local/share/phantomjs-2.0.0-macosx/bin/phantomjs')
        self.driver.set_window_size(1120, 550)


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        i = 0
        # # test scrolller:
        # count = 2
        # while i < count:
        # 	self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 	time.sleep(2)
        # 	i += 1
        # 	print("aggregating tweets! step: " + str(i) + " of " + str(count))

        # infinite scroller 1:
        lastItemsCount = len(self.driver.find_elements_by_xpath("//ol[contains(@class,'stream-items')]/li"))
        print lastItemsCount

        while True:
            print "No."+str(i)+" Scrolling"
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            # elemsCount = self.driver.execute_script("return document.querySelectorAll('.GridTimeline-items > .Grid').length")
            newItemsCount = len(self.driver.find_elements_by_xpath("//ol[contains(@class,'stream-items')]/li"))
            if newItemsCount == lastItemsCount:
            	break
            else:
            	lastItemsCount = newItemsCount
            	i+=1

            
            
            

        # ## infinite scroller 2:
        # self.driver.find_element_by_link_text("All").click()
        # for i in range(1,100):
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(4)
        
        hxs = Selector(text = self.driver.page_source)
        h = html2text.HTML2Text()
        item = TwitterScraperItem()
        tweet_id_strs = hxs.xpath("//ol[contains(@class,'stream-items')]/li/@data-item-id").extract()
        # raw_tweets = hxs.xpath("//p[contains(@class,'tweet-text')]").extract()
        raw_tweets = hxs.xpath("//p[contains(@class,'tweet-text')]/text()").extract()
        
        raw_names = hxs.xpath("//span[contains(@class, 'username')]/b/text()").extract()
        
        #test
        for tweet_id,tweets in zip(tweet_id_strs,raw_tweets):
                print
                print tweet_id +': '+tweets
                print

        counter = 0
        for tweets in raw_tweets:
                #print raw_tweets[number]
                item['tweet_text'] = h.handle(raw_tweets[counter])
                # item['tweet_text'] = BeautifulSoup(raw_tweets[counter])
                item['tweet_id'] = tweet_id_strs[counter]
                item['screen_name'] = raw_names[counter]
                counter += 1
                yield item
        self.driver.quit()