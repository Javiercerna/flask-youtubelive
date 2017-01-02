
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
