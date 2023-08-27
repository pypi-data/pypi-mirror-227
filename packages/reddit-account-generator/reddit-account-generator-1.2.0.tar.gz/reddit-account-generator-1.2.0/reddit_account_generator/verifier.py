import logging

import requests
from tempmail import EMail

from .exceptions import EmailVerificationException

_logger = logging.getLogger(__name__)


def verify_email(email: str, proxies: dict[str, str] | None = None):
    _logger.info('Verifying reddit account email')

    # Get verification link
    link = get_verification_link(email)
    direct_link = get_direct_verification_link(link)

    _logger.debug('Verifying email')
    resp = requests.post(direct_link, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }, proxies=proxies)

    if resp.status_code != 200:
        if 'EMAIL_ALREADY_VERIFIED' not in resp.text:
            raise EmailVerificationException(resp.text)
        
        _logger.warning('Email is already verified')


def get_verification_link(email: str) -> str:
    try:
        email_ = EMail(email)
    except ValueError:
        raise ValueError('Verification of this email is not supported.')

    _logger.debug('Waiting for email...')
    msg = email_.wait_for_message(filter=lambda m: 'reddit' in m.subject.lower())

    # Get link
    start = msg.body.index('https://www.reddit.com/verification/')
    end = msg.body.index('"', start)
    link = msg.body[start:end]

    return link


def get_direct_verification_link(link: str) -> str:
    """Create a direct verification link from a verification link."""

    start = link.index('verification/') + len('verification/')
    end = link.index('?', start)
    token = link[start:end]

    start = link.index('correlation_id=') + len('correlation_id=')
    end = link.index('&', start)
    correlation_id = link[start:end]

    return f'https://www.reddit.com/api/v1/verify_email/{token}.json?correlation_id={correlation_id}&ref_campaign=verify_email'
