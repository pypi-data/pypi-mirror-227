"""Runs example strategy"""

from tradeboy.engines.future import FutureEngine
from strategies.example import Strategy as ex_strat

engine = FutureEngine(Strategy=ex_strat, rate=30, verbose=True)
engine.run(trades=100)
