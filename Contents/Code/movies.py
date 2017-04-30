from lxml import etree
import urllib2
import common
import urlparse
import re
import time
import datetime

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON


####################################################################################################
@route(PREFIX + '/movies')
def MoviesMenu(url,movieselection,pageCount):
    oc = ObjectContainer(title1=(movieselection))
    newurl= url
    feed = RSS.FeedFromURL(url+pageCount)
    page_data = HTML.ElementFromURL(newurl.replace("/feed/?paged=","/page/")+pageCount)
    #Log(feed.entries)
    for item in feed.entries:
            channel = item.title
            link = item.link
            #Log(item.tags[0])
            #pubDate = str(item.tags[0]['pubDate'])
            #Log(pubDate)
            movieImg=getMovieImage(page_data,channel)
            #heading = item.title.split(None, 1)[0]
            oc.add(DirectoryObject(key = Callback(VideoLink, url=link,title=channel), title = channel, thumb = Resource.ContentsOfURLWithFallback(url=movieImg, fallback=R(common.ART))))

    if (len(oc) >=10):
        oc.add(NextPageObject(
            key = Callback(MoviesMenu,url=url ,movieselection=movieselection,pageCount=int(pageCount) + 1),
            title = "More...",
            thumb = R(common.ICON_NEXT)
                )
            )

    # If there are no channels, warn the user
    if len(oc) == 1:
        return ObjectContainer(header=SITETITLE, message=L('ChannelWarning'))

    return oc

####################################################################################################

@route(PREFIX + '/getvideolink')
def VideoLink(url,title):
    oc = ObjectContainer(title2=title)
    #Log('test')
    #Log(url)
    page_data = HTML.ElementFromURL(url)
    linkURL = page_data.xpath("//iframe[contains(@src,'www.playhd.video')]/@src")
    #Log(linkURL)
    MovieView(oc,linkURL[0],title,common.ART)

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc


def MovieView(oc,linkURL,title,thumb):
    page_data = HTML.ElementFromURL(linkURL)
    #linkURL = page_data.xpath("/html/body//a[contains(@href,'youtube')]/@href")
    #Log(linkURL)
    #if not linkURL:
    linkURL = page_data.xpath("//source[contains(@src,'media')]/@src")
    #if not linkURL:
         #linkURL = page_data.xpath("//iframe[contains(@src,'dailymotion')]/@src")
    #Log(linkURL)
    if linkURL[0].startswith("//") == True:
        linkURL[0]='http:'+linkURL[0]
    #Log(linkURL)
    if linkURL[0].startswith("http") == True:
        #Log(linkURL[0])
        summary = None
        originally_available_at = None

        oc.add(CreateVideoClipObject(
				url = linkURL[0],
				title = title,
            	summary = summary,
				originally_available_at = originally_available_at
				))

    # If there are  no channels, warn the user
    if len(oc) == 0:
        return ObjectContainer(header=title, message=L('EpisodeWarning'))

    return oc


@route(PREFIX +'/createvideoclipobject')
def CreateVideoClipObject(url, title, summary, originally_available_at, include_container=False):

	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, originally_available_at=originally_available_at, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		originally_available_at = originally_available_at,
		items = [
			MediaObject(
				parts = [
					PartObject(key=url)
				],
				container = Container.MP4,
				video_codec = VideoCodec.H264,
				video_resolution = '544',
				audio_codec = AudioCodec.AAC,
				audio_channels = 2,
				optimized_for_streaming = True
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

def MovieList(oc):
    ICON_MOVIES='icon-movies.png'
    oc.add(DirectoryObject(key = Callback(MoviesMenu, url=common.MoviesNew,movieselection='New Tamil Movies',pageCount=1), title = 'New Tamil Movies', thumb = R(ICON_MOVIES)))
    oc.add(DirectoryObject(key = Callback(MoviesMenu, url=common.MoviesHD,movieselection='HD Tamil Movies',pageCount=1), title = 'HD Tamil Movies', thumb = R(ICON_MOVIES)))
    return oc


def getMovieImage(page_data,episodeName):
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