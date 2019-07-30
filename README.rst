===========
slackistics
===========

Package to send Statistics over a Slack Incoming Webhook


* Free software: MIT license


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Usage
-----
.. code-block:: python

    from slacktastic.client import SlackClient
    from slacktastic.template import Attachment, PieChart, Message

    client = SlackClient(webhook_url='YOUR WEBHOOK URL')
    attachment = Attachment(
        title='Cool block title',
        title_link='https://labela.nl',
        text='Some awesome text')

    chart = PieChart(
            title="Test data",
            labels=['Ride', 'Reservation'],
            values=[22, 55]
        )

    another_chart = BarChart(
            "Test data", labels=['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            data={
                'Test 1': [1, 2, 4, 8, 16],
                'Test 2': [7, 3, 45, 1, 12],
            }
    )

    message = Message(
        text="I want to show you some *magic* :sparkles:",
        attachments=[attachment, chart]
    )
    client.send_message(message)

