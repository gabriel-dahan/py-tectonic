from typing import Union, List
from pathlib import Path

class Cell(object):

    def __init__(self, group: int, value: int = None) -> None:
        self.group = group
        self.value = value

    def __str__(self) -> str:
        return f'Cell(group: {self.group}, value: {self.value})'
    
    def __repr__(self) -> str:
        return str(self)

class Tectonic(object):

    def __init__(self, config: Union[Path, str]) -> None:
        if isinstance(config, str):
            config = Path(config)
        self.config = config
        self.cells = self.extract_cells()

    def extract_cells(self) -> List[Cell]:
        cells = []
        with open(self.config, 'r') as fp:
            raw = fp.readlines()
            for line in raw:
                cells += [Cell(int(arg[0]), int(arg[1]) or None) for arg in line.split(',')]
        return cells
    
if __name__ == '__main__':
    t = Tectonic('configs/1.tec')
    print(t.cells)