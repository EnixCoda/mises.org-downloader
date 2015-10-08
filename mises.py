# -*- coding: utf-8 -*-
import urllib2
import re
import os
import multiprocessing

def multiThreadWork(func, arr, processes):
	pool = multiprocessing.Pool(processes = processes)
	outputs = pool.map(func, arr)
	pool.close()
	pool.join()
	return outputs

def getThisUrl(url, timeout):
	notSucceed = True
	timesToTry = 4
	while notSucceed and timesToTry>0:
		try:
			timesToTry-=1
			response = urllib2.urlopen(url, timeout = timeout).read()
			notSucceed=False
		except Exception, e:
			pass
	if notSucceed:
		print 'exception:', e, 'url: ', url
		return False
	else:
		return response

def downloadBook(fileName_Link):
	(fileName, link) = fileName_Link
	if not os.path.exists(fileName):
		timesToTry = 4
		bookFile = getThisUrl(link, 30)
		if bookFile:
			with open(fileName, 'wb') as f:
				f.write(bookFile)
		else:
			return 'Failed at', fileName_Link

def getBookPage(bookPageUrl):
	bookFileUrlpattern = re.compile(r'href="(.*?\?file=1.*?)"')
	bookPageUrl = "https://mises.org" + bookPageUrl
	bookPage = getThisUrl(bookPageUrl, 20)
	if bookPage:
		bookDownloadLinks = bookFileUrlpattern.findall(bookPage)
		fileName_Link = []
		for bookDownloadLink in bookDownloadLinks:
			fileName = urllib2.unquote(bookDownloadLink.split('/')[-1].split('?')[0]).decode('utf-8')
			fileName_Link.append((fileName, bookDownloadLink))
		return fileName_Link

def getListPage(pageNum):
	baseUrl = "https://mises.org/library/books?book_type=All&title=All&author=All&topic=All&austrian_school=All&level=All&page="
	pageUrl = baseUrl + str(pageNum)
	page = getThisUrl(pageUrl, 20)
	if page:
		bookPageUrlPattern = re.compile(r'<h2 class="teaser-title"><a href="(.*?)">')
		find = bookPageUrlPattern.findall(page)
		return find

if __name__ == '__main__':
	maxPageNum=55
	bookPageUrls = multiThreadWork(getListPage, range(maxPageNum), 8)
	bookPageUrls = reduce(lambda x, y: x+y, bookPageUrls)
	fileName_Links = multiThreadWork(getBookPage, bookPageUrls, 8)
	fileName_Links = reduce(lambda x, y: x+y, fileName_Links)
	bookDownload = multiThreadWork(downloadBook, fileName_Links, 6)
	for output in bookDownload:
		if output != None:
			print output