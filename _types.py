from typing import List

class Cell(object):

    def __init__(self, group: int, pos: tuple, value: int = None) -> None:
        self.group = group
        self.value = value
        self.pos = pos

    def __str__(self) -> str:
        return f'Cell(group: {self.group}, value: {self.value}, pos: {self.pos})'
    
    def __repr__(self) -> str:
        return str(self)

Matrix = List[List[Cell]]