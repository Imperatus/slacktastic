from slacktastic.client import SlackClient
from slacktastic.template import Message, PieChart

client = SlackClient(
    webhook_url='https://hooks.slack.com/services/'
                'TBWAF1BH7/BLTGSMRNK/40X6YJP7czgUX4OgSfGvFlUR')


test = PieChart(
    "Test data", {
        'labels': ['Ride', 'Reservation'],
        'values': [22, 55]})

message = Message(text='This is a *test*', attachments=[test])
client.send_message(message)
