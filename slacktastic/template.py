from abc import abstractmethod
from datetime import datetime
from urllib.parse import quote

from typing import List, Optional, Union, Dict
from slacktastic.exceptions import ValidationError


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
            raise ValidationError(
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
    diagram_type = None
    BASE_URL = "https://quickchart.io/chart"

    def __init__(
            self,
            title: str,
            data: Dict,
            diagram_type: str,
            color: Optional[str] = None
    ):
        url = self._compute_image_url(data, diagram_type)
        super().__init__(
            title=title,
            color=color,
            image_url=url,
            thumb_url=url,
        )

    @abstractmethod
    def _validate_data(self, *args, **kwargs):
        pass

    def _compute_image_url(self, data: Dict, diagram_type: str):
        escaped = quote(f"{{type: '{diagram_type}',data: {data}}}")
        parameters = f"?c={escaped}"
        return self.BASE_URL + parameters


class Graph(Diagram):
    """
    For all diagrams with the following data payload:
        {
            "labels": List,
            "datasets": [
                {"label": str, "data": List}
            ]
        }
    """
    def __init__(
            self,
            title: str,
            labels: List,
            data: Dict,
            graph_type: str,
            color: Optional[str] = None
    ):
        self._validate_data(labels, data)
        formatted_data = {
            'labels': labels,
            'datasets': []
        }
        for label, values in data.items():
            formatted_data['datasets'].append({'data': values, 'label': label})

        super().__init__(
            title=title,
            data=formatted_data,
            diagram_type=graph_type,
            color=color)

    def _validate_data(
            self,
            labels: List[str],
            data: Dict[str, List[Union[int, float]]]
    ):
        label_len = len(labels)
        for key, values in data.items():
            if label_len != len(values):
                raise ValidationError(
                    f'Labels and values not the same size for "{key}"'
                )


class BarChart(Graph):
    def __init__(
            self,
            title: str,
            labels: List,
            data: Dict,
            color: Optional[str] = None
    ):
        super().__init__(title, labels, data, 'bar', color)


class LineChart(Graph):
    def __init__(
            self,
            title: str,
            labels: List,
            data: Dict,
            color: Optional[str] = None
    ):
        super().__init__(title, labels, data, 'line', color)


class RadarChart(Graph):
    def __init__(
            self,
            title: str,
            labels: List,
            data: Dict,
            color: Optional[str] = None
    ):
        super().__init__(title, labels, data, 'radar', color)


class FoodChart(Diagram):
    """
    Wrapper for Pie and Donut charts with the following payload:
        {
            "labels": List,
            "datasets": [
                {"data": List}
            ]
        }
    """

    def __init__(
            self,
            title: str,
            labels: List,
            values: List,
            graph_type: str,
            color: Optional[str] = None
    ):
        self._validate_data(labels, values)
        data = {
            'labels': labels,
            'datasets': [
                {'data': values}
            ]
        }
        super().__init__(
            title=title, data=data, diagram_type=graph_type, color=color)

    def _validate_data(
            self,
            labels: List[str],
            values: List[Union[int, float]]
    ):
        if len(labels) != len(values):
            raise ValidationError('Labels and values not the same size')


class PieChart(FoodChart):
    def __init__(
            self,
            title: str,
            labels: List,
            values: List,
            color: Optional[str] = None
    ):
        super().__init__(
            title=title,
            labels=labels,
            values=values,
            graph_type='pie',
            color=color
        )


class DonutChart(FoodChart):
    def __init__(
            self,
            title: str,
            labels: List,
            values: List,
            color: Optional[str] = None
    ):
        super().__init__(
            title=title,
            labels=labels,
            values=values,
            graph_type='doughnut',
            color=color
        )


class Message(Base):
    def __init__(
            self,
            text: Optional[str] = None,
            attachments: List[Optional[Attachment]] = None
    ):
        if all(not value for value in [text, attachments]):
            raise ValidationError('Either `text` or `attachments` required')

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
