# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import html2text
from  Article import Article
import utils
from HtmlToMd import markdownify as md

import time, threading
class JavaFetch:
    def __init__(self):
        self.pageIndex = 1;
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}


    def getPageData(self, page):
        url = "http://www.importnew.com/all-posts/page/" + str(page)
        print "\n****************" + url + "****************"

        return self.requestUrl(url)

    def requestUrl(self, url, index = 0):
        if index > 4:
            pass
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            data = response.read();
        except:
            index += 1;
            data = self.requestUrl(url, index)

        data = data.decode('utf-8')
        return data;

    def getArticles(self, archiveEle):
        liEles = archiveEle.find_all('div', {'class': 'post floated-thumb'})
        liArticles = [];
        for liEle in liEles:
            liArticleEles = liEle.select('.meta-title ')
            for articleEle in liArticleEles:
                url = articleEle['href']
                title = articleEle.contents[0]

                liArticles.append(Article(utils.toString(title),  utils.toString(url)))

            # tag
            liArticleTags = liEle.find_all('a', attrs={"rel": "category tag"})
            if liArticleTags:
                tag = liArticleTags[0].contents[0]
                print  "tag:  %s" % tag
        for it in liArticles:
            print it.getTitle()
            print it.getLink()
        return  liArticles

    def getListInpage(self, pageIndex):
        page = self.getPageData(pageIndex);
        allList = []
        if (page):
            soup = BeautifulSoup(page, 'html.parser')
            archives = soup.find_all(id='archive')
            archive = None
            for archive in archives:
                if archive:
                    allList.extend(self.getArticles(archive))
        return allList


    def saveToFiles(self, filename, content):
        fo = open("mds/%s.md" % (filename.replace("/", "")) ,"w")
        fo.write(content)

        # 关闭打开的文件
        fo.close()

    def htmlToMd(self, title, url):
        page =  utils.toString( self.requestUrl(url))
        print "-- article-- %s %s" % (url,title)
        if (page):
            soup = BeautifulSoup(page, 'html.parser')
            entry = utils.toString(soup.find_all('div', {'class': 'entry'})[0])
            print  entry
            mdStr = utils.toString(md(entry))
            id = self.getArticleId(url)
            self.saveToFiles(id + "_" + utils.toString(title)  , mdStr)



    def getArticleId(self, url):
        return url[url.rfind("/",0) + 1 :url.rfind(".html",0)]







javaCrawer = JavaFetch()

def download(ite):
    javaCrawer.htmlToMd(ite.getTitle(), ite.getLink())


for index in range(1, 2, 1):


    for  ite in javaCrawer.getListInpage(index):
       t =  threading.Thread(target=download, args={ite,}, name=('LoopThread %d'%j))
       t.start()
# url = "http://www.importnew.com/28260.html"
# javaCrawer.htmlToMd('cyning', url)
