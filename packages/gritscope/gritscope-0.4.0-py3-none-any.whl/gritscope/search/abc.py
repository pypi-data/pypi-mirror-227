from __future__ import annotations # Default behavior pending PEP 649

from abc import ABC, abstractmethod

from gritscope.topology.coords import TopoCoords

class Metric(ABC):

    @abstractmethod
    def __call__(self, topo: TopoCoords) -> float: ...
