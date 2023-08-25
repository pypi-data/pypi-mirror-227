import contextlib
import threading
from dataclasses import dataclass
from typing import Callable, Dict
import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


locks: Dict[str, "WLock"] = {}
locks_lock = threading.Lock()


@dataclass
class WLock:
    lock: threading.Lock
    waiters: int


@contextlib.contextmanager
def get_lock(id, is_obsolete: Callable = None):
    """
    A context manager for acquiring and releasing a lock associated with a given ID.

    Parameters:
    - id (str): The unique identifier for the lock.
    - is_obsolete (Callable): A callable function that determines if the lock should be considered obsolete.
      If provided, this function should take the lock ID as its argument and return True if the lock is obsolete,
      or False otherwise. If not provided, the lock will be deleted as soon as there are no more waiters.

    Usage:
    - Use this context manager to safely acquire and release locks for specific operations.
    - The lock is associated with a unique ID, and you can use the same ID across multiple sections of code
      to coordinate access to shared resources.
    - The `is_obsolete` function can be used to specify a custom condition for when the lock should be deleted.
      If not provided, the lock will be deleted as soon as there are no more waiters (threads waiting for the lock).
    """
    lock = None
    try:
        with locks_lock:
            lock = locks.setdefault(id, WLock(threading.Lock(), 0))
            lock.waiters += 1
        lock.lock.acquire()
        yield
    except KeyError:
        logger.warning(f"Lock id `{id}` is not available")
    except Exception:
        logger.exception(f"Unable to acquire or release lock for `{id}`")
    finally:
        if lock is not None:
            lock.lock.release()
            with locks_lock:
                lock.waiters -= 1
                if lock.waiters < 1 and (is_obsolete is None or is_obsolete(id)):
                    del locks[id]

    logger.debug(f"Current threading locks: {len(locks)}")
