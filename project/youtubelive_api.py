
#############################################################
########################  Constants  ########################
#############################################################

DEFAULT_BROADCAST_TITLE = 'Broadcast Python Example'
DEFAULT_BROADCAST_PRIVACY_STATUS = 'private'
DEFAULT_BROADCAST_START_TIME = '2017-12-30T00:00:00.000Z'
DEFAULT_BROADCAST_END_TIME = '2017-12-31T00:00:00.000Z'

#############################################################
#####################  Main functions  ######################
#############################################################

def createBroadcast(youtube):
    # Set broadcast options and snippet details (body)
    options = {
        'broadcast_title' : DEFAULT_BROADCAST_TITLE,
         'privacy_status' : DEFAULT_BROADCAST_PRIVACY_STATUS,
             'start_time' : DEFAULT_BROADCAST_START_TIME,
               'end_time' : DEFAULT_BROADCAST_END_TIME }

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

    print 'Broadcast "%s" with title "%s" was published at "%s".' % (
        broadcast_response['id'], broadcast_response['snippet']['title'],
        broadcast_response['snippet']['publishedAt'])
    return broadcast_response['id']

def getAllUpcomingBroadcasts(youtube):
    upcoming_broadcasts = []

    list_broadcasts_request = youtube.liveBroadcasts().list(
        broadcastStatus='upcoming',
        part='id,snippet',
        maxResults=50
    )

    while list_broadcasts_request:
        list_broadcasts_response = list_broadcasts_request.execute()

        for broadcast in list_broadcasts_response.get('items',[]):
            upcoming_broadcasts.append(broadcast)

        list_broadcasts_request = youtube.liveBroadcasts().list_next(
            list_broadcasts_request,list_broadcasts_response)

    return upcoming_broadcasts

def getUpcomingBroadcastWithName(upcoming_broadcasts,name):
    for broadcast in upcoming_broadcasts:
        broadcast_name = broadcast['snippet']['title']
        if (broadcast_name == name):
            print 'Found broadcast "%s" with title "%s".' % (
                broadcast['id'], broadcast['snippet']['title'])
            return broadcast['id']
    print 'No broadcasts where found.'
    return None

def getUpcomingBroadcastExample(upcoming_broadcasts):
    return getUpcomingBroadcastWithName(upcoming_broadcasts,DEFAULT_BROADCAST_TITLE)

def getOrCreateBroadcastExample(youtube):
    upcoming_broadcasts = getAllUpcomingBroadcasts(youtube)
    broadcast_example_id = getUpcomingBroadcastExample(upcoming_broadcasts)

    if (broadcast_example_id == None):
        broadcast_id = createBroadcast(youtube)
        return broadcast_id
    return broadcast_example_id

def getLiveStreamStatusFromId(youtube,stream_id):
    list_streams_request = youtube.liveStreams().list(
        part='id,snippet,status',
        id=stream_id,
    )

    list_streams_response = list_streams_request.execute()
    stream = list_streams_response['items'][0]
    print 'Stream "%s" with title "%s" has status "%s".' % (
        stream['id'],stream['snippet']['title'],stream['status']['streamStatus'])
    
def getAllLiveStreams(youtube):
    live_streams = []

    list_streams_request = youtube.liveStreams().list(
        part='id,snippet',
        mine=True,
        maxResults=50
    )

    while list_streams_request:
        list_streams_response = list_streams_request.execute()

        for stream in list_streams_response.get('items', []):
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

def controlBroadcast(youtube,broadcast_id,stream_id,broadcast_status):
    stream_status = getLiveStreamStatusFromId(youtube,stream_id)

    if (stream_status != 'active'):
        print 'The stream is inactive. Cannot start broadcast'
        return
    
    transition_broadcast_response = youtube.liveBroadcasts().transition(
        part='id,status',
        id=broadcast_id,
        broadcastStatus=broadcast_status
    ).execute()

    print 'Broadcast "%s" was transitioned to status "%s".' % (
        transition_broadcast_response['id'],
        transition_broadcast_response['status']['recordingStatus'])

def startBroadcast(youtube,broadcast_id,stream_id):
    controlBroadcast(youtube,broadcast_id,stream_id,'live')

def stopBroadcast(youtube,broadcast_id,stream_id):
    controlBroadcast(youtube,broadcast_id,stream_id,'complete')

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
