# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

Versao = "19.07.01"

def getmd5(t):
	value_altered = ''.join(chr(ord(letter)-1) for letter in t)
	return value_altered

AddonID = 'plugin.video.Raiden'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
usuario = Addon.getSetting("user")

addonDir = Addon.getAddonInfo('path').decode("utf-8")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

#URLP = getmd5("iuuq;00xxx/b{wpewjq/pomjof0cbtfbee0")
URLP = "https://brplay.xyz/painel/baseadd"
#URLP = "http://localhost:8080/base/"
addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cFonte1 = Addon.getSetting("cFonte1")
cFonte2 = Addon.getSetting("cFonte2")
cFonte3 = Addon.getSetting("cFonte3")

cTxt1 = Addon.getSetting("cTxt1")
cTxt2 = Addon.getSetting("cTxt2")
cTxt3 = Addon.getSetting("cTxt3")

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewS2():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')	
	xbmc.executebuiltin("Container.SetViewMode(\"55\")")
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')
	
def Categories(): #70
	try:
		link = urllib2.urlopen( URLP + "/c/"+usuario+".php" ).read()
		link2 = urllib2.urlopen( URLP + "/c/"+link+".php" ).read().replace("\r","")
		m = link2.split("\n")
		for a in m:
			q = a.split(";")
			if "dir/" in q[1]:
				AddDir("[COLOR "+q[2]+"]"+q[0]+"[/COLOR]", q[1], 73, q[3], q[3], isFolder=True, IsPlayable=False, info="")
			else:
				AddDir("[COLOR "+q[2]+"]"+q[0]+"[/COLOR]", q[1], 71, q[3], q[3], isFolder=True, IsPlayable=False, info="")
	except:
		AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)
		
def Categories2(): #71
	try:
		link = urllib2.urlopen(URLP+"/"+url).read()
		m = re.compile('tvg\-logo\=\"([^\"]+).+,(.+)\s(.+)|,(.+)\s(.+)').findall(link)
		i=0
		for img2,name2,a,name3,c in m:
			AddDir(name2+name3, url, 72, img2, img2, isFolder=False, IsPlayable=True, info="", background=str(i))
			i+=1
	except:
		AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)

def Dirr(): #73
	try:
		link2 = urllib2.urlopen( URLP + "/" + url ).read()
		m = link2.split("\n")
		for a in m:
			q = a.split(";")
			if "dir/" in q[1]:
				AddDir("[COLOR "+q[2]+"]"+q[0]+"[/COLOR]", q[1], 73, q[3], q[3], isFolder=True, IsPlayable=False, info="")
			else:
				AddDir("[COLOR "+q[2]+"]"+q[0]+"[/COLOR]", q[1], 71, q[3], q[3], isFolder=True, IsPlayable=False, info="")
			#AddDir("[COLOR "+q[2]+"]"+q[0]+"[/COLOR]", q[1], 71, q[3], q[3], isFolder=True, IsPlayable=False, info="")
	except:
		AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)
		
def Playy(): #72
	link = urllib2.urlopen(URLP+"/"+url).read()
	m = re.compile('tvg\-logo\=\"([^\"]+).+,(.+)\s(.+)|,(.+)\s(.+)').findall(link)
	#xbmcgui.Dialog().ok('Cube Play',   str(m[int(background)][1]) + str(m[int(background)][3])  )
	PlayUrl(str(m[int(background)][1]) + str(m[int(background)][3]), str(m[int(background)][2]) + str(m[int(background)][4]) , "", "", "")
	
def PlayUrl(name, url, iconimage=None, info='', sub='', metah=''):
	#url = re.sub('\.mp4$', '.mp4?play', url)
	url = common.getFinalUrl(url)
	#xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	if metah:
		listitem.setInfo(type="Video", infoLabels=metah)
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
def PlayTVCB(): #103
	try:
		PlayUrl(name, getmd5(url), "", "", "")
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', "Servidor offline, tente novamente em alguns minutos")
# --------------  Fim menu

# --------------  FIM MMfilmes

def Data(x):
	x = eInfo = re.sub('\d\d(\d+)\-(\d+)\-(\d+)', r'\3/\2/\1', x )
	return "[COLOR yellow]("+x+")[/COLOR]"
def EPI(x):
	x = re.sub('[0]+(\d+)', r'\1', x )
	return x
def AddDir(name, url, mode, iconimage='', logos='', index="", move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', DL='', year='', metah={}, episode=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'index': index, 'info': info, 'background': background, 'DL': DL, 'year': year, 'metah': metah, 'episode': episode}
	if metah:
		if background and episode:
			mg = metahandlers.MetaData()
			#sInfo = mg.get_seasons(metah['TVShowTitle'], metah['imdb_id'], [1])
			eInfo = mg.get_episode_meta(metah['TVShowTitle'], metah['imdb_id'], background, EPI(episode))
			liz=xbmcgui.ListItem(DL+background+"."+EPI(episode)+" "+eInfo['title'] +" "+Data(eInfo['premiered'])+ " [COLOR blue]["+str(eInfo['rating'])+"][/COLOR]", iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			liz.setArt({"thumb": eInfo['cover_url'], "poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'] })
			infoLabels = {}
			infoLabels['Premiered'] = "2018-01-01"
			liz.setInfo( type="Video", infoLabels= eInfo )
		else:
			liz=xbmcgui.ListItem(name, iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			liz.setArt({"poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
			liz.setInfo( type="Video", infoLabels= metah )
	else:
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
		#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
	
	
def CheckUpdate(): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/robinhoodtvip/brplay/master/versao.py" ).read().replace('\n','').replace('\r','')
		uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
		#xbmcgui.Dialog().ok(Versao, uversao)
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except:
		pass

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/robinhoodtvip/brplay/master/default.py" ).read().replace('\n','')
		prog = re.compile('#checkintegrity25852').findall(fonte)
		if prog:
			py = os.path.join( Path, "default.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
		xbmc.sleep(2000)
	except:
		xbmcgui.Dialog().ok('Addon', "Ocorreu um erro, tente novamente mais tarde")

def Refresh():
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ST(x):
	x = str(x)
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, "w")
	file.write(x)
	file.close()

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
url = params.get('url')
logos = params.get('logos', '')
name = params.get('name')
iconimage = params.get('iconimage')
cache = int(params.get('cache', '0'))
index = params.get('index')
move = int(params.get('move', '0'))
mode = int(params.get('mode', '0'))
info = params.get('info')
background = params.get('background')
DL = params.get('DL')
year = params.get('year')
metah = params.get('metah')
episode = params.get('episode')

if mode == 0:
	Categories()
	setViewM()
	CheckUpdate()
if mode == 71:
	Categories2()
	setViewM()
if mode == 72:
	Playy()
if mode == 73:
	Dirr()
	setViewM()
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
elif mode == 103:
	PlayTVCB()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852
