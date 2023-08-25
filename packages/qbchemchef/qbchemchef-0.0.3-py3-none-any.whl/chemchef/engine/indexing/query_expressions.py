from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from chemchef.engine.indexing import FuzzyIndexCollection


class AbstractQueryExpression(ABC, BaseModel):

    def __and__(self, other: "AbstractQueryExpression") -> "AbstractQueryExpression":
        return And(left=self, right=other)

    def __or__(self, other: "AbstractQueryExpression") -> "AbstractQueryExpression":
        return Or(left=self, right=other)

    @abstractmethod
    def to_query(self) -> "AbstractQuery":
        raise NotImplementedError


class Exact(AbstractQueryExpression):
    field: str
    target: str

    def to_query(self) -> "AbstractQuery":
        return ExactQuery(self.field, self.target)


class Fuzzy(AbstractQueryExpression):
    field: str
    target: str
    max_candidates: int = 50

    # max_candidates = the maximum number of candidate matches to get from the vector DB
    # (These will then be post-filtered by the LLM)

    def to_query(self) -> "AbstractQuery":
        return FuzzyQuery(self.field, self.target, self.max_candidates)


class And(AbstractQueryExpression):
    left: AbstractQueryExpression
    right: AbstractQueryExpression

    def to_query(self) -> "AbstractQuery":
        return AndQuery(self.left.to_query(), self.right.to_query())


class Or(AbstractQueryExpression):
    left: AbstractQueryExpression
    right: AbstractQueryExpression

    def to_query(self) -> "AbstractQuery":
        return OrQuery(self.left.to_query(), self.right.to_query())


class AbstractQuery:

    @abstractmethod
    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        """
        Runs query.
        :return: Set of document ids returned by query
        """
        raise NotImplementedError


class ExactQuery(AbstractQuery):

    def __init__(self, field: str, target: str) -> None:
        self._field = field
        self._target = target

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        return indexes.exact_query(self._field, self._target)


class FuzzyQuery(AbstractQuery):

    def __init__(self, field: str, target: str, max_candidates: int) -> None:
        self._field = field
        self._target = target
        self._max_candidates = max_candidates

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        return indexes.fuzzy_query(self._field, self._target, self._max_candidates)


class AndQuery(AbstractQuery):

    def __init__(self, left_query: AbstractQuery, right_query: AbstractQuery):
        self._left_query = left_query
        self._right_query = right_query

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        left_results = self._left_query.run(indexes)
        right_results = self._right_query.run(indexes)
        return left_results.intersection(right_results)


class OrQuery(AbstractQuery):

    def __init__(self, left_query: AbstractQuery, right_query: AbstractQuery):
        self._left_query = left_query
        self._right_query = right_query

    def run(self, indexes: FuzzyIndexCollection) -> set[int]:
        left_results = self._left_query.run(indexes)
        right_results = self._right_query.run(indexes)
        return left_results.union(right_results)
