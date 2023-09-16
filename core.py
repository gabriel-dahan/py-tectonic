from typing import Union, List
from pathlib import Path
import itertools
import numpy as np
import copy

from _types import Cell, Matrix
from configs import TectonicConfig

class Tectonic(object):

    def __init__(self, config: Union[Union[str, Path], TectonicConfig]) -> None:
        if not isinstance(config, TectonicConfig):
            config = TectonicConfig(Path(config))

        self.tec = config

        self.cells = self.tec.extract_cells()
        self.matrix = self.tec.extract_matrix()

    def group_permutations(self, group: int) -> List[List[int]]:
        values = [cell.value for cell in self.tec.get_group_cells(group)]
        indicated = [(values.index(val), val) for val in values if val]
        return [list(perm) for perm in itertools.permutations(range(1, len(values) + 1)) if all(perm[i] == v for i, v in indicated)]
    
    def groups_permutations(self) -> itertools.product:
        groups_permutations = [self.group_permutations(group) for group in self.tec.get_groups_nbs()]
        return [list(perm) for perm in itertools.product(*groups_permutations)]
    
    def groups_to_grid(self, groups_permutation: List[List[int]]) -> Matrix:
        gp = copy.deepcopy(groups_permutation)
        grid = []
        for line in self.matrix:
            grid_line = []
            for cell in line:
                grid_line.append(gp[cell.group][0])
                gp[cell.group].pop(0)
            grid.append(grid_line)
        return grid
    
    def grid_permutations(self) -> List[Matrix]:
        return [self.groups_to_grid(perm) for perm in self.groups_permutations()]

    def is_solution(self, grid: Matrix) -> bool:
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
    
    def solution(self) -> Matrix:
        sols = []
        for grid in self.grid_permutations():
            grid = [list(line) for line in grid]
            if self.is_solution(list(grid)):
                sols.append(list(grid))
        return sols

if __name__ == '__main__':
    t = Tectonic('configs/conf.tec')
    print(t.solution())