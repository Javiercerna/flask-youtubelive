    
def createBroadcast(youtube):
    # Set broadcast options and snippet details (body)
    options = {
        'broadcast_title' : 'Broadcast Python 1',
         'privacy_status' : 'private',
             'start_time' : '2017-12-30T00:00:00.000Z',
               'end_time' : '2017-12-31T00:00:00.000Z' }

    new_broadcast_body = dict.fromkeys(('snippet','status'))
    new_broadcast_body['snippet'] = {
                     'title' : options['broadcast_title'],
        'scheduledStartTime' : options['start_time'],
          'scheduledEndTime' : options['end_time'] }
    new_broadcast_body['status'] = {
             'privacyStatus' : options['privacy_status'] }

    # Create new broadcast from details
    broadcast_response = youtube.liveBroadcasts().insert(
        part='snippet,status',
        body=new_broadcast_body
    ).execute()

    snippet = broadcast_response['snippet']

    print 'Broadcast "%s" with title "%s" was published at "%s".' % (
        broadcast_response['id'], snippet['title'], snippet['publishedAt'])
    return broadcast_response['id']

def getAllLiveStreams(youtube):
    live_streams = []

    list_streams_request = youtube.liveStreams().list(
        part='id,snippet',
        mine=True,
        maxResults=50
    )

    while list_streams_request:
        list_streams_response = list_streams_request.execute()

        for stream in list_streams_response.get("items", []):
            live_streams.append(stream)
        
        list_streams_request = youtube.liveStreams().list_next(
            list_streams_request, list_streams_response)

    return live_streams

def getLiveStreamWithQuality(live_streams,quality):
    for stream in live_streams:
        stream_quality = stream['snippet']['title'].split('-')[-1]
        if (stream_quality == quality):
            print 'Found stream "%s" with title "%s".' % (
                stream['id'], stream['snippet']['title'])
            return stream['id']
    print 'No streams where found.'
    return None

def getLiveStream1080p(live_streams):
    return getLiveStreamWithQuality(live_streams,'1080p')
    
def getLiveStream720p(live_streams):
    return getLiveStreamWithQuality(live_streams,'720p')

def getLiveStream480p(live_streams):
    return getLiveStreamWithQuality(live_streams,'480p')

def getLiveStream240p(live_streams):
    return getLiveStreamWithQuality(live_streams,'240p')

def bindBroadcast(youtube,broadcast_id,stream_id):
    bind_broadcast_response = youtube.liveBroadcasts().bind(
        part='id,contentDetails',
        id=broadcast_id,
        streamId=stream_id
    ).execute()

    print 'Broadcast "%s" was bound to stream "%s".' % (
        bind_broadcast_response['id'],
        bind_broadcast_response['contentDetails']['boundStreamId'])

#############################################################
#########  Helpers to test basic API functionality  #########
#############################################################

def getUploadedVideos(youtube):
    uploaded_videos = []
    channels_response = youtube.channels().list(
      mine=True,
      part='contentDetails'
    ).execute()

    for channel in channels_response['items']:
        # Playlist id of videos uploaded
        uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']

        # Request to retrieve list of videos uploaded
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part='snippet',
            maxResults=50
        )

        # Append videos uploaded object to list
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()
            
            for playlist_item in playlistitems_list_response['items']:
                uploaded_videos.append(playlist_item)
                
            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    return uploaded_videos

def printUploadedVideos(uploaded_videos):
    for video in uploaded_videos:
        title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        print '%s (%s)' % (title,video_id)
    
def createTemplateFromUploadedVideos(uploaded_videos):
    template = ''
    for video in uploaded_videos:
        title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        template += '%s (%s) <br>' % (title,video_id)
    return template
