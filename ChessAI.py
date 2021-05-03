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

    def best_strategy(self, board, color, depth, maxTime, startTime):
        # returns best move
        # boardC = board.copy()
        # best_move = self.alphabeta(board.copy(), color, 1, -10000, 10000, maxTime, startTime)
        for x in range(1, 100):
            try:
                best_move = self.alphabeta(board.copy(), color, x, -10000, 10000, maxTime, startTime)
                # best_move = best_move2
                # print(best_move)
            except TimeoutError:
                if x == 1:
                    best_move = random.choice(board.legal_moves)
                    print(x - 1)
                    break
                else:
                    d = x - 1
                    print(x - 1)
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
        return True if my_board.is_checkmate() or my_board.is_stalemate() else False

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
        # print(board)

        # print()
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


board = chess.Board()
squares = board.attacks(chess.E4)
open('out.svg', 'w').write(chess.svg.board(board, size=500))
bbot = Best_AI_bot()
bot2 = Candidate_AI_bot()
# bbot = Candidate_AI_bot()
# bot2 = Best_AI_bot()
# print(board.piece_at(chess.A4))
from tkinter import *

tk = Tk()
# frame=tk.Frame(main)
from PIL import Image, ImageTk

open('out.svg', 'w').write(chess.svg.board(board, size=500, flipped=True))
cairosvg.svg2png(url='out.svg', write_to='temp.png')
img = Image.open('temp.png')
pimg = ImageTk.PhotoImage(img)
size = img.size
frame = Canvas(tk, width=size[0], height=size[1])
frame.pack()
frame.create_image(0, 0, anchor='nw', image=pimg)
tk.update()
print(Best_AI_bot.evaluate(bbot, board, True, []))
print(len(board.move_stack))
import time

depth_list = []
depth_list_2 = []
depth = 5
while True:
    curtime = time.time()
    while True:
        try:
            curtime = time.time()
            move, d = Best_AI_bot.best_strategy(bbot, board, True, 4, depth, time.time())
            depth_list_2.append(d)
            # move = Candidate_AI_bot.best_strategy(bbot, board, True, 4)
            break
        except ValueError:
            print("ERROR: Illegal Move, Try Again")
    board.push(move[1])
    print(move, " White: ", time.time() - curtime, "\n")

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
        print("Black Depth Avg: ", sum(depth_list) / len(depth_list))
        print("White Depth Avg: ", sum(depth_list_2) / len(depth_list_2))
        while True:
            pass
    if board.is_game_over():
        print("Game over")
        print("Black Depth Avg: ", sum(depth_list) / len(depth_list))
        print("White Depth Avg: ", sum(depth_list_2) / len(depth_list_2))
        while True:
            pass
    lm = [a for a in board.legal_moves]
    # for index, value in enumerate(lm):
    #     print(index, " ", value)

    curtime = time.time()
    # move = Best_AI_bot.best_strategy(bot2, board, False, 4)
    # move = Candidate_AI_bot.best_strategy(bot2, board, False, 4)
    # board.push(move[1])
    # print(move, " Black: ",time.time() - curtime, "\n")

    # board.push(random.choice(lm))  # TODO RANDOM
    while True:
        try:
            move = input()  # TODO HUMAN INPUT BLACK
            curtime = time.time()
            # move, d = Candidate_AI_bot.best_strategy(bot2, board, False, 4, depth, time.time())
            # move, d = Best_AI_bot.best_strategy(bbot, board, False, 4, depth, time.time())
            depth_list.append(d)
            if chess.Move.from_uci(move) not in lm:
                raise ValueError
            board.push(chess.Move.from_uci(move))
            # board.push(move[1])
            break
        except ValueError:
            print("ERROR: Illegal Move, Try Again")
        except TypeError:
            board.push(random.choice(lm))
    print("black moved")
    print(move, " Black: ", time.time() - curtime, "\n")
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
        print("Black Depth Avg: ", sum(depth_list) / len(depth_list))
        print("White Depth Avg: ", sum(depth_list_2) / len(depth_list_2))
        while True:
            pass
    if board.is_game_over():
        print("Game over")
        print("Black Depth Avg: ", sum(depth_list) / len(depth_list))
        print("White Depth Avg: ", sum(depth_list_2) / len(depth_list_2))
        while True:
            pass
    # break
