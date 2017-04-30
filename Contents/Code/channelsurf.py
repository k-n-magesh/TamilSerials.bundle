from lxml import etree
import urllib2
import common
import urlparse
import re
import time
import datetime

SITETITLE = 'suntv'
SITETHUMB = 'icon-desirulez.png'


DESIRULEZMOVIES = ['Latest & Exclusive Movie HQ']

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON


####################################################################################################
@route(PREFIX + '/channels')
def ChannelsMenu(url,tvselection):
    oc = ObjectContainer(title1=(tvselection))
    page_data = HTML.ElementFromURL(url)
    #thumb=R(common.ART)
    linkURL = page_data.xpath("//a[contains(., 'Browse Channels')]")
    ##Log(etree.tostring(linkURL[0], pretty_print=True))
    #oc.add(DirectoryObject(key = Callback(ChannelsMenu, url='http://www.tubetamil.com/category/tamil-comedy-show/feed',tvselection='Tamil Comedy'), title = 'Tamil Comedy', thumb = R('icon-comedy.png')))
    #oc.add(DirectoryObject(key = Callback(ChannelEpisodesList, url=common.VIJAY_SITEURL,title='Vijay TV Serials'), title = 'Vijay TV Serials', thumb = R('icon-vijaytv.png')))
    #ChannelEpisodesList(oc,common.VIJAY_SITEURL,"Vijay TV")
    Log(url)
    #feed = RSS.FeedFromURL(url)
    Log(feed.entries)
    for item in feed.entries:
            channelName = item.title
            channelURL = item.link
            Log(channelName)
            #thumb=common.GetThumb(channelName)
            #oc.add(DirectoryObject(key = Callback(EpisodesMenu, url=link,title=heading), title = channel, thumb = 'icon-9xinxmedia.png'))
            oc.add(DirectoryObject(key = Callback(EpisodesMenu, url=channelURL,tvselection=channelName), title = channelName, thumb ='icon-9xinxmedia.png'))
    
    #oc = ObjectContainer(title1=(tvselection))
    #feed = RSS.FeedFromURL(url)
    #Log(feed.entries)
    #for item in feed.entries:
            #channel = item.title
            #link = item.link
            #heading = channel.split(None, 1)[0]
            #oc.add(DirectoryObject(key = Callback(EpisodesMenu, url=link,title=heading), title = channel, thumb = 'icon-9xinxmedia.png'))

    # If there are no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=SITETITLE, message=L('ChannelWarning'))

    return oc

####################################################################################################

@route(PREFIX + '/getvideolist')
def EpisodesMenu(url,title):
    oc = ObjectContainer(title2=title)
    #Log(url)
    endpos=url.rfind('/')
    newurl=url[:endpos]
    newurl=newurl+"/feed"
    newurl= newurl.replace(".com/",".com/category/")

    feed = RSS.FeedFromURL(newurl)
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            link = item.link
            ##Log(channel)
            #oc.add(DirectoryObject(key = Callback(EpisodesView, url=link,title=title), title = channel, thumb = 'icon-9xinxmedia.png'))
            EpisodesView(oc,link,channel,common.ART)

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc


def EpisodesView(oc,url,title,thumb):
    page_data = HTML.ElementFromURL(url)
    linkURL = page_data.xpath("/html/body//a[contains(@href,'youtube')]/@href")
    #Log(linkURL)
    if not linkURL:
         linkURL = page_data.xpath("//iframe[contains(@src,'youtube')]/@src")
    if not linkURL:
         linkURL = page_data.xpath("//iframe[contains(@src,'dailymotion')]/@src")
    if linkURL[0].startswith("//") == True:
        linkURL[0]='http:'+linkURL[0]
    #Log(linkURL)
    if linkURL[0].startswith("http") == True:
        #Log(linkURL[0])
        summary = None
        rating = None
        duration = 0
        originally_available_at = None

        oc.add(VideoClipObject(
				url = linkURL[0],
				title = title,
            	summary = summary,
				duration = duration,
				rating = rating,
				originally_available_at = originally_available_at,
				thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=R(common.ART))))

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc



def ChannaleList(oc,url):
    page_data = HTML.ElementFromURL(url)
    #thumb=R(common.ART)
    linkURL = page_data.xpath("//a[contains(., 'Browse Channels')]")
    ##Log(etree.tostring(linkURL[0], pretty_print=True))
    #oc.add(DirectoryObject(key = Callback(ChannelsMenu, url='http://www.tubetamil.com/category/tamil-comedy-show/feed',tvselection='Tamil Comedy'), title = 'Tamil Comedy', thumb = R('icon-comedy.png')))
    #oc.add(DirectoryObject(key = Callback(ChannelEpisodesList, url=common.VIJAY_SITEURL,title='Vijay TV Serials'), title = 'Vijay TV Serials', thumb = R('icon-vijaytv.png')))
    #ChannelEpisodesList(oc,common.VIJAY_SITEURL,"Vijay TV")
    Log(url)
    #feed = RSS.FeedFromURL(url)
    Log(feed.entries)
    for item in feed.entries:
            channelName = item.title
            channelURL = item.link
            Log(channelName)
            #thumb=common.GetThumb(channelName)
            #oc.add(DirectoryObject(key = Callback(EpisodesMenu, url=link,title=heading), title = channel, thumb = 'icon-9xinxmedia.png'))
            oc.add(DirectoryObject(key = Callback(ChannelsMenu, url=channelURL,tvselection=channelName), title = channelName, thumb ='icon-9xinxmedia.png'))
    
    return oc


###########################################################################################################################

@route(PREFIX + '/getchannellist')
def ChannelEpisodesList(url,title):
    oc = ObjectContainer(title2=title)
    #Log(url)
    #title=None
    #endpos=url.rfind('/')
    #newurl=url[:endpos]
    #newurl=newurl+"/feed"
    #newurl= newurl.replace(".com/",".com/category/")

    feed = RSS.FeedFromURL(url)
    page_data = HTML.ElementFromURL(url.replace("/feed","/"))
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            #link = item.link
            #Log(channel)
            #Log(link)
            category = str(item.tags[0]['term'])
            #Log(category)
            try:
                if 'Serial' in category:
                    category = str(item.tags[1]['term'])
                    #Log(category)
                if 'Serial' in category:
                    category = str(item.tags[2]['term'])
                    #Log(category)
            except:
                continue
            chncategory = category
            #Log(category)
            category=category.replace(" ","-")

            newurl=url.replace("feed",(category+"/feed"))
            #Log(newurl)
            imgURL=getEpisodeImage(page_data,chncategory)
            oc.add(DirectoryObject(key = Callback(ChannelEpisodesMenu, url=newurl,title=channel,category=category,imgURL=imgURL), title = channel, thumb = imgURL))
            #EpisodesView(oc,link,channel)

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc
#//span[contains(.,'TV Serials')]


@route(PREFIX + '/getchannelvideolist')
def ChannelEpisodesMenu(url,title,category,imgURL):
    oc = ObjectContainer(title1=title)
    #Log(url)
    feed = RSS.FeedFromURL(url)
    #page_data = HTML.ElementFromURL(url.replace("/feed","/"))
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            link = item.link
            #Log(channel)
            #oc.add(DirectoryObject(key = Callback(EpisodesView, url=link,title=title), title = channel, thumb = 'icon-9xinxmedia.png'))
            #getEpisodeImage(page_data,category)
            EpisodesView(oc,link,channel,imgURL)

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc


def getEpisodeImage(page_data,episodeName):
    #Log(episodeName)
    episodeName= episodeName
    episodeFName=episodeName.partition(' ')[0]
    #Log(episodeFName)
    #Log(episodeName)
    #page_data = HTML.ElementFromURL(common.EpisodeImageURL)
    thumbURL = page_data.xpath("//img[contains(@alt, '"+episodeName+"')]/@src")
    #Log(episodeName + str(len(thumbURL)))
    #Log(len(thumbURL))
    if len(thumbURL) ==0:
        episodeName=episodeName.replace(" ","-")
        thumbURL = page_data.xpath("//img[contains(@alt, '"+episodeName+"')]/@src")
        #Log(episodeName + str(len(thumbURL)))
    #Log(episodeName)
    if len(thumbURL) ==0:
        episodeName=episodeName.replace("-","")
        thumbURL = page_data.xpath("//img[contains(@alt, '"+episodeName+"')]/@src")
        #Log(episodeName + str(len(thumbURL)))
    if len(thumbURL) ==0:
        thumbURL = page_data.xpath("//img[contains(@alt, '"+episodeFName+"')]/@src")
        #Log(episodeFName + str(len(thumbURL)))
        #Log(episodeFName)

    #Log(episodeName)
    #if not thumbURL:
    try:
        #Log(thumbURL[0])
        episodeImgUrl=thumbURL[0]
    except:
        episodeImgUrl='icon_video.png'

    #Log(episodeImgUrl)

    return episodeImgUrl
    #https://forums.plex.tv/discussion/45957/thumbnails-not-showing-up