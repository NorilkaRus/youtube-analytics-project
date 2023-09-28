import json
import os

from googleapiclient.discovery import build

import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class InfoFromAPI(Exception):
    def __init__(self):
        self.message = "Несуществующий id видео"

class Video:
    """
    Класс для ютуб-видео
    """

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.id_video = video_id
        try:
            self.fill_channel_data()
        except InfoFromAPI as m:
            print(m.message)
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None

    def fill_channel_data(self):
        """Подтягиваем недостающие данные из API"""
        video_id = self.id_video
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id
                                               ).execute()
        if video_response['pageInfo']['totalResults'] != 0:
            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.channel_title: str = video_response['items'][0]['snippet']['channelTitle']
            self.url = f"https://www.youtube.com/watch?v={self._video_id}&ab_channel={self.channel_title}"
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        else:
            raise InfoFromAPI


    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id : str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/watch?v={self._video_id}&list={self.playlist_id}&ab_channel=" \
                   f"{self.channel_title}"

