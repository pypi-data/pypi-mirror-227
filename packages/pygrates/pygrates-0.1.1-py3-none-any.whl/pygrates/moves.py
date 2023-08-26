from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Callable, Iterable, Iterator, Generator
from typing import TypeVar, Optional

from .abc import GCoords, DGCoords
from .itertools import chainmap, unique

# Coordinate types

GC = TypeVar('GC', bound=GCoords)
DGC = TypeVar('DGC', bound=DGCoords)

# Passable function types

Guard = Callable[[GC], bool]
Direction = Callable[[GC, Optional[Guard[GC]]], Iterable[GC]]

# Main library functions

def adjacent(coords: GC,
             guard: Optional[Guard[GC]] = None) -> Iterator[GC]:
    """Iterate adjacent coordinates."""
    
    return filter(guard, coords.adjacent())

def children(coords: DGC,
             guard: Optional[Guard[DGC]] = None) -> Iterator[DGC]:
    """Iterate children."""
    
    return filter(guard, coords.children())

def parents(coords: DGC,
            guard: Optional[Guard[DGC]] = None) -> Iterator[DGC]:
    """Iterate parents."""
    
    return filter(guard, coords.parents())

def neighborhood(coords: GC, 
                 depth: int = 1,
                 guard: Optional[Guard[GC]] = None) -> Iterable[GC]:
    """Iterate neighboring coordinates to given depth."""
    
    return explore(coords, adjacent, depth, guard)

def descendants(coords: DGC, 
                depth: int = 1,
                guard: Optional[Guard[DGC]] = None) -> Iterator[DGC]:
    """Iterate parents to given depth."""
    
    return explore(coords, children, depth, guard)

def ancestors(coords: DGC, 
              depth: int = 1,
              guard: Optional[Guard[DGC]] = None) -> Iterator[DGC]:
    """Iterate descendants to given depth."""
    
    return explore(coords, parents, depth, guard)

def explore(coords: GC,
            direction: Direction[GC],
            depth: int = 1,
            guard: Optional[Guard[GC]] = None) -> Generator[GC, None, None]:
    """Iterate neighboring coordinates in given direction."""
    
    step = lambda c: direction(c, guard)
    
    seen: set[GC] = {coords}
    queue: set[GC] = {coords}
    
    for d in range(depth):
        seen = seen | queue
        queue = yield from unique(chainmap(step, queue), seen)
