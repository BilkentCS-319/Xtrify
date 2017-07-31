import urllib
import re
import Recommender

class Recommendation(Recommender.Recommender):
    def search(self, keywords):
        res_list = []
        url='http://export.arxiv.org/api/query?search_query='
        for eachKey in keywords[:len(keywords)-1]:
            url=url+'all:'+eachKey+'+AND+'
        else:
            url=url+'all:'+keywords[-1]

        resp=urllib.urlopen(url)
        respData=resp.read()
        respData = respData.replace('\n', '')
        titles = re.findall(r'<title>(.*?)</title>', str(respData))
        paragrahs=re.findall(r'<id>(.*?)</id>',str(respData))

        for i in range(len(titles)):
            res_list.append([titles[i], paragrahs[i+1]])
        print(titles)
        print(paragrahs)
        return res_list
