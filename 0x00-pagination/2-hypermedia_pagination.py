#!/usr/bin/env python3
"""
mplement a method named get_page that takes two integer
 arguments page with default value 1 and page_size with
 default value 10.
"""
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int]:
    """ Returns a tuple """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return the appropriate page of the dataset.
        If the input arguments are out of range for the dataset,
        an empty list should be returned.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        data_set = self.dataset()

        if start_index >= len(data_set):
            return []

        end_index = min(end_index, len(data_set))

        return data_set[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """returns a dictionary containing the following key-value pairs:

        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer
        """
        data = self.get_page(page, page_size)
        data_set = self.dataset()
        prev_page = page - 1 if page > 1 else None
        total_page = math.ceil(len(data_set) / page_size)
        next_page = page + 1 if page < total_page else None
        page_size_actual = len(data)
        return {
            'page_size': page_size_actual,
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_page': total_page
        }
