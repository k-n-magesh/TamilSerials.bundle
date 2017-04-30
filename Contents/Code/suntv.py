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
@route(PREFIX + '/suntv/channels')
def ChannelsMenu(url,tvselection):
    oc = ObjectContainer(title1=('Serials'))
    feed = RSS.FeedFromURL(url)
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            link = item.link
            heading = channel.split(None, 1)[0]
            oc.add(DirectoryObject(key = Callback(EpisodesMenu, url=link,title=heading), title = channel, thumb = 'icon-9xinxmedia.png'))

    # If there are no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=SITETITLE, message=L('ChannelWarning'))

    return oc

####################################################################################################

@route(PREFIX + '/suntv/episodesmenu')
def EpisodesMenu(url,title):
    oc = ObjectContainer(title2=title)
    Log(url)
    endpos=url.rfind('/')
    newurl=url[:endpos]
    newurl=newurl+"/feed"
    newurl= newurl.replace(".com/",".com/category/")

    feed = RSS.FeedFromURL(newurl)
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            link = item.link
            oc.add(DirectoryObject(key = Callback(EpisodesView, url=link,title=title), title = channel, thumb = 'icon-9xinxmedia.png'))

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc

@route(PREFIX + '/suntv/episodesview')
def EpisodesView(url,title):
    oc = ObjectContainer(title2=title)
    Log(url)
    page_data = HTML.ElementFromURL(url)
    thumb=R(common.ART)
    linkURL = page_data.xpath("/html/body//a[contains(@href,'youtube')]/@href")[0]
    Log(linkURL)

    if linkURL.startswith("http") == True:
        oc.add(VideoClipObject(
				url = linkURL,
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(common.ART))))

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc


