from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats import endpoints
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def configure_nba_api():
    NBAStatsHTTP._NBAStatsHTTP__headers = {
        "Host": "stats.nba.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "x-nba-stats-origin": "stats",
        "x-nba-stats-token": "true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Origin": "https://www.nba.com",
        "Referer": "https://www.nba.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }

    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))

    timeout = 60
    session.timeout = timeout

    endpoints._session = session
