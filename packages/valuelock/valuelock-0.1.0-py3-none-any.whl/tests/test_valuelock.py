import unittest
import concurrent.futures
import random
import time
from valuelock import get_lock
from valuelock.valuelock import locks


class TestValueLock(unittest.TestCase):
    def test_concurrent_access(self):
        lock_id = "test"
        num_threads = 5

        # A shared resource protected by the lock
        resource_result = []
        resource2_result = []
        resource_expected = [0, 1, 2, 3, 4]

        def access_protected_resource(thread_id):
            with get_lock(lock_id):
                # Simulate some work that needs to be protected by the lock
                # Introduce random sleep periods to create contention
                sleep_time = random.uniform(
                    0.1, 0.5
                )  # Random sleep between 0.1 to 0.5 seconds
                time.sleep(sleep_time)
                resource_result.append(thread_id)
                resource2_result.append(thread_id)

        def access_protected_resource2():
            with get_lock("whatever"):
                resource2_result.append(99)

        # Create a thread pool to run multiple workers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit the worker functions to the thread pool
            futures = [
                executor.submit(access_protected_resource, i)
                for i in range(num_threads)
            ]
            futures.append(executor.submit(access_protected_resource2))

            # Wait for all workers to complete
            concurrent.futures.wait(futures)

        # Assert that the shared resource was accessed by only one thread at a time
        self.assertEqual(resource_result, resource_expected)
        self.assertNotEqual(resource2_result[-1], 10)

    def test_is_obsolete_callback(self):
        def is_obsolete(id):
            return False

        num_threads = 5
        lock_id1 = "test"

        def task1():
            with get_lock(lock_id1):
                pass

        def task2():
            time.sleep(1)  # Sleep to ensure task2 starts after task1
            with get_lock(lock_id1, is_obsolete):
                pass

        # Create a thread pool to run multiple workers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit the worker functions to the thread pool
            futures = [executor.submit(task) for task in [task1, task2]]

            # Wait for all workers to complete
            concurrent.futures.wait(futures)

        self.assertEqual(len(locks), 1)


if __name__ == "__main__":
    unittest.main()
