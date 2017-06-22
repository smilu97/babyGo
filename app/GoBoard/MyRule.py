import numpy as np

captured_weight = 2


def get_score(board):  # calculate score from board

    next_cluster_num = 1

    cluster_num = np.zeros(board.board_size, dtype=np.int)  # contain cluster number of blank

    for x in range(board.board_size[0]):
        for y in range(board.board_size[1]):
            if cluster_blank(x, y, next_cluster_num, cluster_num, board):  # cluster blanks
                next_cluster_num += 1

    # contain each clusters meeting with white or black stone
    cluster_type = [[False, False] for _ in range(next_cluster_num)]

    # contain the size of clusters
    cluster_size = [0 for _ in range(next_cluster_num)]

    # check cluster_size, cluster_type
    for x in range(board.board_size[0]):
        for y in range(board.board_size[1]):
            current_cluster = cluster_num[x, y]

            if current_cluster == 0:  # it's not blank. not included in any cluster
                continue

            cluster_size[current_cluster] += 1  # increase cluster size

            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]:  # check if meeting with stones
                nx, ny = x + offset[0], y + offset[1]
                if 0 <= nx < board.board_size[0] and 0 <= ny < board.board_size[1]:  # check if out of range
                    if board.board[nx, ny] == 1:  # if the stone is white
                        cluster_type[current_cluster][0] = True  # this cluster meet with white stone
                    elif board.board[nx, ny] == -1:  # if the stone is black
                        cluster_type[current_cluster][1] = True  # this cluster meet with black stone

    # initialize scores with the number of captured stone of opposite
    white_score, black_score = board.captured['black'] * captured_weight, board.captured['white'] * captured_weight

    for current_cluster in range(1, next_cluster_num):
        current_type = cluster_type[current_cluster]
        if current_type[0] == 1 and current_type[1] == 0:  # if this cluster only meets with white stones
            white_score += cluster_size[current_cluster]  # the white has this territory as score
        elif current_type[0] == 0 and current_type[1] == 1:  # if this cluster only meets with black stones
            black_score += cluster_size[current_cluster]  # the black has this territory as score

    return (white_score, black_score), cluster_num, cluster_type, cluster_size


def cluster_blank(x, y, num, cluster_num, board):

    if board.board[x, y] != 0:  # if this isn't blank
        return False  # there is no change

    if cluster_num[x, y] != 0:  # if this is included in a cluster already
        return False  # there is no change

    cluster_num[x, y] = num  # include this in cluster (#num)

    for offset in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        nx, ny = x + offset[0], y + offset[1]
        if 0 <= nx < cluster_num.shape[0] and 0 <= ny < cluster_num.shape[1]:
            # recursively, DFS
            cluster_blank(nx, ny, num, cluster_num, board)  # include around blanks in the cluster of this

    return True  # change exists
