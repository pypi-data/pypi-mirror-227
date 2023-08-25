"""
A module that implements various sorting algorithms.

Each function in this module is an implementation of a specific sorting algorithm.
All functions accept an input array of integers. The time and space complexity of each
algorithm is specified in its respective function's documentation.

This module is designed primarily for educational purposes. It allows for the understanding
and learning of various types of sorting algorithms and their Python implementations.
"""

from itertools import chain, repeat


def insert_sort(array: list[int]) -> None:
    """
    Sort an array of integers using the insertion sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    :param array: array of integers
    :return: None
    """
    for i in range(1, len(array)):
        current = array[i]
        j = i
        while j > 0 and array[j - 1] > current:
            array[j] = array[j - 1]
            j -= 1
        array[j] = current


def _merge(array_one: list[int], array_two: list[int]) -> list[int]:
    result = []

    i = j = 0
    while i < len(array_one) and j < len(array_two):
        if array_one[i] < array_two[j]:
            result.append(array_one[i])
            i += 1
        else:
            result.append(array_two[j])
            j += 1

    result.extend(array_one[i:])
    result.extend(array_two[j:])
    return result


def merge_sort(array: list[int]) -> list[int]:
    """
    Sorts an array of integers using the merge sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(n), where n is the length of the array.

    :param array: array of integers
    :return: sorted array of integers
    """
    length = len(array)
    if length <= 1:
        return array

    mid = length // 2
    left_array = array[:mid]
    right_array = array[mid:]

    left_array_sorted = merge_sort(left_array)
    right_array_sorted = merge_sort(right_array)

    return _merge(left_array_sorted, right_array_sorted)


def quick_sort(array: list[int], left: int, right: int) -> None:
    """
    Sorts an array of integers using the quick sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1)

    :param array: array of integers
    :param left: left index (inclusive)
    :param right: right index (inclusive)
    :return: None
    """
    if left < right:
        mid = _partition(array, left, right)
        quick_sort(array, left, mid - 1)
        quick_sort(array, mid + 1, right)


def _partition(array: list[int], left: int, right: int) -> int:
    pivot = array[right]
    pivot_index = left - 1
    for i in range(left, right):
        if array[i] <= pivot:
            pivot_index += 1
            array[pivot_index], array[i] = array[i], array[pivot_index]

    array[pivot_index + 1], array[right] = array[right], array[pivot_index + 1]
    return pivot_index + 1


def heap_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the heap sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1).

    :param array: array of integers
    :return: None
    """
    _build_heap(array)

    for index in reversed(range(len(array))):
        array[index], array[0] = array[0], array[index]
        _heapify(array, index, 0)


def _left_child(index: int) -> int:
    return 2 * index + 1


def _right_child(index: int) -> int:
    return 2 * index + 2


def _heapify(array: list[int], size: int, index: int) -> None:
    largest = index
    if _left_child(index) < size and array[_left_child(index)] > array[largest]:
        largest = _left_child(index)
    if _right_child(index) < size and array[_right_child(index)] > array[largest]:
        largest = _right_child(index)
    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        _heapify(array, size, largest)


def _build_heap(array: list[int]) -> None:
    for i in reversed(range(len(array) // 2)):
        _heapify(array, len(array), i)


def counting_sort(array: list[int], max_value: int) -> list[int]:
    """
    Sorts an array of integers using the counting sort algorithm.

    Time complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    The function assumes that the array contains non-negative integers.

    :param array: array of integers
    :param max_value: maximum value in the array
    :return: sorted array of integers
    """
    count_of_each_integer = list(repeat(0, max_value + 1))
    for num in array:
        count_of_each_integer[num] += 1

    for i in range(1, max_value + 1):
        count_of_each_integer[i] += count_of_each_integer[i - 1]

    result = list(repeat(0, len(array)))
    for num in reversed(array):
        count_of_each_integer[num] -= 1
        result[count_of_each_integer[num]] = num

    return result


def radix_sort(array: list[int], max_digits: int, base: int = 10) -> list[int]:
    """
    Sorts an array of integers using the radix sort algorithm.

    Time complexity: O(d*(n+k)), where:
     - d is the number of digits in the largest number
     - n is the length of the array
     - k is the number of possible digits (the base)

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the number of possible digits (the base)

    The function assumes that the array contains non-negative integers.

    :param array: array of integers
    :param max_digits: number of digits in the largest number
    :param base: base of the numbers, default is 10
    :return: sorted array of integers
    """
    for i in range(max_digits):
        bins: list[list[int]] = [[] for _ in range(base)]
        for num in array:
            digit = (num // base**i) % base
            bins[digit].append(num)

        array = list(chain.from_iterable(bins))

    return array
