def parse_seq(seqstr, **kwargs):
    symbol_map = dict(kwargs)
    symbol_map['.'] = symbol_map.get('.', None)
    seq = []
    for symbol in seqstr:
        if symbol in symbol_map:
            seq.append(symbol_map[symbol])
    return seq
