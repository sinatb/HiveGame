import queue


def is_movable(board, hex_place):
    return True


def is_crawlable(board, hex_place):
    def f(neighbor):
        common_neighbors = set(board.get_neighbors(hex_place)).intersection(board.get_neighbors(neighbor))
        assert len(common_neighbors) == 2
        return common_neighbors.pop().isEmpty() ^ common_neighbors.pop().isEmpty()
    return f


def queen_moves(board, hex_place):
    if not is_movable(board, hex_place):
        return iter([])
    
    empty_neighbors = board.get_empty_neighbors(hex_place)
    return filter(is_crawlable(board, hex_place), empty_neighbors)


def ant_moves(board, hex_place):
    if not is_movable(board, hex_place):
        return iter([])

    result_set = set()
    processed = set()
    to_be_processed = queue.SimpleQueue()
    to_be_processed.put(hex_place)

    while not to_be_processed.empty():
        place = to_be_processed.get_nowait()
        filtered = filter(is_crawlable(board, place), board.get_empty_neighbors(place))
        result_set.update(filtered)
        processed.add(place)

        for f in filtered:
            if not (f in processed):
                to_be_processed.put_nowait(f)

    return iter(result_set)
