######################################################################################
#
#	http://www.cooltamilserials.com/
#
######################################################################################

import common, updater
import channelsurf
import movies

TITLE = common.TITLE
PREFIX = common.PREFIX
ART = "art-default.jpg"
ICON = "icon-common.png"
ICON_LIST = "icon-list.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_NEXT = "icon-next.png"
ICON_MOVIES = "icon-movies.png"
ICON_SERIES = "icon-series.png"
ICON_QUEUE = "icon-queue.png"
ICON_UPDATE = "icon-update.png"
ICON_UNAV = "icon-unav.png"
ICON_PREFS = "icon-prefs.png"
ICON_LANG = "icon-lang.png"




BASE_URL = "http://www.tamilserials.tv/"
LANG_URL = "/category/watch-tamil-serials-online"
#CATEGORY_BLURAY_URL = 'bluray'
#CATEGORY_HD_URL = 'movies'
SEARCH_URL = "http://www.tamilserials.tv/"

# http://www.tubetamil.com/category/watch-tamil-serials-online/watch-sun-tv-serials

######################################################################################
# Set global variables

def Start():
	#HTTP.CacheTime = CACHE_1HOUR
	#ObjectContainer.title1 = TITLE
	#ObjectContainer.art = R(ART)
	#DirectoryObject.thumb = R(ICON_LIST)
	#DirectoryObject.art = R(ART)
	#VideoClipObject.thumb = R(ICON_MOVIES)
	#VideoClipObject.art = R(ART)

	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	# Setup the default attributes for the ObjectContainer
	ObjectContainer.title1 = TITLE
	ObjectContainer.view_group = 'List'
	ObjectContainer.art = R(ART)

	# Setup the default attributes for the other objects
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	#NextPageObject.thumb = R(ICON)

	
	#HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
	HTTP.Headers['Referer'] = 'http://www.tamilserials.tv/'
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():


	oc = ObjectContainer()
	Log("test")
	channelsurf.ChannaleList(oc,common.ChannelList)
	#movies.MovieList(oc)
	#channelsurf.ChannelEpisodesList(oc,common.VIJAY_SITEURL,"Vijay TV")
	#oc.add(DirectoryObject(key = Callback(suntv.ChannelsMenu, url=common.SUN_SITEURL,tvselection='Sun TV'), title = 'Sun TV', thumb = R(ICON_SUNTV)))
	#oc.add(DirectoryObject(key = Callback(suntv.ChannelsMenu, url=common.VIJAY_SITEURL,tvselection='Vijay TV'), title = 'Vijay TV', thumb = R(ICON_VIJAYTV)))
	#oc.add(DirectoryObject(key = Callback(suntv.ChannelsMenu, url=common.RAJ_SITEURL,tvselection='Raj TV'), title = 'Raj TV', thumb = R(ICON_RAJTV)))
	return oc



#//span[contains(.,'TV Serials')] 

