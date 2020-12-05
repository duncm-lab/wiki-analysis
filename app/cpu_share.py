"""split a 1 dimension array and share the values over an
array of dimension os.cpu_count()"""
from app.client import connect_servers


def get_cpus():
    """
    Get the number of cpu's available across all available servers
    :return: total number of cpu's
    :rtype: int
    :raises ValueError: No CPU's found
    """
    cpus = sum([int(str(i.cpu_count())) for i in connect_servers()])
    if cpus == 0:
        raise ValueError('No cpu\'s available - check servers are running')
    return cpus


def shortest_list(lists):
    """
    Get the shortest list from a list of lists
    :param lists: A list of lists
    :type lists: list of lists
    :return: The list with the smallest number of elements
    :rtype: list
    """

    f = list(map(len, lists))
    g = min(f)
    idx = f.index(g)
    return lists[idx]


def share(iter_in):
    """
    share an iterable of values evenly between the number of cpu's
    For example:

    >>> x = iter([0, 1, 2, 3, 4, 5, 6, 7])
    >>> y = 4
    >>> share(x, y)
    [[0, 1], [2, 3], [4, 5], [6, 7]]

    :param iter_in: The iterable to divide
    :type iter_in: iter
    :return: Initial input distributed over the count of cpus
    :rtype: list
    """
    cpu_array = [[] for i in range(get_cpus())]  # pylint: disable=unused-variable

    def lowest(c):  # gets list index of list with lowest count
        """

        :param c: list of lists
        :type c: list[list]
        :return: List with lowest number of elements
        :rtype: int
        """
        f = [len(i) for i in c]
        ix = f.index(min(f))
        return ix

    try:
        while True:
            val = next(iter_in)
            cpu_array[lowest(cpu_array)].append(val)
    except StopIteration:
        pass

    return cpu_array

#  python's horrible recursion limit :-(
# def share(iter_in: iter, cpu_share: List = None) -> List:
#     """
#     Take an iterable of length N and evenly divide it's items over
#     an list of os.cpu_count() lists
#     :param iter_in: Iterable
#     :param cpu_share: used recursively
#     :return:
#     """
#     if cpu_share is None:
#         cpu_share = [[] for i in range(os.cpu_count())]
#
#     try:
#         val = next(iter_in)
#         s = shortest_list(cpu_share)
#         s.append(val)
#
#     except StopIteration:
#         return cpu_share
#
#     return share(iter_in, cpu_share)
