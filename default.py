#!/usr/bin/python
# -*- coding: utf-8 -*-
#/*
# *      Copyright (C) 2011 by tolin
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# */
import urllib2, re, xbmc, xbmcgui, xbmcplugin, os, urllib, urllib2, socket, math, operator, base64

socket.setdefaulttimeout(12)

h = int(sys.argv[1])
icon = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),'icon.png'))

def showMessage(heading, message, times = 50000):
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def GET(url):
	try:
		print 'def GET(%s):'%url
		req = urllib2.Request(url)
		f = urllib2.urlopen(req)
		a = f.read()
		f.close()
		return a
	except:
		showMessage('Не могу открыть URL def GET', url)
		return None
	    
def GETSER(url):
#	    showMessage('url input in GETSER', url)
	    http = GET(urllib.unquote_plus(params['url']))
#	    showMessage ('http in GETSER', http)
	    r1 = re.compile("<div id='dle-content'>(.*?)<!--/PLAYER--><!-- div players -->", re.S).findall(http)
	    ro1 = re.compile('<a href="(.*?)" onclick=', re.DOTALL).findall(r1[0])
	    ro2 = re.compile('&amp;pl=(.*?)" /><embed src=',re.S).findall(r1[0])
	    pl = DEC(ro2[0])
#	    list = DEC(GET(urllib.unquote_plus(pl)))
#	    print (list)	    
#	    roo = re.compile('<!--PLAYER--><div id="players" class="player">(.*?)</div> <!--/PLAYER-->', re.DOTALL).findall(http)
#	    showMessage ('rows1 in GETSER', list)
#	    ro1 = re.compile('value="(.*?)" /><param').findall(roo[0])
#	    ro2 = re.split('&amp;', ro1[4])
#	    ro2 = ro2[2]
#	    ro2 = re.split('file=',ro2)
#	    ro2 = ro2[1]
#	    showMessage('список серий', ro2)
	    return pl



def ROOT():

        name='Фильмы'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=video_sub'
        xbmcplugin.addDirectoryItem(h, url, li, True)
        
        name='Сериалы'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=serial_sub'
        xbmcplugin.addDirectoryItem(h, url, li, True)
	
#	name='Поиск'
#        li = xbmcgui.ListItem(name)
#        url = sys.argv[0] + '?mode=search'
#        xbmcplugin.addDirectoryItem(h, url, li, True)
        		
	xbmcplugin.endOfDirectory(h)


def video_sub():
    
	name='Жанры'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=genre'
        xbmcplugin.addDirectoryItem(h, url, li, True)
    
	name='Фильмы от А-Я, 0-9'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=ROOT3'+'&url=%s'%urllib.quote_plus('http://filmix.net/?do=archive')
        xbmcplugin.addDirectoryItem(h, url, li, True)
        xbmcplugin.endOfDirectory(h)
    
def serial_sub():
    
	name='Популярные'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=top_view'
        xbmcplugin.addDirectoryItem(h, url, li, True)
	
	name='Новые Cериалы'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=OPEN_SER'+'&url=%s'%urllib.quote_plus('http://filmix.net/serialy/')
        xbmcplugin.addDirectoryItem(h, url, li, True)

	name='Сериалы от А-Я, 0-9'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=ROOT4'+'&url=%s'%urllib.quote_plus('http://filmix.net/?do=serials')
        xbmcplugin.addDirectoryItem(h, url, li, True)
        xbmcplugin.endOfDirectory(h)
    
def search():
	xbmcplugin.endOfDirectory(h)
	
def genre():
	wurl = 'http://filmix.net/'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<div class="block categories">(.*?)</ul>',re.S).findall(http)
	r2 = re.compile('<li><a href="(.*?)">(.*?)</a>',re.S).findall(r1[0])
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "cp1251"), iconImage=icon, thumbnailImage=icon)
#		i = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://filmix.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	
	xbmcplugin.endOfDirectory(h)

def top_view():
	wurl = 'http://filmix.net/'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<div class="block serials">(.*?)</ul>',re.S).findall(http)
	r2 = re.compile('<li><a href="(.*?)" target="_blank">(.*?)</a></li>').findall(r1[0])
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "cp1251"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES4'
		u += '&url=%s'%urllib.quote_plus('http://filmix.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	
	xbmcplugin.endOfDirectory(h)

	
def ROOT1():
	wurl = 'http://filmix.net/'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<li class="li_year"><a href="(.*?)" class="rollerDate">(.*?)</a></li>').findall(http)
	if len(r1) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name in r1:
		i = xbmcgui.ListItem(unicode(name, "cp1251"), iconImage=icon, thumbnailImage=icon)
#		i = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://filmix.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)


def OPEN_MOVIES(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
#	rows = re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)" /></a>').findall(http)
	r1 = re.compile('<div id="container">(.*?)</div><!-- #content-->',re.S).findall(http)
	r2 = re.compile('<h2><a href="(.*?)">(.*?)</a></h2>',re.S).findall(r1[0])
#	#r3 = re.compile('|left--><a href="(.*?)" onclick',re.S).findall(r1[0])
	r3 = re.compile('><img src="(.*?)" style="float:left;" alt=',re.I).findall(r1[0])
	r4 = re.compile('<br />(.*?)</div>',re.S).findall(r1[0])
	
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов href, img, alt')
		return False
	ii = 0
	name='[B][COLOR blue]Жанры[/COLOR][/B]'
        li = xbmcgui.ListItem(name)
        url = sys.argv[0] + '?mode=genre'
        xbmcplugin.addDirectoryItem(h, url, li, True)
	for href, alt in r2:
			img = 'http://filmix.net' + r3[ii]
#			img = icon
			text = r4[ii]
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "cp1251"), iconImage=img, thumbnailImage=img)
			i.setInfo(type='video', infoLabels={'title': unicode(alt, "cp1251"), 'plot': unicode(text, "cp1251")})
#			i = xbmcgui.ListItem(alt, iconImage=img, thumbnailImage=img)
#			i.setInfo(type='video', infoLabels={'title': alt, 'plot': text})
			u  = sys.argv[0] + '?mode=PLAY1'
			u += '&url=%s'%urllib.quote_plus(href)
			i.setProperty('IsPlayable', 'true')
			xbmcplugin.addDirectoryItem(h, u, i)
	try:
		rp = re.compile('<div class="pages">(.*?)</div>', re.DOTALL).findall(http)[0]
		rp2 = re.compile('<a href="(.*?)">(.*?)</a>').findall(rp)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=OPEN_MOVIES'
			u += '&url=%s'%urllib.quote_plus(href)
#			rPN = '[B][COLOR yellow]%s[/COLOR][/B]' % rPN
			i = xbmcgui.ListItem('[ Страница %s ]'%nr)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	xbmcplugin.endOfDirectory(h)
	
def OPEN_SER(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
#	rows = re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)" /></a>').findall(http)
	r1 = re.compile('<div id="container">(.*?)</div><!-- #content-->',re.S).findall(http)
	r2 = re.compile('<h2><a href="(.*?)">(.*?)</a></h2>',re.S).findall(r1[0])
#	#r3 = re.compile('|left--><a href="(.*?)" onclick',re.S).findall(r1[0])
	r3 = re.compile('><img src="(.*?)" style="float:left;" alt=',re.I).findall(r1[0])
	r4 = re.compile('<br />(.*?)</div>',re.S).findall(r1[0])
	r5 = re.compile('<li class="rating">(.*?)</font>', re.S).findall(r1[0])
	
			
	
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов href, img, alt')
		return False
	ii = 0
#	name='[B][COLOR blue]Жанры[/COLOR][/B]'
#        li = xbmcgui.ListItem(name)
#        url = sys.argv[0] + '?mode=genre'
#        xbmcplugin.addDirectoryItem(h, url, li, True)
	for href, alt in r2:
			img = 'http://filmix.net' + r3[ii]
			r6 = re.compile('<b>(.*?)</b>').findall(r5[ii])
			r6 = str(r6)
#			r6 = r6.replace("'[", "")
			
			alt = alt + '  ' + r6
#			img = icon
			text = r4[ii]
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "cp1251"), iconImage=img, thumbnailImage=img)
			i.setInfo(type='video', infoLabels={'title': unicode(alt, "cp1251"), 'plot': unicode(text, "cp1251")})
#			i = xbmcgui.ListItem(alt, iconImage=img, thumbnailImage=img)
#			i.setInfo(type='video', infoLabels={'title': alt, 'plot': text})
			u  = sys.argv[0] + '?mode=OPEN_MOVIES4'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&name=%s'%urllib.quote_plus(alt)
			
			xbmcplugin.addDirectoryItem(h, u, i, True)
			
			
	try:
		rp = re.compile('<div class="pages">(.*?)</div>', re.DOTALL).findall(http)[0]
		rp2 = re.compile('<a href="(.*?)">(.*?)</a>').findall(rp)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=OPEN_SER'
			u += '&url=%s'%urllib.quote_plus(href)
#			rPN = '[B][COLOR yellow]%s[/COLOR][/B]' % rPN
			i = xbmcgui.ListItem('[ Страница %s ]'%nr)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	xbmcplugin.endOfDirectory(h)


def ROOT3():
#	wurl = 'http://filmix.net'
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	rs0 = re.compile('<ul class="catalog">(.*?)<div class="sidebar" id="sideLeft">', re.DOTALL).findall(http)
#	r1 = re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(http)
#    rs0 = re.compile('<ul class="catalog">(.*?)<div class="sidebar" id="sideLeft">', re.DOTALL).findall(http)
	rs = re.compile('<div class="full-link"><a href="(.+?)" class="showfull">(.+?)</a></div>\s*<div class="letter">(.+?)</div>').findall(rs0[0])  
	if len(rs) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name, name1 in rs:
		i = xbmcgui.ListItem(unicode(name, "cp1251") + ' ' + unicode(name1, "cp1251"), iconImage=icon, thumbnailImage=icon)
#		i = xbmcgui.ListItem(name + ' ' + name1, iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES2'
		u += '&url=%s'%urllib.quote_plus('http://filmix.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
		#showMessage('dss', u)
	xbmcplugin.endOfDirectory(h)


def OPEN_MOVIES2(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	showMessage('url mov2', params['url'])
	rows0 = re.compile('<ul class="catalog">(.*?)</ul>', re.DOTALL).findall(http)
	rows = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(rows0[0])
	if len(rows) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов href, img, alt')
		return False
	for href, alt in rows:
			img = icon
			i = xbmcgui.ListItem(unicode(alt, "cp1251"), iconImage=img, thumbnailImage=img)
#			i = xbmcgui.ListItem(alt, iconImage=img, thumbnailImage=img)
			u  = sys.argv[0] + '?mode=PLAY1'
			u += '&url=%s'%urllib.quote_plus('http://filmix.net/' + href)
			#u += '&name=%s'%urllib.quote_plus(name)
			i.setProperty('IsPlayable', 'true')
			#xbmcplugin.addDirectoryItem(h, u, i, True)
			xbmcplugin.addDirectoryItem(h, u, i)

	xbmcplugin.endOfDirectory(h)


def DEC(param):
    
    hash1 = ("l","u","T","D","Q","H","0","3","G","1","f","M","p","U","a","I","6","k","d","s","b","W","5","e","y","=");
    hash2 = ("w","g","i","Z","c","R","z","v","x","n","N","2","8","J","X","t","9","V","7","4","B","m","Y","o","L","h");

    for i in range(0, len(hash1)):
        rr1 = hash1[i]
        rr2 = hash2[i]

        param = param.replace(rr1, '--')
        param = param.replace(rr2, rr1)
        param = param.replace('--', rr2)
	
    
    param = base64.b64decode(param)
    
    return param

def PLAY1(params):
	http = GET(urllib.unquote_plus(params['url']))
#	showMessage('url in Play', params['url'])
	if http == None: return False
	rows1 = re.compile('&amp;file=(.+?)&amp;').findall(http)
	link = DEC(rows1[0])
#	showMessage('rows1[0]', rows1[0])
	showMessage('rows1[0]', link)
	if len(rows1) == 0:
		showMessage('ОЙ', 'Нет FLV-видеофайла')
		return False
	i = xbmcgui.ListItem(path = link)
	xbmcplugin.setResolvedUrl(h, True, i)


def ROOT4():
#	wurl = 'http://filmix.net'
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	rs0 = re.compile('<ul class="catalog">(.*?)<div class="sidebar" id="sideLeft">', re.DOTALL).findall(http)
#	r1 = re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(http)
#    rs0 = re.compile('<ul class="catalog">(.*?)<div class="sidebar" id="sideLeft">', re.DOTALL).findall(http)
	rs = re.compile('<div class="full-link"><a href="(.+?)" class="showfull">(.+?)</a></div>\s*<div class="letter">(.+?)</div>').findall(rs0[0])  
	if len(rs) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name, name1 in rs:
		i = xbmcgui.ListItem(unicode(name, "cp1251") + ' ' + unicode(name1, "cp1251"), iconImage=icon, thumbnailImage=icon)
#		i = xbmcgui.ListItem(name + ' ' + name1, iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES3'
		u += '&url=%s'%urllib.quote_plus('http://filmix.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
		#showMessage('dss', u)
	xbmcplugin.endOfDirectory(h)


def OPEN_MOVIES3(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	rows0 = re.compile('<ul class="catalog">(.*?)</ul>', re.DOTALL).findall(http)
	rows = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(rows0[0])
	rr = rows[0]
#	showMessage('rows  mov3', rr)
	if len(rows) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов href, img, alt')
		return False
	for href, alt in rows:
			img = icon
			hhtt = href
			i = xbmcgui.ListItem(unicode(alt, "cp1251"), iconImage=img, thumbnailImage=img)
#			i = xbmcgui.ListItem(alt, iconImage=img, thumbnailImage=img)
			u  = sys.argv[0] + '?mode=OPEN_MOVIES4'
			u += '&url=%s'%urllib.quote_plus('http://filmix.net/' + href)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def OPEN_MOVIES4(params):
#	showMessage ('mov4',params['url'])
	link = GET(urllib.unquote_plus(params['url']))
	htt = params['url']
#	imm = re.compile('<!--TBegin--><a href="(.*?)".*<!--TEnd-->',re.S).findall(link)
#	http = GET(urllib.unquote_plus(params['url']))
#	showMessage ('http in GETSER', http)
	r1 = re.compile("<div id='dle-content'>(.*?)<!--/PLAYER--><!-- div players -->", re.S).findall(link)
	ro1 = re.compile('<a href="(.*?)" onclick=', re.DOTALL).findall(r1[0])
	img1 = ro1[0]
#	img1 = str(imm)
#	showMessage('url mov4', img1)
	hhh = GETSER(htt)
#	showMessage('htt', hhh)
	hp = DEC(GET(urllib.unquote_plus(hhh)))
#	hp = hp.replace('{"playlist":','')
	hp = hp.replace('{"playlist":','')
	hp = hp.replace('"playlist":','')
#	hp = hp.replace('[{"comment":','{')
	hp = str(hp)
#	showMessage('hp', hp)
	if hp == None: return False
	rows = re.compile('".*?":"(.*?)",".*?":"(.*?).flv"',re.I).findall(hp)
#	rows = re.compile('comment":"(.*?)","file":"(.*?)"',re.S).findall(http)	
#	rows = re.compile('<title>(.*?)</title><location>(.*?)</location>',re.S).findall(http)
	if len(rows) == 0:
	    rows = re.compile('<title>(.*?)</title><creator>.*?</creator><location>(.*?)</location>',re.S).findall(hp)
#	    rows = re.compile('<title>(.*?)</title><creator>.*?</creator><location>(.*?)</location>',re.S).findall(http)
	if len(rows) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов')
		return False
	for alt, href in rows:
#			img = imm[0]
#			i = xbmcgui.ListItem(unicode(alt, "cp1251"), iconImage=icon, thumbnailImage=img)
			alt = '#' + alt
			alt = alt.replace('",[{"comment":"','#')
			altarr = alt.split('#')
			alt = altarr[len(altarr)-1]
			alt = alt.replace(')','')
			altarr = alt.split('(')
			alt = altarr[1] +  ' - ' + altarr[0]
			i = xbmcgui.ListItem(alt, iconImage=icon, thumbnailImage=icon)
#			u  = sys.argv[0] + '?mode=PLAY'
#			u += 'url=' + href
			u = href + '.flv'
			i.setProperty('IsPlayable', 'true')
			xbmcplugin.addDirectoryItem(h, u, i)
	xbmcplugin.endOfDirectory(h)


def PLAY(params):
	http = params['url']
#	showMassage ('http play', http)
        img = icon
	i = xbmcgui.ListItem('test', iconImage=img, thumbnailImage=img)
	xbmc.Player().play(http, i)
    #   k = 'http://video-6.filmix.net/s/c8b86969d4e1d410c030d1546130bfdf/1942/e04.flv'
#    i = xbmcgui.ListItem(path = k)
        xbmcplugin.setResolvedUrl(h, True, i)

def get_params(paramstring):
	param=[]
	if len(paramstring)>=2:
		params=paramstring
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=get_params(sys.argv[2])


mode = None

try:
	mode = urllib.unquote_plus(params['mode'])
except:
	ROOT()

if mode == 'OPEN_MOVIES': OPEN_MOVIES(params)

if mode == 'OPEN_SER': OPEN_SER(params)

if mode == 'ROOT4': ROOT4()
	
if mode == 'OPEN_MOVIES2': OPEN_MOVIES2(params)
	
if mode == 'OPEN_MOVIES3': OPEN_MOVIES3(params)
	
if mode == 'OPEN_MOVIES4': OPEN_MOVIES4(params)

if mode == 'ROOT3': ROOT3()

if mode == 'video_sub': video_sub()
if mode == 'serial_sub': serial_sub()
if mode == 'search': search()
if mode == 'genre': genre()
if mode == 'top_view': top_view()
if mode == 'PLAY': PLAY(params)
	
if mode == 'PLAY1': PLAY1(params)

