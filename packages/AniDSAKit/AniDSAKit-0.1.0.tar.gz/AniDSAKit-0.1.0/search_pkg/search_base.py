from abc import ABC, abstractmethod
from typing import List, Union

class SearchBase(ABC):
    """
    Abstract base class for search algorithms.

    This class defines an abstract search method that should be implemented
    by concrete search algorithm classes.

    Attributes:
        None
    """

    @abstractmethod
    def search(self, arr: List, target: Union[int, float, str]) -> Union[int, float, str]:
        """
        Perform a search for a target element in a list.

        Args:
            arr (List): The list to search within.
            target (Union[int, float, str]): The target element to search for.

        Returns:
            Union[int, float, str]: The result of the search. It can be an integer,
            float, or string depending on the search algorithm's logic.
        """
        pass
