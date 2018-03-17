# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
from bs4 import BeautifulSoup


class NBACrawer:
    def __init__(self):
        self.pageIndex = 1;
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False


        # 传入某一页的索引获得页面代码

    def getPage(self, pageIndex):
        url = 'http://www.nba98.com/nbalx/list_175_' + str(pageIndex) + '.html'
        print  ("url = %s" ) % url;
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)

        data = response.read().decode('gb2312')
        return data;

        # 传入某一页代码，返回本页列表

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print
            "页面加载失败...."
            return None
        pageStories = []

        soup = BeautifulSoup(pageCode, 'html.parser');
        

        pattern = re.compile(
            '''<li> <span class="float_right">(.*?)</span> <a href='(.*?)' target="_blank">(.*?)</a> </li>''', re.S)
        items = re.findall(pattern, pageCode);
        for item in items:
            link = "http://www.nba98.com" + item[1].encode("utf-8");
            title = item[2].encode("utf-8");
            pageStories.append([link, title]);

            print(title);
        return pageStories

        # 加载并提取页面的内容，加入到列表中

    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:

            if len(self.stories) < 7:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                print (self.pageIndex);
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print("第%d页\ttitle=%s\t link:%s" % (page, story[1], story[0]))


    # 开始方法
    def start(self):
        print (u"正在读取NBA98  信息,按回车查看新信息，Q退出")
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)

print("start ---")
spider = NBACrawer();
spider.start();
