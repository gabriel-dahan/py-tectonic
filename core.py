from typing import Union, List, Tuple
from pathlib import Path
import itertools
import numpy as np
import copy

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
        self.asserts()
        self.grid = self.extract_matrix()

    def extract_cells(self) -> List[Cell]:
        cells = []
        with open(self.config.absolute(), 'r') as fp:
            raw = fp.readlines()
            for line in raw:
                cells += [Cell(int(arg[0]), int(arg[1]) or None) for arg in line.split(',')]
        return cells
    
    def extract_matrix(self) -> List[List[int]]:
        with open(self.config.absolute(), 'r') as fp:
            return [
                [Cell(int(arg[0]), int(arg[1]) or None) for arg in line.split(',')] 
                    for line in fp.readlines()
            ]
    
    def get_groups(self) -> set:
        return {cell.group for cell in self.cells}
    
    def get_group_values(self, group: int) -> List[int]:
        assert group in self.get_groups()
        return [cell.value for cell in filter(lambda cell : cell.group == group, self.cells)]
    
    def asserts(self) -> None:
        for group in self.get_groups():
            group_values = [value for value in self.get_group_values(group) if value]
            assert sorted(group_values) == list(set(group_values)), f'Values are not unique in group [{group}].'

    def group_permutations(self, group: int) -> List[List[int]]:
        values = self.get_group_values(group)
        indicated = [(values.index(val), val) for val in values if val]
        return [list(perm) for perm in itertools.permutations(range(1, len(values) + 1)) if all(perm[i] == v for i, v in indicated)]
    
    def groups_permutations(self) -> itertools.product:
        groups_permutations = [self.group_permutations(group) for group in self.get_groups()]
        return [list(perm) for perm in itertools.product(*groups_permutations)]
    
    def groups_to_grid(self, groups_permutation: List[List[int]]) -> List[List[int]]:
        gp = copy.deepcopy(groups_permutation)
        grid = []
        for line in self.grid:
            grid_line = []
            for cell in line:
                grid_line.append(gp[cell.group][0])
                gp[cell.group].pop(0)
            grid.append(grid_line)
        return grid
    
    def grid_permutations(self) -> List[List[List[int]]]:
        return [self.groups_to_grid(perm) for perm in self.groups_permutations()]

    def is_solution(self, grid: List[List[int]]) -> bool:
        matrix = np.array(grid)
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                start_row, end_row = max(j - 1, 0), min(j + 1 + 1, matrix.shape[0])
                start_col, end_col = max(i - 1, 0), min(i + 1 + 1, matrix.shape[1])
                neighbours = list(matrix[start_row : end_row, start_col : end_col].flatten())
                neighbours.remove(grid[j][i])
                if list(filter(
                    lambda cell : cell == grid[j][i],
                    neighbours
                )):
                    return False
        return True
    
    def solution(self) -> List[List[int]]:
        sols = []
        for grid in self.grid_permutations():
            grid = [list(line) for line in grid]
            if self.is_solution(list(grid)):
                sols.append(list(grid))
        return sols

if __name__ == '__main__':
    t = Tectonic('configs/conf.tec')
    print(t.solution())