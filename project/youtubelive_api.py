    
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

##    printUploadedVideos(uploaded_videos)
    return uploaded_videos

def createBroadcast(youtube):
    options = {
        'broadcast_title' : 'New Broadcast Type',
         'privacy_status' : 'private',
             'start_time' : '2017-01-30T00:00:00.000Z',
               'end_time' : '2017-01-31T00:00:00.000Z' }

    new_broadcast_body = dict.fromkeys(('snippet','status'))
    new_broadcast_body['snippet'] = {
        'title' : options['broadcast_title'],
        'scheduledStartTime' : options['start_time'],
        'scheduledEndTime' : options['end_time'] }
    new_broadcast_body['status'] = {
        'privacyStatus' : options['privacy_status']
        }
    
    broadcast_response = youtube.liveBroadcasts().insert(
        part='snippet,status',
        body=new_broadcast_body
    ).execute()

    snippet = broadcast_response['snippet']

    print "Broadcast '%s' with title '%s' was published at '%s'." % (
        broadcast_response["id"], snippet["title"], snippet["publishedAt"])
    return broadcast_response["id"]

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
