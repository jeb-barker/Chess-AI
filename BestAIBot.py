
import chess
import random
import time
class Best_AI_bot:

    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {chess.BLACK: chess.WHITE, chess.WHITE: chess.BLACK}

    def best_strategy(self, board, color, depth, maxTime, startTime):
        # returns best move
        # boardC = board.copy()
        # best_move = self.alphabeta(board.copy(), color, 1, -10000, 10000, maxTime, startTime)
        for x in range(0, 100):
            try:
                best_move = self.alphabeta(board.copy(), color, x, -10000, 10000, maxTime, startTime)
                # best_move = best_move2
                # print(best_move)
            except TimeoutError:
                if x == 1:
                    best_move = random.choice(board.legal_moves)
                d = x - 1
                print(d)
                break
        return best_move, d

    def max_value(self, board, color, search_depth, alpha, beta, maxTime, startTime):
        # return value and state: (val, state)
        poss = board.legal_moves
        # print(poss)
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return self.evaluate(board, color, poss)
        if time.time() - startTime > maxTime:
            raise TimeoutError
        v = (-1000000, board)

        for s in poss:
            board.push(s)
            min = self.min_value(board, chess.WHITE if color == chess.BLACK else chess.BLACK, search_depth - 1, alpha,
                                 beta, maxTime, startTime)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, s), key=lambda item: item[0])
            board.pop()
            if v[0] > beta:
                return v
            alpha = max(v[0], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta, maxTime, startTime):
        # return value and state: (val, state)
        poss = board.legal_moves
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return -self.evaluate(board, color, poss)
        if time.time() - startTime > maxTime:
            raise TimeoutError
        v = (1000000, board)

        for s in poss:
            board.push(s)
            maxV = self.max_value(board, chess.WHITE if color == chess.BLACK else chess.BLACK, search_depth - 1, alpha,
                                  beta, maxTime, startTime)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, s), key=lambda item: item[0])
            board.pop()
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])

        return v

    def alphabeta(self, board, color, search_depth, alpha, beta, maxTime, startTime):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta, maxTime,
                              startTime)  # if color else self.min_value(board, color, search_depth, alpha, beta, maxTime, startTime)

    def make_move(self, board, color, move):
        # returns board that has been updated
        b = chess.Board.copy(board)
        b.push(move)
        return b

    def is_done(self, my_board, color):
        return True if my_board.is_checkmate() or my_board.is_stalemate() or my_board.is_game_over() else False

    def evaluate(self, board, color, possible_moves):
        fen = board.board_fen()
        if board.is_checkmate():
            # print("CHECKMATE")
            return -100000 + len(board.move_stack) if board.turn is color else 100000 - len(board.move_stack)
        if board.is_repetition(3):
            return -100000
        check_bias = 0
        if board.is_check() and board.turn is color:
            check_bias -= 2
        if board.is_check() and board.turn is not color:
            check_bias += 2
        piece_total = 0
        # print(board)
        # print()
        attack_total = 0
        for square in chess.SquareSet(chess.BB_CENTER):
            attack_total += 1 if board.is_attacked_by(color, square) else 0
            attack_total -= 1 if board.is_attacked_by(not color, square) else 0

        pawn_rank_total = 0
        # print(str(board))
        bstring = [a for a in str(board) if a != " " and a != "\n"]
        for index, square in enumerate(bstring):
            # print(board.piece_at(square))
            if not color:
                if square == "p":
                    piece_total += 1
                    pawn_rank_total -= 7 - index // 8
                elif square == "b" or square == "n":
                    piece_total += 3
                elif square == "r":
                    piece_total += 5
                elif square == "q":
                    piece_total += 9
                elif square == "P":
                    piece_total -= 1
                elif square == "B" or square == "N":
                    piece_total -= 3
                elif square == "R":
                    piece_total -= 5
                elif square == "Q":
                    piece_total -= 9
            else:
                if square == "p":
                    piece_total -= 1
                    pawn_rank_total += index // 8 + 1
                elif square == "b" or square == "n":
                    piece_total -= 3
                elif square == "r":
                    piece_total -= 5
                elif square == "q":
                    piece_total -= 9
                elif square == "P":
                    piece_total += 1
                elif square == "B" or square == "N":
                    piece_total += 3
                elif square == "R":
                    piece_total += 5
                elif square == "Q":
                    piece_total += 9

        # print("pawn:", pawn_rank_total)
        return (piece_total * 15) + (attack_total / (.4 * len(board.move_stack) + 1)) + ((1 if color else -1) * (pawn_rank_total) * .1 * len(board.move_stack)) + check_bias
