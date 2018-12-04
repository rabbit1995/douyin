# coding: utf-8
from __future__ import print_function
from pprint import pprint
import re
import requests
from parsel import Selector

try:
    from urllib.parse import urljoin
except ImportError:
    from six.moves.urllib.parse import urljoin

#获取url源码
def download(url, proxy=None, rain_num=2):
    print("dowing", url)
    heads = {
        'Accept': 'text/*, application/xml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.douyin.com",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        html = requests.get(url, headers=heads).text
    except Exception as e:
        print("Downing error", e.reason)
        html = None
        if rain_num > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:   #hasatter判断对象是否包含对应的属性
                return download(url, rain_num - 1)
    return html

#爬取抖音用户的信息
def spider(user_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    res = requests.get(user_url,
                       headers=headers)
    test = res.text
    # 获取用户uid
    uid = re.search('uid: "(\d+)', test).group(1)
    url = "https://www.douyin.com/share/user/%s" % uid
    body = download(url)
    xbody = Selector(text=body)
    item = dict()
	#获取用户名
    nick_name = xbody.xpath("//p[@class='nickname']/text()").extract_first()

    #获取作品数
    try:
        works = xbody.xpath("//div[@class='user-tab active tab get-list']/span").extract_first()
        works = re.findall('>([\s\S]+?)<', works)
    except TypeError:
	    works = xbody.xpath("//*[@id='pagelet-user-info']/div[3]/div/div[2]/span").extract_first()
	    works = re.findall('>([\s\S]+?)<', works)

    works = jiexi(works).strip()

	#获取喜欢数
    like_num = xbody.xpath("//div[@class='like-tab tab get-list']/span").extract_first()
    like_num = re.findall('>([\s\S]+?)<', like_num)
    like_num = jiexi(like_num).strip()

	#获取用户ID
    douyin_id = xbody.xpath("//p[@class='shortid']").extract_first()
    douyin_id = re.findall('>([\s\S]+?)<', douyin_id)
    douyin_id = jiexi(douyin_id).replace("抖音ID：", '').strip()

    #获取简单信息，如微博认证等
    try:
        info = xbody.xpath("//span[@class='info']/text()").extract_first().strip()
    except Exception as e:
        info = ''

	#获取关注数
    guanzhu = xbody.xpath("//span[contains(@class,'focus block')]/span[@class='num']").extract_first()
    guanzhu = re.findall('>([\s\S]+?)<', guanzhu)
    guanzhu = jiexi(guanzhu)

	#获取粉丝数
    fans = xbody.xpath("//span[contains(@class,'follower block')]/span[@class='num']").extract_first()
    fans = re.findall('>([\s\S]+?)<', fans)
    fans = jiexi(fans)

	#获取赞数
    zan = xbody.xpath("//span[contains(@class,'liked-num block')]/span[@class='num']").extract_first()
    zan = re.findall('>([\s\S]+?)<', zan)
    zan = jiexi(zan)

    #获取详细信息
    info_de = xbody.xpath("//p[@class='signature']/text()").extract_first()

    #获取用户头像
    head = xbody.xpath("//span[@class='author']/img[@class='avatar']").extract_first()
    head = re.findall('https://\S+jpeg',head)
    head = ''.join(head)





	#将信息放入字典
    item['douyin_id'] = douyin_id
    item['nick_name'] = nick_name
    item["fans"] = fans
    item["zan"] = zan
    item["guanzhu"] = guanzhu
    item['works'] = works
    item['like_num'] = like_num
    item['info'] = info
    item['info_de']=info_de
    item['head'] = head
    pprint(item)
    return item

#解析字体加密
def jiexi(lists):
    pat = {
        "\ue60d": 0,
        "\ue603": 0,
        "\ue616": 0,
        "\ue60e": 1,
        "\ue618": 1,
        "\ue602": 1,
        "\ue605": 2,
        "\ue610": 2,
        "\ue617": 2,
        "\ue611": 3,
        "\ue604": 3,
        "\ue61a": 3,
        "\ue606": 4,
        "\ue619": 4,
        "\ue60c": 4,
        "\ue60f": 5,
        "\ue607": 5,
        "\ue61b": 5,
        "\ue61f": 6,
        "\ue612": 6,
        "\ue608": 6,
        "\ue61c": 7,
        "\ue60a": 7,
        "\ue613": 7,
        "\ue60b": 8,
        "\ue61d": 8,
        "\ue614": 8,
        "\ue615": 9,
        "\ue61e": 9,
        "\ue609": 9,
        "w": "w",
        ".": "."
    }
    _li = list()
    for i in lists:
        if str(i).strip():
            i = i.replace('<i class="icon iconfont follow-num">', "").strip()
            i = i.replace('<i class="icon iconfont ">', "").strip()
            i = i.replace('<i class="icon iconfont tab-num">', "").strip()
            i = pat.get(i, i)
            _li.append(str(i))
    return "".join(_li)


if __name__ == '__main__':
    '''
    	#用于测试    
    	http://v.douyin.com/dvTSLL/
    	'''
    user_url = 'http://v.douyin.com/dvTSLL/'
    spider(user_url)