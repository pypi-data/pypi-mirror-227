import os
from collections import namedtuple

Setter = namedtuple('Setter', ['fnc', 'flds'])

VERBOSE = os.getenv('VERBOSE') in ('True', '1', 'true')

LANGUAGE = os.getenv('LANGUAGE', 'UA')
assert LANGUAGE, "Please fill the correct LANGUAGE variable"

COUNTRY = os.getenv('COUNTRY', 'UA')
assert COUNTRY, "Please fill the correct COUNTRY variable"

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
USER_AGENT = os.getenv('USER_AGENT', DEFAULT_USER_AGENT)
assert USER_AGENT, "Please fill the correct USER_AGENT variable"

DEFAULT_HEADERS = {
    'User-Agent': USER_AGENT,
}

DEFAULT_COOKIES = {
    'visitor_city': "1",
}

CALLS_MAX = int(os.getenv('CALLS_MAX', 10))
CALLS_PERIOD = int(os.getenv('CALLS_PERIOD', 1))

# GET_RETRIES = int(os.getenv('GET_RETRIES', 50))
# GET_DELAY = int(os.getenv('GET_DELAY', 30))
GET_TIMEOUT = int(os.getenv('GET_TIMEOUT', 60))


INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_USER_MENTIONS = os.getenv('SLACK_USER_MENTIONS', '')

TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
TEAMS_USER_MENTIONS = os.getenv('TEAMS_USER_MENTIONS', '')

MEASUREMENT = os.getenv('MEASUREMENT', 'goods')

DEFAULT_TAGS = [
    'id_',
]
TAGS = os.getenv('TAGS', DEFAULT_TAGS)
if isinstance(TAGS, str):
    TAGS = TAGS.split()

DEFAULT_FIELDS = [
    'price',
    'old_price',
    # 'stars',
    'discount',
    # 'comments_amount',
    # 'comments_mark',
]
FIELDS = os.getenv('FIELDS', DEFAULT_FIELDS)
if isinstance(FIELDS, str):
    FIELDS = FIELDS.split()
