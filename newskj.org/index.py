#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: solar.lv
# @Date:   2019-03-08 19:04:28
# @Last Modified by:   lyb
# @Last Modified time: 2019-03-19 23:29:02
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import json
import time, datetime
import re
import requests
import md5

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
txt_path = "./newskj.txt"
txt_list = 0
def find_elements(self, key, value):
    elements = []
    try:
        if key == 'xpath':
            elements = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located((By.XPATH, value)))
        elif key == 'class_name':
            elements = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, value)))
        elif key == 'id':
            elements = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located((By.ID, value)))
        elif key == 'name':
            elements = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located((By.NAME, value)))
    except Exception as e:
        print(e)
    return elements

def post_data(post_title,post_content):
	post_url = ''
	requests.post(post_url)
	headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': '',
        'Origin': '',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }
	timestamp = int(time.time())
	nonce_str = str(timestamp) + "_" + ""
	m1 = md5.new()  
	m1.update(nonce_str)   
	nonce =  m1.hexdigest()
	payload = {
		'action': 'post_data',
		'timestamp' : timestamp,
		'nonce' : nonce,
		'lyb_post_title': post_title,
		'lyb_post_content': post_content,
	}
	r = requests.post(post_url,payload,headers = headers)
	print(r.text)

def getDetail():
	nextBotton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.paging b+a')))
	next_url = nextBotton.get_attribute('href')
	html = pq(browser.page_source,parser="html")
	current = html.find(".paging > b").text()
	content = html.find('.list-items')
	uls = content.find('ul').items()
	news = []
	i = 0
	for ul in uls:
		lis = ul.find('li').items()
		for li in lis:
			if len(li.find('a').text()) > 0: 
				time.sleep(2)
				i = i + 1
				href = "https://www.newskj.org" + li.find('a').attr("href")
				c = getContent(href)
				c = c.replace('【每日科技网】','')
				title = li.find('a').text().encode("utf-8")
				#new = dict();
				new = "INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`)"
				new += "VALUES ('1', curtime(), curtime(), '{}', '{}', '', 'publish', 'open', 'open', '', '', '', '', curtime(), curtime(), '', '0', '{}', '0', 'post', '', '0');" . format(c,title,href) + "\n"
				news.append(new)
				c = "<!-- wp:paragraph -->" + c + "<!-- /wp:paragraph -->"
				post_data(title,c)

def getContent(content_url):
	browser.get(content_url)
	html = pq(browser.page_source,parser="html")
	content = html.find('#main_content').text().encode("utf-8")
	return content

def next_detail():
    try:
        nextBotton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.paging b+a')))
        nextBotton.click()
        #wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#d_list > div > span.pagebox_num_nonce'), str()))
        getDetail()
    except TimeoutException:
        next_detail()



def get_mrkj_fun():
	url = "https://www.newskj.org/news/web/"
	browser.get(url)
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-l')))
	#获取页面总数
	total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.paging > a:last-child')))
	t_str = total.get_attribute('href')
	print(t_str)
	t = re.search('(?P<number>[0-9]{3})',t_str,re.U)
	total_num = int(t.groupdict()['number'])
	total_num = 2
	getDetail()
	for i in range(1, total_num + 1):
		next_detail()
	browser.quit()

if __name__ == '__main__':
	get_mrkj_fun()