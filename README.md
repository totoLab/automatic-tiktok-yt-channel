# Automatic TikTok YT channel

## Based on
- [Google guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [YT Tutorial](https://youtu.be/N5jMX6erNeo)

## Project creation:
### Google Console:
- New project
- API key creation (unrestricted): key should be bound to a static ip address (or to a range - CIDR)
- OAuth 2.0 Client IDs (Desktop Client type): specify redirect (code assumes localhost)

### Code samples: 
- [x] Google 2.x: https://github.com/youtube/api-samples/blob/master/python/upload_video.py
- [ ] Updated 3.x: https://github.com/kjellski/youtube-upload-video-py

### Usage
` $ command.sh /path/to/file.mp4 "Title of the video" `

### Capabilities
- [ ] video fetching
- [ ] video editing
- [x] upload video to youtube, given an API key in [client_secret.json](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [ ] automatic authorization token filling
- [ ] upload planning
- [ ] cronjob (fetch -> edit -> upload)

### Dependencies
```
pip install oauth2client google-auth-oauthlib
```