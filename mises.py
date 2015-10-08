# -*- coding: utf-8 -*-
import urllib2
import re
import os
import multiprocessing

def downloadBook(fileName_Link):
	(fileName, link) = fileName_Link
	if not os.path.exists(fileName):
		timesToTry = 4
		downloaded = False
		while timesToTry > 0 and not downloaded:
			timesToTry -= 1
			try:
				bookFile = urllib2.urlopen(link, timeout=20).read()
				downloaded = True
				with open(fileName, 'wb') as f:
					f.write(bookFile)
			except Exception, e:
				pass
		if not downloaded:
			return fileName_Link

def func():
	baseUrl="https://mises.org/library/books?book_type=All&title=All&author=All&topic=All&austrian_school=All&level=All&page="
	pageNum=0
	maxPageNum=54

	bookPages=[]
	pattern = re.compile(r'<h2 class="teaser-title"><a href="(.*?)">')
	while pageNum < maxPageNum:
		print "loading page", pageNum
		page = urllib2.urlopen(baseUrl+str(pageNum), timeout=20).read()
		find = pattern.findall(page)
		bookPages.extend(find)
		pageNum += 1

	fileName_Link = []
	pattern = re.compile(r'href="(.*?\?file=1.*?)"')
	for page in bookPages:
		page = "https://mises.org" + page
		bookPage = urllib2.urlopen(page, timeout=20).read()
		findLink = pattern.findall(bookPage)
		for fileLink in findLink:
			bookDownloadLink = fileLink
			print bookDownloadLink
			fileName = urllib2.unquote(bookDownloadLink.split('/')[-1].split('?')[0]).decode('utf-8')
			fileName_Link.append((fileName, bookDownloadLink))

	print fileName_Link

	pool = multiprocessing.Pool(processes = 6)
	outputs = pool.map(downloadBook, fileName_Link)
	pool.close()
	pool.join()

	for output in outputs:
		if output != None:
			print output

if __name__ == '__main__':
	func()