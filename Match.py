import math

MATCH_LENGTH = 80
LINE_WIDTH = 5
MAIN_COLOR = "#c7a16f"
END_COLOR = "#ad5f3b"
END_RADIUS = LINE_WIDTH * 1.25
MOVE_SPEED = 7

def move_towards(start, end, dist):
    # calculate the distance between the start and end coordinates
    distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    
    # if the distance is less than the specified distance, just return the end coordinates
    if distance <= dist:
        return end
    
    # calculate the new x and y coordinates that are d units away from the start coordinates in the direction of the end coordinates
    x = start[0] + (end[0] - start[0]) * dist / distance
    y = start[1] + (end[1] - start[1]) * dist / distance
    return (round(x), round(y))

class Match:

    def __init__(self, canvas, x, y, is_horizontal):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.is_horizontal = is_horizontal
        if is_horizontal:
            end_x, end_y = x + MATCH_LENGTH, y
        else:
            end_x, end_y = x, y + MATCH_LENGTH
        self.line = canvas.create_line(x, y, end_x, end_y, fill=MAIN_COLOR, width=LINE_WIDTH)
        r = END_RADIUS
        self.oval = canvas.create_oval(end_x - r, end_y - r, end_x + r, end_y + r, fill=END_COLOR)

    def moveto(self, to_x, to_y):
        new_x, new_y = move_towards((self.x, self.y), (to_x, to_y), MOVE_SPEED)
        x_offset = new_x - self.x
        y_offset = new_y - self.y
        self.canvas.move(self.line, x_offset, y_offset)
        self.canvas.move(self.oval, x_offset, y_offset)
        self.x = new_x
        self.y = new_y

    def set_orientation(self, is_horizontal):
        if self.is_horizontal == is_horizontal:
            return
        else:
            self.is_horizontal = not self.is_horizontal
            self.canvas.delete(self.line)
            self.canvas.delete(self.oval)
            self.__init__(self.canvas, self.x, self.y, self.is_horizontal)

    def get_pos(self):
        return (self.x, self.y)

    
