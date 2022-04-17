import queue
from constants import *


def is_movable(board, hex_place):
    return True


def is_crawlable(board, hex_place):
    def f(neighbor):
        common_neighbors = set(board.get_neighbors(hex_place)).intersection(board.get_neighbors(neighbor))
        return len(common_neighbors) == 2 and common_neighbors.pop().isEmpty() ^ common_neighbors.pop().isEmpty()
    return f


def is_connected(board):
    def f(place):
        for n in board.get_neighbors(place):
            if n.isNotEmpty():
                return True
        return False
    return f


def queen_moves(board, hex_place):
    if not is_movable(board, hex_place):
        return []
    
    empty_neighbors = board.get_empty_neighbors(hex_place)
    return list(filter(is_crawlable(board, hex_place), empty_neighbors))


def ant_moves(board, hex_place, pop=False):
    if not is_movable(board, hex_place):
        return []

    piece = None
    if pop:
        piece = hex_place.pop_top_piece()

    result_set = set()
    processed = set()
    to_be_processed = queue.SimpleQueue()
    to_be_processed.put(hex_place)

    while not to_be_processed.empty():
        place = to_be_processed.get_nowait()
        filtered = list(
            filter(lambda n: is_crawlable(board, place)(n) and n != hex_place, board.get_empty_neighbors(place))
        )
        result_set.update(filtered)
        processed.add(place)

        for f in filtered:
            if not (f in processed):
                to_be_processed.put_nowait(f)

    if pop:
        hex_place.top_piece = piece
    return list(result_set)


def cockroach_moves(board, hex_place):
    if not is_movable(board, hex_place):
        return []

    return list(filter(is_connected(board), board.get_neighbors(hex_place)))


def grasshopper_moves(board, hex_place):
    if not is_movable(board, hex_place):
        return []

    directions = [
        lambda n: board.pos_x_of(n),
        lambda n: board.pos_y_of(n),
        lambda n: board.pos_z_of(n),
        lambda n: board.neg_x_of(n),
        lambda n: board.neg_y_of(n),
        lambda n: board.neg_z_of(n),
    ]

    result = []

    for direction in directions:
        neighbor = direction(hex_place)
        while neighbor is not None and neighbor.isNotEmpty():
            neighbor = direction(neighbor)
        if neighbor is not None:
            result.append(neighbor)

    return result


def valid_moves_of(board, hex_place, piece_type):
    if piece_type == QUEEN:
        return queen_moves(board, hex_place)
    elif piece_type == ANT:
        return ant_moves(board, hex_place)
    elif piece_type == COCKROACH:
        return cockroach_moves(board, hex_place)
    elif piece_type == GRASSHOPPER:
        return grasshopper_moves(board, hex_place)
    else:
        return []
