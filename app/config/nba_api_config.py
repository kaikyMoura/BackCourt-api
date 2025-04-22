from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats import endpoints
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def configure_nba_api():
    """
    Configure the NBA API library to use a custom session with retry policy.

    This function configures the NBA API library to use a custom session with a
    retry policy. This allows the library to retry failed requests up to 5 times,
    with an exponential backoff between retries.

    The custom session is created using the requests library, with a retry policy
    that retries on the following status codes: 408, 429, 500, 502, 503, 504.

    The custom session is then mounted on the NBA API library, and the timeout
    for the session is set to 60 seconds. The timeout for the NBA API library
    is set to 70 seconds.

    Finally, the custom session is returned.

    Returns:
        requests.Session: The custom session with retry policy.
    """
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
        backoff_factor=1,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(
        max_retries=retries, pool_connections=20, pool_maxsize=20, pool_block=False
    )

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.timeout = 60
    NBAStatsHTTP.timeout = 70

    endpoints._session = session

    NBAStatsHTTP._NBAStatsHTTP__timeout = (7, 15)

    return session
