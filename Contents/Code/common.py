################################################################################
TITLE = "Tamil Serials"
VERSION = '0.01' # Release notation (x.y - where x is major and y is minor)
GITHUB_REPOSITORY = 'coder-alpha/TamilSerials.bundle'
PREFIX = "/video/tamilserials"
ART = "art-default.jpg"
ICON = "icon-tubetamil.png"
NAME = "Sun TV"

ICON_NEXT = "icon-next.png"
################################################################################
ChannelList='http://www.tamilserials.tv/'

Reffer = "http://www.tamilserials.tv/"

####################################################################################################

def GetThumb(channel):
  icon = ('icon-indiantv.png')

  if channel == "Kalaignar TV":
    icon = ('icon-kalaignartv.png')
  elif channel == "Jaya TV":
    icon = ('icon-jaya.png')
  elif channel == "Raj TV Serials":
    icon = ('icon-rajtv.png')
  elif channel == "Sun TV":
    icon = ('icon-suntv.png')
  elif channel == "Other TV Shows":
    icon = ('icon-indiantv.png')
  elif channel == "KB Serials":
    icon = ('icon-kb.png')
  elif channel == "Polimer TV":
    icon = ('icon-Polimer.png')
  elif channel == "Vendhar TV":
    icon = ('icon-vendhartv.png')
  elif channel == "Zee Tamil Serials":
    icon = ('icon-zeetv.png')
  elif channel == "Puthu Yugam TV":
    icon = ('icon-puthutv.png')
  elif channel == "Vijay TV":
    icon = ('icon-vijaytv.png')

  return icon

####################################################################################################