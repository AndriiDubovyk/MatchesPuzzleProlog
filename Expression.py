from Symbol import Symbol, symbol_to_matches, match_to_orientation

FREE_SPACE = 20 # Space between symbols

def get_removed_match(start_exp, end_exp):
    for i in range(0, len(start_exp)):
        sc = start_exp[i]
        fc = end_exp[i]
        diff = symbol_to_matches[sc] - symbol_to_matches[fc]
        if diff:
            return (i, list(diff)[0])
    return (-1, -1)

def get_pasted_match(start_exp, end_exp):
    for i in range(0, len(start_exp)):
        sc = start_exp[i]
        fc = end_exp[i]
        diff = symbol_to_matches[fc] - symbol_to_matches[sc]
        if diff:
            return (i, list(diff)[0])
    return (-1, -1)
        



class Expression:

    # available symbols: 0,1,2,3,4,5,6,7,8,9,-,+,=
    def __init__(self, canvas, x, y, exp_str):
        if not exp_str:
            return
        self.canvas = canvas
        self.x = x
        self.y = y
        self.exp_str = exp_str
        self.symbol_list = [None] * 5
        self.symbol_list[0] = num1_sym = Symbol(canvas, x, y, exp_str[0])
        self.symbol_list[1] = op_sym = Symbol(canvas, num1_sym.x_edge + FREE_SPACE, y, exp_str[1])
        self.symbol_list[2] = num2_sym = Symbol(canvas, op_sym.x_edge + FREE_SPACE, y, exp_str[2])
        self.symbol_list[3] = equal_sym = Symbol(canvas, num2_sym.x_edge + FREE_SPACE, y, exp_str[3])
        self.symbol_list[4] = num3_sym = Symbol(canvas, equal_sym.x_edge + FREE_SPACE, y, exp_str[4])
        self.showcase_pos = (op_sym.x_edge + FREE_SPACE, y - 100)
        self.is_in_target = True
        
    def set_target_exp(self, target_exp_str):
        self.target_exp_str = target_exp_str
        self.removed_match_pos = get_removed_match(self.exp_str, target_exp_str)
        self.pasted_match_pos = get_pasted_match(self.exp_str, target_exp_str)
        self.end_pos = self.__get_end_pos()
        self.is_in_target = False
        self.is_in_showcase = False

    def __get_end_pos(self):
        symbol, match = self.pasted_match_pos
        cur_symbol = self.symbol_list[symbol]
        return cur_symbol.get_match_placeholder_pos(match)

    def is_in_target(self):
        return self.is_in_target

    def move_to_target(self):
        symbol, match = self.removed_match_pos
        cur_symbol = self.symbol_list[symbol]
        cur_match = cur_symbol.match_list[match]
        if not self.is_in_showcase:
            cur_symbol.move_match_to(match, self.showcase_pos[0], self.showcase_pos[1])
            if cur_match.get_pos() == self.showcase_pos:
                self.is_in_showcase = True
                cur_match.set_orientation(match_to_orientation[self.pasted_match_pos[1]])
        else:
            self.is_in_showcase = True
            cur_symbol.move_match_to(match, self.end_pos[0], self.end_pos[1])
            if cur_match.get_pos() == self.end_pos:
                self.is_in_target = True