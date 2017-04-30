
feed = RSS.FeedFromURL(FEED_URL)

for item in feed.entries:
    url = item.enclosures[0]['url']
    title = item.title
    summary = item.summary
    originally_available_at = Datetime.ParseDate(item.updated)
    duration = Datetime.MillisecondsFromString(item.itunes_duration)