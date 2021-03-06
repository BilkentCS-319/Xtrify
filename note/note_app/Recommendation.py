import urllib
import re


class Recommendation:

    def search(self, keywords):
        res_list = []
        url='http://export.arxiv.org/api/query?search_query='
        for eachKey in keywords[:len(keywords)-1]:
            url=url+'all:'+eachKey+'+OR+'
        else:
            url=url+'all:'+keywords[-1]

        resp=urllib.urlopen(url)
        respData=resp.read()
        respData = respData.replace('\n', '')
        titles = re.findall(r'<title>(.*?)</title>', str(respData))
        paragrahs=re.findall(r'<id>(.*?)</id>',str(respData))

        for i in range(len(titles)):
            res_list.append([titles[i], paragrahs[i+1]])
        
        return res_list

    def recommend(self, keywords):
        res_list = []
        url_begin = 'http://export.arxiv.org/api/query?search_query=all:'
        url_end = '&start=0&max_results=2'

        for w in keywords:
            url = url_begin+w+url_end
            resp = urllib.urlopen(url)
            respData = resp.read()
            respData = respData.replace('\n', '')
            titles = re.findall(r'<title>(.*?)</title>', str(respData))
            paragrahs = re.findall(r'<id>(.*?)</id>',str(respData))

            res_list.append([titles, paragrahs])

        return res_list
