import copy

import chess
import chess.svg


class Best_AI_bot:

    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {chess.BLACK: chess.WHITE, chess.WHITE: chess.BLACK}

    def best_strategy(self, board, color):
        # returns best move

        best_move = self.alphabeta(board, color, 5, -10000, 10000)
        return best_move

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = board.legal_moves
        # print(poss)
        if search_depth == 0 or len(poss) == 0 or self.is_done(board, color) is None:
            return self.evaluate(board, color, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            min = self.min_value(b, chess.WHITE if color == chess.BLACK else chess.BLACK, search_depth - 1, alpha,
                                 beta)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, s), key=lambda item: item[0])
            if v[0] > beta:
                return v
            alpha = max(v[0], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = board.legal_moves
        if search_depth == 0 or len(poss) == 0 or self.is_done(board, color) is None:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            maxV = self.max_value(b, chess.WHITE if color == chess.BLACK else chess.BLACK, search_depth - 1, alpha,
                                  beta)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, s), key=lambda item: item[0])
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta)

    def make_move(self, board, color, move):
        # returns board that has been updated
        b = chess.Board(board)
        b.push(move)
        return b

    def is_done(self, my_board, color):
        return True if my_board.is_game_over() or my_board.can_claim_draw() else False

    def evaluate(self, board, color, possible_moves):
        fen = board.board_fen()
        total = 0
        for piece in fen:
            if color:
                if piece == "p":
                    total += 1
                elif piece == "b" or piece == "n":
                    total += 3
                elif piece == "r":
                    total += 5
                elif piece == "q":
                    total += 9
            else:
                if piece == "P":
                    total += 1
                elif piece == "B" or piece == "N":
                    total += 3
                elif piece == "R":
                    total += 5
                elif piece == "Q":
                    total += 9
        return total


board = chess.Board()
squares = board.attacks(chess.E4)
open('out.svg', 'w').write(chess.svg.board(board, size=500))
bbot = Best_AI_bot()
print(Best_AI_bot.best_strategy(bbot, board, True))
