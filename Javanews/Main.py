# -*- coding: utf-8 -*-
from FetchJava import JavaFetch
import time, threading

javaCrawer = JavaFetch()


def download(ite):
    javaCrawer.htmlToMd(ite.getTitle(), ite.getLink())


if __name__=="__main__":
    for index in range(16, 82, 1):
        j = 0;
        for ite in javaCrawer.getListInpage(index):
            t = threading.Thread(target=download, args={ite, }, name=('LoopThread %d' % j))
            t.start()
            j += 1;
            time.sleep( (index * j ) % 5)

