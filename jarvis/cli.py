#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    jarvis.cli
    ~~~~~~~~~~~~

    This module is the main of jarvis.

    :copyright: (c) 2017 by Ma Fei.
"""
import logging
import os
import signal
import time

import click
from slackclient import SlackClient

import jarvis

logger = logging.getLogger(__name__)

# jarvis's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def output_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: {}".format(jarvis.__version__))
    ctx.exit()


def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "<!here> Sure...write some more code then I can do that!"
    if "rules" in command:
        response = """
>A robot may not injure a human being or, through inaction, allow a human being to come to harm.
>A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.
>A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws.
"""
    if "create" in command:
        response = "<@fei.ma03> is my creator"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def eating():
    channel_name = 'C5QKM4F3R'
    response = "<!here> let's go to eating!"
    slack_client.api_call("chat.postMessage", channel=channel_name,
                          text=response, as_user=True)


def chat():
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


@click.command()
@click.option(
    '-v',
    '--version',
    is_flag=True,
    is_eager=True,
    callback=output_version,
    expose_value=False,
    help="show the version of this tool")
@click.option(
    '-l',
    '--log',
    default='INFO',
    help='Specify logging level, default is INFO')
def parse_command(log):
    log_level = getattr(logging, log.upper())
    logging.basicConfig(level=log_level)
    chat()


def signal_handler(signum, frame):
    logger.info("main process(%d) got GracefulExitException" % os.getpid())
    os._exit(0)


def main():
    print("Jarvis is providing services")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    parse_command()


if __name__ == "__main__":
    main()
