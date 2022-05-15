import queue
from constants import *


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
    empty_neighbors = board.get_empty_neighbors(hex_place)
    return list(filter(is_crawlable(board, hex_place), empty_neighbors))


def ant_moves(board, hex_place):
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

    return list(result_set)


def cockroach_moves(board, hex_place):
    result = []
    crawlable = is_crawlable(board, hex_place)
    for neighbor in board.get_neighbors(hex_place):
        if neighbor.isNotEmpty() or crawlable(neighbor):
            result.append(neighbor)
    return result


def grasshopper_moves(board, hex_place):
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
        i = 0
        while neighbor is not None and neighbor.isNotEmpty():
            neighbor = direction(neighbor)
            i += 1
        if neighbor is not None and i > 0:
            result.append(neighbor)

    return result


def spider_moves(board, hex_place):
    empty_neighbors = board.get_empty_neighbors(hex_place)
    set1 = set(filter(is_crawlable(board, hex_place), empty_neighbors))

    set2 = set()
    for place in set1:
        place_empty_neighbors = board.get_empty_neighbors(place)
        set2.update(filter(lambda n: is_crawlable(board, place)(n) and n != hex_place and (n not in set1),
                           place_empty_neighbors))

    set3 = set()
    for place in set2:
        place_empty_neighbors = board.get_empty_neighbors(place)
        set3.update(
            filter(lambda n: is_crawlable(board, place)(n) and n != hex_place and (n not in set1) and (n not in set2),
                   place_empty_neighbors))

    return list(set3)


def valid_moves_of(board, hex_place, piece_type, should_pop):
    piece = hex_place.pop_top_piece() if should_pop else None
    result = None

    if not is_movable(board, hex_place):
        if should_pop:
            hex_place.top_piece = piece
        return []

    if piece_type == QUEEN:
        result = queen_moves(board, hex_place)
    elif piece_type == ANT:
        result = ant_moves(board, hex_place)
    elif piece_type == COCKROACH:
        result = cockroach_moves(board, hex_place)
    elif piece_type == GRASSHOPPER:
        result = grasshopper_moves(board, hex_place)
    elif piece_type == SPIDER:
        result = spider_moves(board, hex_place)
    else:
        result = []

    if should_pop:
        hex_place.top_piece = piece

    return result


def have_path(board, source, destination):
    stack = [source]
    checked = set()

    while len(stack) > 0:
        node = stack.pop()
        children = board.get_full_neighbors(node)
        for child in children:
            if child == destination:
                return True
            elif child not in checked:
                stack.append(child)

        checked.add(node)
    return False


def is_movable(board, hex_place):
    pos_x, neg_x = board.pos_x_of(hex_place), board.neg_x_of(hex_place)
    pos_y, neg_y = board.pos_y_of(hex_place), board.neg_y_of(hex_place)
    pos_z, neg_z = board.pos_z_of(hex_place), board.neg_z_of(hex_place)

    directions = [
        [pos_x, neg_x, pos_z, neg_y],
        [pos_y, neg_x, neg_z, neg_y],
        [pos_z, neg_z, pos_x, neg_y],
    ]

    for direc in directions:
        is_ok = (direc[0] is None or direc[0].isEmpty()) or (
                (direc[1] is None or direc[1].isEmpty() or have_path(board, direc[0], direc[1])) and (
                direc[2] is None or direc[2].isEmpty() or have_path(board, direc[0], direc[2])) and (
                        direc[3] is None or direc[3].isEmpty() or have_path(board, direc[0], direc[3])))
        if not is_ok:
            return False

    return True


def can_accept_new_piece(board, hex_place, player_num):
    if hex_place.isNotEmpty():
        return False

    self_count = 0
    for neighbor in board.get_full_neighbors(hex_place):
        if neighbor.top_piece.player != player_num:
            return False
        self_count += 1
    return self_count > 0


def find_outer_edge(board, some_point_inside):
    if some_point_inside is None:
        return []

    edge_place = board(some_point_inside[0], 0)
    while edge_place.isEmpty():
        edge_place = board.pos_x_of(edge_place)

    edge_place = board.neg_x_of(edge_place)
    result = ant_moves(board, edge_place)
    result.append(edge_place)

    return result


def legal_actions_of(gs, player):
    result = []

    some_point_inside = None
    for onboard_piece in player.onboard_pieces():
        some_point_inside = onboard_piece.pos
        if not player.has_placed_queen():
            continue
        for move in valid_moves_of(gs.board, gs.board(*onboard_piece.pos), onboard_piece.type, should_pop=True):
            result.append((POP, onboard_piece.pos, move.pos))

    if gs.turn == 1:
        outer_edge = [gs.P1_FIRST_PLACE()]
    elif gs.turn == 2:
        outer_edge = [gs.P2_FIRST_PLACE()]
    else:
        outer_edge = find_outer_edge(gs.board, some_point_inside)
    for ondeck_piece_type, count in player.ondeck_pieces():
        if count == 0:
            continue
        if gs.has_to_enter_queen() and ondeck_piece_type != QUEEN:
            continue
        for edge_place in outer_edge:
            if 1 <= gs.turn <= 2 or can_accept_new_piece(gs.board, edge_place, player.num):
                result.append((NEW, ondeck_piece_type, edge_place.pos))

    return result
