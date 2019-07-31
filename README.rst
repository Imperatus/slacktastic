===========
slackistics
===========

Package to send Statistics over a Slack Incoming Webhook


* Free software: MIT license


Features
--------

* Send messages via Slack Incoming Webhook
* Provides object-based templates for Messages, Attachments and Fields
* Fine-grained control over Message formatting, and supports mrkdwn
* Easily generate various charts based on your data. Supported types are:
    * Bar Chart
    * Line Chart
    * Radar Chart
    * Pie Chart
    * Donut Chart


Roadmap
-------

* Implement tests
* Add extensive documentation
* Add support for more chart types
* Add templates for most commonly sent messages
* Extend customizability to override webhook settings


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

This package makes use of the Quickchart.io_ to draw diagrams.

.. _Quickchart.io: https://quickchart.io


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

    # You can now pass custom ChartJS options for all diagrams! See ChartJS docs
    chart.set_options({
        title: {
        display: true,
        text: 'Cool title',
        fontColor: 'hotpink',  # For testing purposes only...
        fontSize: 32,
    })

    another_chart = BarChart(
            "Test data", labels=['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            data={
                'Test 1': [1, 2, 4, 8, 16],
                'Test 2': [7, 3, 45, 1, 12],
            }
    )

    # Customise the background colors of your data if you don't like our scheme
    another_chart.set_background_colors([
        "#000", "#3333", "#666", "#999", "#CCC"
    ])

    message = Message(
        text="I want to show you some *magic* :sparkles:",
        attachments=[attachment, chart]
    )
    client.send_message(message)
