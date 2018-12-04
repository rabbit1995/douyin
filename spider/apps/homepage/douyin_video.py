# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
import json
from bs4 import BeautifulSoup
from requests.packages import urllib3
import requests
import re


class Doyin_Download(object):

    def __init__(self, user_url):
        print("======================================================================= ")
        print("                      By Twelve billion_Eric                          ")
        print("                      Douyin_Video_Download                           ")
        print("                             Python3.5X                                 ")
        print("======================================================================= ")
        # 配置selenium
        self.__headers__ = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }
        self.__headers__
        self.__mobile_emulation__ = {
            'deviceName': 'iPhone X'
        }
        self.__options__ = webdriver.ChromeOptions()
        self.__options__.add_experimental_option(
            "mobileEmulation", self.__mobile_emulation__)
        self.browser = webdriver.Chrome(options=self.__options__)
        # 保存好三个参数
        self.user_url = user_url

    def get_url(self):
        res = requests.get(self.user_url,
                           headers=self.__headers__)
        test = res.text
        # 获取用户uid和dytk
        user_id = re.search('uid: "(\d+)', test).group(1)
        dytk = re.search("dytk: '(\w+)", test).group(1)
        # 个人主页网址所得到的响应
        url = 'https://www.amemv.com/aweme/v1/aweme/favorite/?user_id=%s&count=21&max_cursor=0&aid=1128&dytk=%s' % (
            user_id, dytk)
        url_list = [url]
        self.browser.get(url)
        # network中preview中源代码
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')
        # aweme_list中的作品信息
        web_data = json.loads(str(soup.pre.string))
        if web_data['status_code'] == 0:
            while web_data['has_more'] == 1:  # 只要has_more属性为1，就继续循环保存url
                max_cursor = web_data["max_cursor"]
                url = 'https://www.amemv.com/aweme/v1/aweme/favorite/?user_id=%s&count=21&max_cursor=%s&aid=1128&dytk=%s' % (
                    user_id, max_cursor, dytk)
                self.browser.get(url)
                response2 = self.browser.page_source
                soup2 = BeautifulSoup(response2, 'lxml')
                web_data = json.loads(str(soup2.pre.string))
                url_list.append(url)
            else:
                max_cursor = web_data["max_cursor"]
                url = 'https://www.amemv.com/aweme/v1/aweme/favorite/?user_id=%s&count=21&max_cursor=%s&aid=1128&dytk=%s' % (
                    user_id, max_cursor, dytk)
                url_list.append(url)
        self.url_list = url_list
        return url_list

    def get_download_url(self, url_list):
        download_url = []
        title_list = []
        if len(url_list) > 0:
            for url in url_list:  # 访问个人主页（可能分页了）的url，获得视频地址与每个视频的名称
                self.browser.get(url)
                response = self.browser.page_source
                soup = BeautifulSoup(response, 'lxml')
                web_data = json.loads(str(soup.pre.string))
                if web_data['status_code'] == 0:
                    for i in range(len(web_data['aweme_list'])):
                        download_url.append(web_data['aweme_list'][i]['video'][
                                            'play_addr']['url_list'][0])
                        title_list.append(web_data['aweme_list'][i][
                                          'share_info']['share_desc'])
        self.download_url = download_url
        self.title_list = title_list
        dict_url={}
        for i in range(len(download_url)):
            dict_url[title_list[i]]=download_url[i]
        return dict_url
        # return download_url,title_list
    def video_Download(self, download_url, title_list):  # 写入mp4
        for i in range(len(download_url)):
            title = str(title_list[i]).replace('/', ' ') + '.mp4'
            urllib3.disable_warnings()
            response = requests.get(
                download_url[i], headers=self.__headers__, verify=False)
            f = open(title, 'wb')
            f.write(response.content)
            print("%s is over" % title)
            f.close()

    def run(self):
        url_list = self.get_url()
        download_url, title_list = self.get_download_url(url_list)
        self.video_Download(download_url, title_list)


if __name__ == "__main__":
    user_url ='http://v.douyin.com/dvTSLL/'

    '''
	#用于测试    
	
	'''
    start = Doyin_Download(user_url)
    start.run()
