import json
import os

from googleapiclient.discovery import build

import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id

        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel['items'][0]['id']}"
        self.subscriberCount = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']


    def __str__(self):
        return f"{self.title} ({self.url})"


    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount


    def __sub__(self, other):
        return self.subscriberCount - other.subscriberCount


    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount


    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount


    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount


    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel_info)


    @property
    def channel_id(self):
        return self._channel_id


    @classmethod
    def get_service(cls):
        return youtube


    def to_json(self, file):
        with open(file, "a") as json_file:
            return json.dump(self.__dict__, json_file, indent=2, ensure_ascii=False)