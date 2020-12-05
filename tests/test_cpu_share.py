# pylint: disable=all
import unittest
from app.cpu_share import share, shortest_list, get_cpus


class TestCPUShare(unittest.TestCase):

    def test_shortest_list(self):
        lists = [[1], [1, 2], [3], [], [1, 3, 4]]
        x = shortest_list(lists)
        self.assertEqual(x, [])

    def test_share(self):
        """a list of objects is evenly distributed over an array of size os.cpu_count()"""
        iter_in = iter([i for i in range(300)])
        t = share(iter_in)

    def test_get_cpus(self):
        """get cpu's returns the count of all running server cpu's"""
        x = get_cpus()
        self.assertGreater(x, 0)


if __name__ == '__main__':
    unittest.main()
