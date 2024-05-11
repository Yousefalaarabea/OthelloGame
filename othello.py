import score, turtle, random
from board import board

MOVE_DIRS = [ (-1,-1), (-1,0), (-1,1),
              (0,-1), (0,1),
              (1,-1), (1,0), (1,1)]


class othello:
    def __init__(self, n=8):
        n = 8
        turtle.title('Othello')
        board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2,2]

    # def draw_board(self):
    #      board.draw_board(self.board)



    def initialize_board(self):
        if self.n < 2:
            return

        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
        initial_squares = [(coord1, coord2), (coord1, coord1),
                           (coord2, coord1), (coord2, coord2)]

        for i in range(len(initial_squares)):
            color = i%2
            row = initial_squares[i][0]
            col = initial_squares[i][1]
            self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)

    def make_move(self):
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.draw_tile(self.move, self.current_player)
            self.flip_tiles()

    def flip_tiles(self):
        curr_tile = self.current_player + 1
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move,direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[0] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles [self.current_player] += 1
                        self.num_tiles[(self.current_player +1)%2] -=1
                        self.draw_tile((row, col), self.current_player)
                        i += 1

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0,1) and \
            self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[0] + direction[1] * i
                if not self.is_valid_coord(row, col) or\
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1

        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row , col)
                if self.is_legal_move(move):
                    return True
        return False

    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row , col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves

    def is_legal_move(self, move):
        if move != () and self.is_valid_coord(move[0], move[1])\
            and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False

    def run(self):
        if self.current_player not in [0,1]:
            print('Error, unknow player.Quittt...')
            return

        self.current_player = 0
        print('Your Turn..')
        turtle.onscreenclick(self.play)
        turtle.mainloop()

    def play(self,x,y):
        if self.has_legal_move():
            self.get_coord(x,y)
            if self.is_legal_move(self.move):
                turtle.onscreenclick(None)
                self.make_move()
            else:
                return

        while True:
            self.current_player = 1
            if self.has_legal_move():
                print('Computer\'s turn..')
                self.make_random_move()
                self.current_player = 0
                if self.has_legal_move():
                    break
            else:
                 break

        self.current_player = 0

        if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
            turtle.onscreenclick(None)
            print('--------------')
            self.report_result()
            name = input('Enter your name: \n')
            if not score.update_scores(name,self.num_tiles[0]):
                print('Your Score has not been saved.\n')
            print('Thank you for playing!')
            close = input('Exit Game?(y/n)')
            if close == 'y':
                turtle.bye()
            elif close != 'n':
                print('Quit in 3s...')
                turtle.ontimer(turtle.bye,3000)
        else:
            print('Your Turn..')
            turtle.onscreenclick(self.play)

    def make_random_move(self):
        moves = self.get_legal_moves()
        if moves:
            self.move = random.choice(moves)
            self.make_move()

    def report_result(self):
        print('Game over:)')
        if self.num_tiles[0] > self.num_tiles[1]:
            print('You are the Winner :)',
                  'You have %d tiles , but the computer has %d tiles'
                  % (self.num_tiles[0], self.num_tiles[1]))
        elif self.num_tiles[0] < self.num_tiles[1]:
            print('You Lose :(',
                  'the computer has %d tiles, but you have %d tiles'
                  % (self.num_tiles[1], self.num_tiles[0]))
        else:
            print('Draw!! Both of You Got %d tiles' % (self.num_tiles[0]))

    def __str__(self):
        player_str = 'Current Player:' + str(self.current_player + 1) + '\n'
        num_tiles_str = ('# of black tiles -- 1'+ str(self.num_tiles[0]) +
                         '\n' + '# of white tiles -- 2'+ str(self.num_tiles[1]) + '\n')
        board_str = board.__str__(self)
        printable_str = player_str + num_tiles_str + board_str
        return printable_str

    def __eq__(self, other):
        return board.__eq__(self, other) and self.current_player == other.current_player





