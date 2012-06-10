from .base import C, Constant, Buffer, Tap, If, Eval, Tempo
from .player import play, countdown
from . import midi, math, waves, util

try:
    import zmq
    from . import zmq
except ImportError:
    pass
