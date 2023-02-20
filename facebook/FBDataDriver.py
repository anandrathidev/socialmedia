# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:54:40 2023

@author: ananduser
"""

# selenium-driver.py
import json
from pathlib import Path
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time

class SeleniumDriver(object):
    def __init__(
        self,
        # chromedriver path
        driver_path = 'chromedriver.exe',
        # pickle file path to store cookies
        cookies_file_path = 'cookies/cookies.txt',
        # list of websites to reuse cookies with
        # cookies_websites=["https://facebook.com"]
        website = "https://facebook.com"

    ):
        self.driver_path = Path(driver_path).as_posix()
        self.cookies_file_path = Path(cookies_file_path).as_posix()
        # self.cookies_websites = cookies_websites
        self.website = website
        # chrome_options = webdriver.ChromeOptions()
        options = Options()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(
            executable_path=self.driver_path,
            options=options
        )
        try:
            # load cookies for given websites
#             cookies = pickle.load(open(self.cookies_file_path, "rb"))
            with open(self.cookies_file_path) as cookie_file:
                cookies = json.load(cookie_file)
            # for website in self.cookies_websites:
            self.driver.get(self.website)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        except Exception as e:
            # it'll fail for the first time, when cookie file is not present
            print(str(e))
            print("Error loading cookies")

    def save_cookies(self):
        # save cookies
        cookies = self.driver.get_cookies()
#         json.dump(cookies, open(self.cookies_file_path, "wb"))
        with open(self.cookies_file_path, 'w') as outfile:
            json.dump(cookies, outfile, indent=4)

    def close_all(self):
        # close all open tabs
        if len(self.driver.window_handles) < 1:
            return
        for window_handle in self.driver.window_handles[:]:
            self.driver.switch_to.window(window_handle)
            self.driver.close()

    def quit(self):
        self.save_cookies()
        self.close_all()
        self.driver.quit()


def account_fun():
    with open('accounts.txt') as f:
        account_list = f.readlines()
        new_accounts = []
        for acc in account_list:
            acc = acc.replace("\n", "")
            acc = acc.split(",")
            new_acc = []
            for i in acc:
                i = i.strip()
                new_acc.append(i)
            # print(new_acc)
            new_accounts.append(new_acc)
    random.shuffle(new_accounts)
    account_tuple = tuple(new_accounts)
    return account_tuple


def is_fb_logged_in():
    driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def fb_login(driver, username, password):
    username_box = driver.find_element(By.ID, 'email')
    username_box.send_keys(username)

    password_box = driver.find_element(By.ID, 'pass')
    password_box.send_keys(password)

    login_box = driver.find_element(By.NAME, 'login')
    login_box.click()


# function to wait for random time
def random_wait(a=0, b=None):
    if b == None:
        time.sleep(a)
    else:
        time.sleep(random.randrange(a,b))


def scroll_down(driver, n):
    html = driver.find_element(By.TAG_NAME, 'html')
    for i in range(n):
        html.send_keys(Keys.PAGE_DOWN)
        random_wait(3, 7)

def open_page(driver, pageurl):
    driver.get(pageurl)   
    wait = WebDriverWait(driver, 6) 
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    html = driver.find_element(By.TAG_NAME, 'html')
    time.sleep(0.3)


# like posts
def like_post(driver):
    # "//*[contains(text(), 'My Button')]"
    # '//div[contains(text(), "{0}") and @class="inner"]'.format(text)
    like_post = driver.find_elements(By.XPATH, "//*[contains(text(), 'Like')]")
    print(len(like_post))
    for ele in like_post:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


# add friend
def add_friend(driver):
    add_friend = driver.find_elements(By.XPATH, "//*[contains(text(), 'Add Friend')]")
    print(len(add_friend))
    for ele in add_friend[:3]:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)




# liked pages
def getPage_id(driver, pageurl): 
    driver.get(pageurl)   
    property_id = driver.find_element(By.XPATH, '//*[@property="al:android:url"]')
    print(property_id)
    print(property_id.get_attribute("content"))
    print(property_id.get_attribute("content").split("/")[-1] )
          
    return  property_id.get_attribute("content").split("/")[-1]



# liked groups
def managed_page(driver, like_page_url):
    #like_page_url = 'https://www.facebook.com/ExMuslimMurtadApostateIndia/likes'
    driver.get(like_page_url)
    scroll_down(driver, 1)
    like_pages = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]')    
    like_pages_list = like_pages.find_elements(By.XPATH, ".//a[@role='link']")
    print(like_pages)
    href_list = []
    id_list = []
    for ele in like_pages_list:
        try:
            href = ele.get_attribute("href")
            print(href)
            href_list.append(href)
            pageid = getPage_id(driver=driver, pageurl=href)
            id_list.append(pageid)
            #print(f"{ele} \n")
            print(f"text Element: {ele.text}  href {href} \n", )
        except Exception as e:
            print(e)
    return href_list,id_list

# like pages
def like_page(driver, ):
    like_page_url = 'https://www.facebook.com/pages/?category=top&ref=bookmarks'
    driver.get(like_page_url)
    scroll_down(driver, 1)
    like_page = driver.find_elements(By.XPATH, "//*[contains(text(), 'Like')]")
    print(len(like_page))
    for ele in like_page[1:10]:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


def switch_role_to_page(driver, my_pprofile):
    #div aria-label="Account controls and settings" role="navigation"  
    driver.get(like_page_url)
    html = driver.find_element(By.TAG_NAME, 'html')
    for i in range(2):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
    wait = WebDriverWait(driver, 6) 
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Your profile"]')))
    profile_control_ele = driver.find_element(By.XPATH, 
                                     '//*[@aria-label="Your profile"]')
    profile_control_ele.click()
    time.sleep(0.4)
    
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"See all profiles")]' )))      
    see_all_profiles_ele = driver.find_element( By.XPATH, 
                     '//*[contains(text(),"See all profiles")]' )

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"See all profiles")]' )))      
        see_all_profiles_ele = driver.find_element( By.XPATH, 
                     '//*[contains(text(),"See all profiles")]' )
        see_all_profiles_ele.click()
    except Exception as e:
        #action = ActionChains(driver);
        #action.move_to_element(my_profile_ele).perform();
        print(f"see_all_profiles_ele  not found: {e}")
    try:
        time.sleep(0.4)
        wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{my_pprofile}" )]' )))      
        my_profile_ele = driver.find_element( By.XPATH, 
                     f'//span[contains(text(), "{my_pprofile}" )]' )
        profile_parent_ele = my_profile_ele.find_element(By.XPATH, './/../../../../../../..')
        #print("profile ")
        print( f"my_profile_ele {profile_parent_ele.is_selected()} {profile_parent_ele.tag_name} {profile_parent_ele.accessible_name} {profile_parent_ele.aria_role}  {profile_parent_ele.get_attribute('aria-checked')}\n"  )
        #print( f"my_profile_ele {my_profile_ele.is_selected()}  {my_profile_ele.get_attribute('outerHTML')}\n"  )
        if( profile_parent_ele.get_attribute('aria-checked') == "false"):
            my_profile_ele.click()
        
    except Exception as e:
        #action = ActionChains(driver);
        #action.move_to_element(my_profile_ele).perform();
        print(f"Profile {my_pprofile} not found: {e} ")
        
    time.sleep(1)
    driver.refresh()
    wait = WebDriverWait(driver, 30) 
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Hide Menu"]')))
    hide_side_ele = driver.find_element( By.XPATH, 
                 '//div[@aria-label="Hide Menu"]' )
    hide_side_ele.click()
    time.sleep(0.4)
    

# get sharable grupus url
def get_share_to_groups(driver, like_page_url):
    #//div[@aria-label="Send this to friends or post it on your Timeline."]
    #driver.refresh()
    ret_urls=[]
    html = driver.find_element(By.TAG_NAME, 'html')
    for i in range(2):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    
    
    share_button_list = driver.find_elements(By.XPATH, 
                                     '//div[@aria-label="Send this to friends or post it on your Timeline."]')    
    print(f"1 share_button_list = {share_button_list}\n")
    if(len(share_button_list)<1):
        html = driver.find_element(By.TAG_NAME, 'html')
        for i in range(2):
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
        share_button_list = driver.find_elements(By.XPATH, 
           '//div[@aria-label="Send this to friends or post it on your Timeline."]') 
        print(f"2 share_button_list = {share_button_list}")
        
    if len(share_button_list)>0:
        wait = WebDriverWait(driver, 6) 
        share_button_list[0].send_keys(Keys.ENTER)
        time.sleep(0.5)
        #share_button_list[0].click()
        #driver.switch_to.frame(share_button_list[0]);
        share_to_group = None
        try:
            xpath_group_str =  '//span[contains(text(),"Share to a group")]' 
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_group_str)))
            share_to_group = driver.find_element( By.XPATH, xpath_group_str)        
            share_to_group.click()
            time.sleep(0.5)
        except: 
            xpath_str =  '//*[contains(text(),"More options")]'
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_str)))
            more_opts = driver.find_element( By.XPATH, xpath_str )
            time.sleep(0.5)
            more_opts.click()
            time.sleep(0.5)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_group_str)))
            share_to_group = driver.find_element( By.XPATH, xpath_group_str)        
            share_to_group.click()
            time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]')))
        share_group_list = driver.find_elements(By.XPATH, 
              '//div[@role="listitem"]' )
        print(f"share_group_list = {share_group_list}\n")
        for group_name in share_group_list:
            group_link_ele = group_name.find_element(By.XPATH, './/a')
            print( f"URI {group_link_ele.get_attribute('href')}\n" )
            if group_link_ele.get_attribute('href'):
                ret_urls.append(group_link_ele.get_attribute('href'))
    return ret_urls
            

def create_post(driver, post):
    ret_urls=[]
    html = driver.find_element(By.TAG_NAME, 'html')

    wait = WebDriverWait(driver, 6) 
    xpath_str = '//*[contains(text(),"Write something...")]'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_str)))
    more_opts = driver.find_element( By.XPATH, xpath_str )
    time.sleep(0.5)
    more_opts.click()    
    #<div aria-describedby="placeholder-40iv2" aria-label="Write something..." 
    # class="notranslate _5rpu" contenteditable="true" role="textbox" spellcheck="true" tabindex="0" style="outline: none; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;"><div data-contents="true"><div class="x1e56ztr" data-block="true" data-editor="40iv2" data-offset-key="25r7f-0-0"><div data-offset-key="25r7f-0-0" class="_1mf _1mj"><span data-offset-key="25r7f-0-0"><br data-text="true"></span></div></div></div></div>    
    xpath_str = '//div[@role="textbox" and @spellcheck="true"]'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_str)))
    post_ele = driver.find_element( By.XPATH, xpath_str )
    post_ele.send_keys(Keys.SPACE ) ##Press ENTER
    post_ele.send_keys(post)
    post_ele.send_keys(Keys.ENTER) ### Press ENTER to post the content on facebook
    
    xpath_str = '//div[@aria-label="Post" and @role="button"]'
    post_button_ele = driver.find_element( By.XPATH, xpath_str )
    post_button_ele.click()
    
if __name__ == '__main__':
    # extract accounts from accounts file
    accounts = account_fun()
    for account in accounts:
        cookie_path = 'cookies/' + account[0] + '.txt'
        selenium_object = SeleniumDriver(cookies_file_path=cookie_path)
        driver = selenium_object.driver
        username = account[0]
        password = account[1]
        if is_fb_logged_in():
            print("Already logged in")
        else:
            print("Not logged in. Login")
            fb_login(driver, username, password)

        like_page_url = 'https://www.facebook.com/ExMuslimMurtadApostateIndia'    
        #r,i = managed_page(driver, like_page_url)
        switch_role_to_page(driver, my_pprofile="Ex-Muslim Murtad Apostate India")
        switch_role_to_page(driver, my_pprofile="Ex-Muslim Murtad Apostate India")
        ret_urls = get_share_to_groups(driver, like_page_url)
        for url in ret_urls:
            open_page(driver, url)
            create_post(driver, "Please support ExMuslim of India on youtube.")
        #print(i)        
        #getPage_id(driver=driver, pageurl = "https://www.facebook.com/groups/VaisnavaHumour/" )
        #scroll_down(driver, 2)
        #like_post(driver)
        #add_friend(driver)
        #like_page(driver)
        #selenium_object.quit()
        
        
        
