import logging
from functools import wraps

from dzy.timer import RecurringTimer

log = logging.getLogger(__name__)


def with_keepalives(*, interval: float = 10):
    timer = RecurringTimer(
        interval=interval,
        function=log.info,
        args=("still alive", ),
    )

    def factory(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            try:
                timer.start()
                return fn(*a, **kw)
            finally:
                timer.cancel()
                timer.join()
        return wrapper
    return factory
