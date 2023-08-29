from fake_useragent import UserAgent
from requests import Session


def create_session() -> Session:
    """
    Creates a session with a random User-Agent header.

    Returns:
        Session: The created session with the User-Agent header set.
    """
    session: Session = Session()
    ua: UserAgent = UserAgent()
    session.headers.update({
        'User-Agent': ua.random
    })
    return session
