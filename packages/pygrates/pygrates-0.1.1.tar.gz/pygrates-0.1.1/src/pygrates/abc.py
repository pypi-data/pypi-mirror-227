from __future__ import annotations # Default behavior pending PEP 649

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Self

from itertools import chain

# Base coordinate classes to implement for using the library functions

class GCoords(ABC):
    """Base class for implicit definition of a graph."""
    
    __slots__ = ()
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        
        raise NotImplementedError
    
    @abstractmethod
    def __hash__(self) -> int:
        
        raise NotImplementedError
    
    @abstractmethod
    def adjacent(self) -> Iterable[Self]:
        """Return iterable containing adjacent coordinates."""
        
        raise NotImplementedError
    
    def is_adjacent(self, other: Self) -> bool:
        """Return True if self is a parent of other."""
        
        adjacent: Iterable[Self] = self.adjacent()
        return any(coords == other for coords in adjacent)

class DGCoords(GCoords, ABC):
    """Base class for implicit definition of a directed graph."""
    
    __slots__ = ()
    
    @abstractmethod
    def children(self) -> Iterable[Self]:
        """Return iterable containing children."""
        
        raise NotImplementedError
    
    @abstractmethod
    def parents(self) -> Iterable[Self]:
        """Return iterable containing parents."""
        
        raise NotImplementedError
    
    def adjacent(self) -> Iterable[Self]:
        """Return iterable containing adjacent coordinates."""
        
        return chain(self.children(), self.parents())
    
    def is_child(self, other: Self) -> bool:
        """Return True if self is a child of other."""
        
        parents: Iterable[Self] = self.parents()
        return any(coords == other for coords in parents)
    
    def is_parent(self, other: Self) -> bool:
        """Return True if self is a parent of other."""
        
        children: Iterable[Self] = self.children()
        return any(coords == other for coords in children)

class DAGCoords(DGCoords, ABC):
    """Base class for implicit definition of a directed acyclic graph."""
    
    __slots__ = ()

class TGCoords(DAGCoords, ABC):
    """Base class for implicit definition of a tree graph."""
    
    __slots__ = ()
