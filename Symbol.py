from Match import *

FREE_SPACE = 10  # Space between matches

symbol_to_matches = {
    '0': {0, 1, 2, 4, 5, 6},
    '1': {2, 5},
    '2': {0, 2, 3, 4, 6},
    '3': {0, 2, 3, 5, 6},
    '4': {1, 2, 3, 5},
    '5': {0, 1, 3, 5, 6},
    '6': {0, 1, 3, 4, 5, 6},
    '7': {0, 2, 5},
    '8': {0, 1, 2, 3, 4, 5, 6},
    '9': {0, 1, 2, 3, 5, 6},
    '-': {3},
    '+': {3, 7},
    '=': {8, 9}
}

match_to_orientation = [
    True,   #0
    False,  #1
    False,  #2
    True,   #3
    False,  #4
    False,  #5
    True,   #6
    False,  #7
    True,   #8
    True    #9
]

class Symbol:

    # available symbols: 0,1,2,3,4,5,6,7,8,9,-,+,=
    def __init__(self, canvas, x, y, symbol):
        self.canvas = canvas
        self.symbol = symbol
        self.x = x
        self.y = y
        self.width = MATCH_LENGTH + FREE_SPACE * 2
        self.x_edge = x + self.width
        self.match_list = [None] * 10 # we have 10 matches positions
        self.__create_symbol()

    def __create_symbol(self):
        self.__draw_matches_at(symbol_to_matches[self.symbol])

    #  -0-
    #  1 2
    #  -3-
    #  4 5
    #  -6-
    #
    # 7 - '+'(plus) vertical line
    # 8, 9 - lines for equal symbol '='
    def __draw_match_at(self, pos):
        x_pos, y_pos = self.get_match_placeholder_pos(pos)
        self.match_list[pos] = Match(self.canvas, x_pos, y_pos, match_to_orientation[pos])

    def __draw_matches_at(self, args):
        for arg in args:
            self.__draw_match_at(arg)

    def get_match_placeholder_pos(self, pos):
        x = self.x
        y = self.y
        l = MATCH_LENGTH
        match pos:
            case 0:
                return (x + FREE_SPACE, y)
            case 1:
                return (x, y + FREE_SPACE)
            case 2:
                return (x + l + FREE_SPACE * 2, y + FREE_SPACE)
            case 3:
                return (x + FREE_SPACE, y + l + FREE_SPACE * 2)
            case 4:
                return (x, y + l + FREE_SPACE * 3)
            case 5:
                return (x + l + FREE_SPACE * 2, y + l + FREE_SPACE * 3)
            case 6:
                return (x + FREE_SPACE, y + l * 2 + FREE_SPACE * 4)
            case 7:
                return (x + FREE_SPACE + l / 2, y + FREE_SPACE * 2 + l / 2)
            case 8:
                return (x + FREE_SPACE, y + FREE_SPACE + l * 0.8)
            case 9:
                return (x + FREE_SPACE, y + FREE_SPACE * 2 + l * 1.2)
            case _:
                return (-1, -1)


    def move_match_to(self, match_index, x_to, y_to):
        match = self.match_list[match_index]
        if match:
            match.moveto(x_to, y_to)
