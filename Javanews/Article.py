# -*- coding:utf-8 -*-

class Article:



    def __init__(self, title, link):
        self.title = title
        self.link = link

    def setTitle(self ,title):
        self.title = title

    def setLink(self ,link):
        self.link = link

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def __repr__(self):
        return "[" + self.title + " , " +self.link +" (__repr__)"


