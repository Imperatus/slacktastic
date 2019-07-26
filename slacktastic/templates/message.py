from abc import abstractmethod
from datetime import datetime
from urllib.parse import quote
import json

from typing import List, Optional, Union, Dict
from slacktastic.exceptions import BadArgumentsError


class Base:
    @abstractmethod
    def to_slack(self):
        pass


class Attachment(Base):
    def __init__(
            self,
            title: Optional[str] = None,
            title_link: Optional[str] = None,
            pretext: Optional[str] = None,
            text: Optional[str] = None,
            footer: Optional[str] = None,
            footer_icon: Optional[str] = None,
            color: Optional[str] = None,
            fields: Optional[List['Field']] = None,
            formatting: str = 'mrkdwn',
            image_url: Optional[str] = None,
            thumb_url: Optional[str] = None,
            date_time: Optional[datetime] = None
    ):
        if all(not value for value in [title, text, fields]):
            raise BadArgumentsError(
                'Either `title`, `text` or `fields` required')
        self.title = title
        self.title_link = title_link
        self.pretext = pretext
        self.text = text
        self.footer = footer
        self.footer_icon = footer_icon
        self.image_url = image_url
        self.thumb_url = thumb_url
        self.date_time = date_time
        self.color = color
        self.fields = fields
        self.formatting = formatting

        if isinstance(fields, list):
            self.fields = fields
        else:
            self.fields = list()

    def to_slack(self):
        print(self.image_url)
        return {
            'title': self.title,
            'title_link': self.title_link,
            'pretext': self.pretext,
            'text': self.text,
            'footer': self.footer,
            'footer_icon': self.footer_icon,
            'image_url': self.image_url,
            'thumb_url': self.thumb_url,
            'ts': self.date_time.timestamp() if self.date_time else None,
            'color': self.color,
            'fields': [field.to_slack() for field in self.fields],
            'type': self.formatting,
        }


class Field:
    def __init__(
            self,
            title: str,
            value: Union[str, int, float, bool],
            short: Optional[bool] = True
    ):
        self.title = title
        self.value = value
        self.short = short

    def to_slack(self):
        return {
            'title': self.title,
            'value': self.value,
            'short': self.short
        }


class Diagram(Attachment):
    def __init__(
            self,
            title: str,
            data: Dict
    ):
        self.data = data
        super().__init__(title=title)

    def to_slack(self):
        pass


class PieChart(Attachment):
    def __init__(
            self,
            title: str,
            data: Dict
    ):
        image_url = self._compute_image_url(data)
        super().__init__(title, image_url=image_url, thumb_url=image_url)

    @staticmethod
    def _compute_image_url(data):
        base_url = "https://quickchart.io/chart"
        labels = data.get('labels', [])
        values = data.get('values', [])
        escaped = quote(f"{{type: 'pie',data: {{labels: {labels},"
                        f"datasets: [{{data: {values}}}]}}}}")
        parameters = f"?c={escaped}"
        return base_url + parameters


class Message(Base):
    def __init__(
            self,
            text: Optional[str] = None,
            attachments: List[Optional[Attachment]] = None
    ):
        if all(not value for value in [text, attachments]):
            raise BadArgumentsError('Either `text` or `attachments` required')

        self.text = text
        if isinstance(attachments, list):
            self.attachments = attachments
        else:
            self.attachments = list()

    def to_slack(self):
        return {
            'text': self.text,
            'attachments': [
                attachment.to_slack() for attachment in self.attachments]
        }
