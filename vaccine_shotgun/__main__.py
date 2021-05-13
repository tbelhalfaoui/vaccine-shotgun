import argparse
import json
import random
import time
import logging

from datetime import datetime
import requests
import smtplib
from email.message import EmailMessage

import daiquiri
from tqdm import tqdm

daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger("shotgun")


with open('config.json') as f:
    CONFIG = json.load(f)


def list_urls_from_txt(urls_file):
    with open(urls_file) as f:
        for url in f:
            url = url.strip()
            if url:
                yield url


def get_availabilities(urls, min_wait_time, max_wait_time):
    random.shuffle(urls)
    for url in tqdm(urls):
        result = requests.get(url)
        result.raise_for_status()
        result_dict = result.json()
        if result_dict['total']:
            yield url, result_dict
        time.sleep(random.uniform(min_wait_time, max_wait_time))


def send_notification(subject, body):
    message = EmailMessage()
    message['From'] = CONFIG['sender']
    message['To'] = CONFIG['receiver']
    message['Subject'] = subject
    message.set_content(body)

    session = smtplib.SMTP(CONFIG['server'], int(CONFIG['port']))
    session.starttls()
    session.login(CONFIG['login'], CONFIG['password'])
    text = message.as_string()
    session.sendmail(message['From'], message['To'], text)
    session.quit()


def build_message(result_dict):

    dates = []
    for avail in result_dict['availabilities']:
        for slot in avail['slots']:
            date = datetime.fromisoformat(slot['start_date']).strftime('%A %d %B %Y - %H:%M')
            dates.append(date)

    subject = f'[{dates[0]}] {result_dict["total"]} slot(s) at {result_dict["search_result"]["last_name"]}'

    body = f"""
    {result_dict['search_result']['last_name']}
    https://doctolib.fr{result_dict['search_result']['url']}
    
    {result_dict['search_result']['address']}
    {result_dict['search_result']['zipcode']} - {result_dict['search_result']['city']}
    {result_dict['search_result']['visit_motive_name']}

    """ + "\n".join(dates)
    return subject, body


def test_notification(example_response_file):
    with open(example_response_file) as f:
        result_dict = json.load(f)
    title, body = build_message(result_dict)
    send_notification(title, body)
    print(title)
    print(body)
    logger.info(f'Notification sent to {CONFIG["receiver"]}')


def main(min_wait_time, max_wait_time, urls_file):
    urls = list(list_urls_from_txt(urls_file))

    while True:
        for url, result_dict in get_availabilities(urls, min_wait_time, max_wait_time):
            title, body = build_message(result_dict)
            logger.warning(body)
            send_notification(title, body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action='store_true', help="Send a fake test notification.")
    args = parser.parse_args()
    if args.test:
        test_notification('example_response.json')
    else:
        main(min_wait_time=0, max_wait_time=5, urls_file='urls.txt')
