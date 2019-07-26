===========
slackistics
===========

Package to send Statistics over a Slack Incoming Webhook


* Free software: MIT license
* Documentation: https://slackistics.readthedocs.io.


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
            data={
                'labels': ['Alpha', 'Omega'],
                 'values': [22, 55]
             }
        )

    message = Message(
        text="I want to show you some *magic* :sparkles:",
        attachments=[attachment, chart]
    )
    client.send_message(message)

