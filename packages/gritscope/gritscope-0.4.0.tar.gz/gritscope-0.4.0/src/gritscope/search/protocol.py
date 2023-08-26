from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Collection

from typing import Protocol

from gritscope.topology.coords import TopoCoords

class Metric(Protocol):
    
    name: str
    
    def __call__(self, topo: TopoCoords) -> float: ...

class MetricBatch(Protocol):
    
    metrics: Collection[Metric]
