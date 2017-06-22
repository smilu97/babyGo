
from ...GoBoard import GoBoard


def test_checking_surrounded():
    board = GoBoard()

    test_case = [
        [0, 0, 1, 0, 0],
        [0, 1, -1, 1, 0],
        [1, -1, 0, -1, 1],
        [0 ,1, -1, 1, 0],
        [0, 0, 1, 0, 0]
    ]

    for i in range(5):
        for j in range(5):
            board.set(i, j, board.board_value_to_name(test_case[i][j]))

    board.set(2, 2, 'white')

    board.check_surrounded_all()

    result_case = [
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0]
    ]

    result_correct = True

    for i in range(5):
        for j in range(5):
            if board.board[i,j] != result_case[i][j]:
                result_correct = False
                break
        if not result_correct:
            break

    if not result_correct:
        raise Exception('result not currect!')