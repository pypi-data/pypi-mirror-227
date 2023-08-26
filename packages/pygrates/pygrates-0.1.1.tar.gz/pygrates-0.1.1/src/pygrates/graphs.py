from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Mapping, Collection, Set, Callable
from typing import TypeVar

# Functions for operating on adjacency maps

A = TypeVar('A', bound=Hashable)
B = TypeVar('B', bound=Hashable)
C = TypeVar('C', bound=Hashable)
D = TypeVar('D', bound=Hashable)

def inverse(a: Mapping[A, Collection[B]]) -> dict[B, set[A]]:
    """Return inverse of adjacency map."""
    
    inv: dict[B, set[A]] = {}
    
    for f, ts in a.items():
        for t in ts:
            inv.setdefault(t, set()).add(f)
            
    return inv

def compound(a: Mapping[A, Collection[B]],
             b: Mapping[B, Collection[C]]) -> dict[A, set[C]]:
    """Return linked adjacency map from two adjacency maps."""
    
    comp: dict[A, set[C]] = {}
    
    for f, ts in a.items():
        for t in ts:
            comp.setdefault(f, set()).update(set(b.get(t, [])).difference([f]))
    
    return comp

def merge(a: Mapping[A, Collection[C]],
          b: Mapping[B, Collection[D]],
          left: bool = False) -> dict[A | B, set[C | D]]:
    """Return merged adjacency map from two adjacency maps."""
    
    mer: dict[A | B, set[C | D]] = {f: set(ts) for f, ts in a.items()}
    
    for f, ts in b.items():
        if left:
            mer.get(f, set()).update(ts)
        else:
            mer.setdefault(f, set()).update(ts)
    
    return mer

def degrees(a: Mapping[A, Collection[B]]) -> dict[A, int]:
    """Return degree map of adjacency map."""
    
    degs: dict[A, int]
    
    return {f: len(ts) for f, ts in a.items()}

def subsources(a: Mapping[A, Collection[B]],
               condition: Callable[[A], bool]) -> dict[A, set[B]]:
    """Return adjacency map with sources filtered by condition."""
    
    return {f: set(ts) for f, ts in a.items() if condition(f)}

def subsinks(a: Mapping[A, Collection[B]],
             condition: Callable[[B], bool]) -> dict[A, set[B]]:
    """Return adjacency map with sinks filtered by condition."""
    
    return {f: set(filter(condition, ts)) for f, ts in a.items()
            if len(tuple(filter(condition, ts))) != 0}

def subgraph(a: Mapping[A, Collection[B]],
             condition: Callable[[A | B], bool]) -> dict[A, set[B]]:
    """Return adjacency map with all objects filtered by condition."""
    
    return subsinks(subsources(a, condition), condition)
