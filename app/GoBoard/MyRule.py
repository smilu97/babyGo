import numpy as np

captured_weight = 2


def get_score(board):

    next_cluster_num = 1

    cluster_num = np.zeros(board.board_size, dtype=np.int)  # contain cluster number of blank

    for x in range(board.board_size[0]):
        for y in range(board.board_size[1]):
            if cluster_blank(x, y, next_cluster_num, cluster_num, board):
                next_cluster_num += 1

    cluster_type = [[False, False] for _ in range(next_cluster_num)]
    cluster_size = [0 for _ in range(next_cluster_num)]

    for x in range(board.board_size[0]):
        for y in range(board.board_size[1]):
            current_cluster = cluster_num[x, y]
            if current_cluster == 0:
                continue

            cluster_size[current_cluster] += 1

            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                nx, ny = x + offset[0], y + offset[1]
                if 0 <= nx < board.board_size[0] and 0 <= ny < board.board_size[1]:
                    if board.board[nx, ny] == 1:
                        cluster_type[current_cluster][0] = True
                    elif board.board[nx, ny] == -1:
                        cluster_type[current_cluster][1] = True

    white_score, black_score = board.captured['white'] * captured_weight, board.captured['black'] * captured_weight

    for current_cluster in range(1, next_cluster_num):
        current_type = cluster_type[current_cluster]
        if current_type[0] == 1 and current_type[1] == 0:
            white_score += cluster_size[current_cluster]
        elif current_type[0] == 0 and current_type[1] == 1:
            black_score += cluster_size[current_cluster]

    return (white_score, black_score), cluster_num, cluster_type, cluster_size


def cluster_blank(x, y, num, cluster_num, board):

    if board.board[x, y] != 0:
        return False

    if cluster_num[x, y] != 0:
        return False

    cluster_num[x, y] = num

    offsets = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for offset in offsets:
        nx, ny = x + offset[0], y + offset[1]
        if 0 <= nx < cluster_num.shape[0] and 0 <= ny < cluster_num.shape[1]:
            cluster_blank(nx, ny, num, cluster_num, board)

    return True
