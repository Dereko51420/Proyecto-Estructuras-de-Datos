class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.start_position = position
        self.keys_collected = 0
        self.last_direction = None
        self.lives = 3

    def move(self, direction, board):
        self.last_direction = direction
        r, c = self.position
        moves = {
            "UP": (-1,0),
            "DOWN": (1,0),
            "LEFT": (0,-1),
            "RIGHT": (0,1)
        }
        if direction in moves:
            dr, dc = moves[direction]
            new = (r+dr, c+dc)
            if board.is_valid_cell(new):
                self.position = new
                return True
        return False
