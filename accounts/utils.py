import logging

logger = logging.getLogger(__name__)
syslog = logging.FileHandler(filename='./logs/ipAddressUsers.log')
formatter = logging.Formatter('Timestamp: %(asctime)s | %(message)s : %(ip_address)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ip_logger(extra, username):
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra)
    logger.info(username)
