import copy
import random

import cairosvg
import chess
import chess.svg
import PIL
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


class Candidate_AI_bot:

    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {chess.BLACK: chess.WHITE, chess.WHITE: chess.BLACK}

    def best_strategy(self, board, color, depth):
        # returns best move

        best_move = self.alphabeta(board, color, depth, -10000, 10000)
        return best_move

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = board.legal_moves
        # print(poss)
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return self.evaluate(board, color, poss)
        v = (-1000000, board)

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
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return -self.evaluate(board, color, poss)
        v = (1000000, board)

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
        b = chess.Board.copy(board)
        b.push(move)
        return b

    def is_done(self, my_board, color):
        return True if my_board.is_checkmate() or my_board.is_stalemate() or my_board.can_claim_draw() else False

    def evaluate(self, board, color, possible_moves):
        fen = board.board_fen()
        if board.is_checkmate():
            # print("CHECKMATE")
            return -100000
        piece_total = 0
        for piece in fen:
            if not color:
                if piece == "p":
                    piece_total += 1
                elif piece == "b" or piece == "n":
                    piece_total += 3
                elif piece == "r":
                    piece_total += 5
                elif piece == "q":
                    piece_total += 9
                elif piece == "P":
                    piece_total -= 1
                elif piece == "B" or piece == "N":
                    piece_total -= 3
                elif piece == "R":
                    piece_total -= 5
                elif piece == "Q":
                    piece_total -= 9
            else:
                if piece == "p":
                    piece_total -= 1
                elif piece == "b" or piece == "n":
                    piece_total -= 3
                elif piece == "r":
                    piece_total -= 5
                elif piece == "q":
                    piece_total -= 9
                elif piece == "P":
                    piece_total += 1
                elif piece == "B" or piece == "N":
                    piece_total += 3
                elif piece == "R":
                    piece_total += 5
                elif piece == "Q":
                    piece_total += 9
        #print(board)

        #print()
        attack_total = 0
        for square in chess.SQUARES:
            attack_total += 1 if board.is_attacked_by(color, square) else 0
            attack_total -= 1 if board.is_attacked_by(not color, square) else 0
        # print("piece:", piece_total, "|attack:", attack_total)

        return piece_total * 35 + attack_total


class Best_AI_bot:

    def __init__(self):
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {chess.BLACK: chess.WHITE, chess.WHITE: chess.BLACK}

    def best_strategy(self, board, color, depth):
        # returns best move

        best_move = self.alphabeta(board, color, depth, -10000, 10000)
        return best_move

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = board.legal_moves
        # print(poss)
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return self.evaluate(board, color, poss)
        v = (-1000000, board)

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
        if search_depth == 0 or poss is None or self.is_done(board, color) is True:
            return -self.evaluate(board, color, poss)
        v = (1000000, board)

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
        b = chess.Board.copy(board)
        b.push(move)
        return b

    def is_done(self, my_board, color):
        return True if my_board.is_checkmate() or my_board.is_stalemate() or my_board.can_claim_draw() else False

    def evaluate(self, board, color, possible_moves):
        fen = board.board_fen()
        if board.is_checkmate():
            # print("CHECKMATE")
            return -100000 if board.turn is color else 100000
        if board.is_game_over():
            return -10000
        piece_total = 0
        for piece in fen:
            if not color:
                if piece == "p":
                    piece_total += 1
                elif piece == "b" or piece == "n":
                    piece_total += 3
                elif piece == "r":
                    piece_total += 5
                elif piece == "q":
                    piece_total += 9
                elif piece == "P":
                    piece_total -= 1
                elif piece == "B" or piece == "N":
                    piece_total -= 3
                elif piece == "R":
                    piece_total -= 5
                elif piece == "Q":
                    piece_total -= 9
            else:
                if piece == "p":
                    piece_total -= 1
                elif piece == "b" or piece == "n":
                    piece_total -= 3
                elif piece == "r":
                    piece_total -= 5
                elif piece == "q":
                    piece_total -= 9
                elif piece == "P":
                    piece_total += 1
                elif piece == "B" or piece == "N":
                    piece_total += 3
                elif piece == "R":
                    piece_total += 5
                elif piece == "Q":
                    piece_total += 9
        #print(board)

        #print()
        attack_total = 0
        for square in chess.SquareSet(chess.BB_CENTER):
            attack_total += 1 if board.is_attacked_by(color, square) and board.piece_at(square) is None else 0
            attack_total -= 1 if board.is_attacked_by(not color, square) and board.piece_at(square) is None else 0
        # print("piece:", piece_total, "|attack:", attack_total)

        return piece_total * 35 + attack_total


board = chess.Board()
squares = board.attacks(chess.E4)
open('out.svg', 'w').write(chess.svg.board(board, size=500))
bbot = Best_AI_bot()
bot2 = Candidate_AI_bot()
# print(board.piece_at(chess.A4))
from tkinter import *
tk = Tk()
# frame=tk.Frame(main)
from PIL import Image, ImageTk

img = Image.open('temp.png')
pimg = ImageTk.PhotoImage(img)
size = img.size
frame = Canvas(tk, width=size[0], height=size[1])
frame.pack()
frame.create_image(0, 0, anchor='nw', image=pimg)
tk.update()
while True:
    board.push(Best_AI_bot.best_strategy(bbot, board, True, 3)[1])

    open('out.svg', 'w').write(chess.svg.board(board, size=500, flipped=True))
    # drawing = svg2rlg("out.svg")
    # renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
    cairosvg.svg2png(url='out.svg', write_to='temp.png')
    img = Image.open('temp.png')
    pimg = ImageTk.PhotoImage(img)
    frame.create_image(0, 0, anchor='nw', image=pimg)
    tk.update()
    print("white moved")
    print(board)
    if board.is_checkmate():
        print("White wins")
        break
    if board.is_game_over():
        print("Game over")
        break
    lm = [a for a in board.legal_moves]
    for index, value in enumerate(lm):
        print(index, " ", value)

    board.push(Candidate_AI_bot.best_strategy(bot2, board, False, 3)[1])

    # board.push(random.choice(lm))
    # board.push(chess.Move.from_uci(input()))
    print("black moved")
    open('out.svg', 'w').write(chess.svg.board(board, size=500, flipped=True))
    # drawing = svg2rlg("out.svg")
    # renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
    cairosvg.svg2png(url='out.svg', write_to='temp.png')
    img = Image.open('temp.png')
    pimg = ImageTk.PhotoImage(img)
    frame.create_image(0, 0, anchor='nw', image=pimg)
    tk.update()
    print(board)
    if board.is_checkmate():
        print("Black wins")
        break
    if board.is_game_over():
        print("Game over")
        break
    # break
