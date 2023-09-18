import json
import os

from googleapiclient.discovery import build

import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Класс для ютуб-видео
    """

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._video_id = video_id

        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()

        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.channel_title: str = video_response['items'][0]['snippet']['channelTitle']
        self.url = f"https://www.youtube.com/watch?v={self._video_id}&ab_channel={self.channel_title}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']


    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id : str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/watch?v={self._video_id}&list={self.playlist_id}&ab_channel=" \
                   f"{self.channel_title}"
