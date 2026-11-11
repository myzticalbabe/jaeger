# coding: utf-8
"""krampus-jaeger: durable spans for routed delegations, stdlib only."""

from .spans import SpanStore, VERDICTS, build_span, timed

__version__ = "0.1.0"

__all__ = ["SpanStore", "VERDICTS", "build_span", "timed",
           "__version__"]
