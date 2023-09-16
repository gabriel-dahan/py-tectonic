from typing import Union, List, Tuple, Set
from pathlib import Path
import numpy as np

from prettytable import PrettyTable, ALL

from _types import Cell, Matrix

def unique_arrs_list(ndarrays: List[np.ndarray]) -> List[np.ndarray]:
    # Cette fonction convertit la liste de matrices numpy en liste de leur correspondance en octets, permettant de transformer tout ça en set et de supprimer les doublons.
    bytes_list = [arr.tobytes() for arr in ndarrays]
    unique_bytes_set = set(bytes_list)
    return [np.frombuffer(b, dtype=int).reshape(arr.shape) for b, arr in zip(unique_bytes_set, ndarrays)] # Ici on revient aux matrices initiales à partir des octets.

class TectonicConfig(object):
    
    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        self.config = path

        self.cells = self.extract_cells()
        # Vérifie toutes les assertions nécessaires à la validité de la grille de jeu.
        self.asserts() 
        self.matrix = self.extract_matrix()

    def extract_cells(self) -> List[Cell]:
        cells = []
        for line in self.extract_matrix():
            cells += line
        return cells
    
    def extract_matrix(self) -> Matrix:
        with open(self.config.absolute(), 'r') as fp:
            return [
                [Cell(int(arg[0]), (i, j), int(arg[1]) or None) for i, arg in enumerate(line.split(','))] 
                    for j, line in enumerate(fp.readlines())
            ]
        
    def get_groups_nbs(self) -> set:
        # Renvoie un set contenant tous les numéros de groupe présents dans la grille de jeu.
        return {cell.group for cell in self.cells}
    
    def get_group_cells(self, group: int) -> List[Cell]:
        assert group in self.get_groups_nbs()
        return list(filter(lambda cell : cell.group == group, self.cells))
    
    def get_groups_values(self) -> List[Tuple[int, List[Cell]]]:
        return [(group, self.get_group_cells(group)) for group in self.get_groups_nbs()]
    
    def asserts(self) -> None:
        for group in self.get_groups_nbs():
            group_values = [cell.value for cell in self.get_group_cells(group) if cell.value]
            assert sorted(group_values) == list(set(group_values)), f'Les valeurs des cellules ne sont pas uniques dans le groupe [{group}].'
        
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        table = PrettyTable()
        table.hrules = ALL
        for line in (self.matrix):
            table.add_row([f'{elem.value or 0} ({elem.group})' for elem in line])
        return f'<TectonicConfig> \n{table.get_string(header=False)}'
    
class SmartTectonicConfig(TectonicConfig):

    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__(path)
        self.msize = (len(self.matrix), len(self.matrix[0]))
    
    def unit_array(self, i, j):
        arr = np.zeros(self.msize, dtype = int)
        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                y = (y + j) % (arr.shape[0]) # e.g. Commence à la case j à la place de la case 0, puis j+1 à la place de 1, ... jusqu'à revenir à 0 au modulo.
                x = (x + i) % (arr.shape[1]) # Même exemple qu'au dessus.
                start_row, end_row = max(y - 1, 0), min(y + 1 + 1, arr.shape[0])
                start_col, end_col = max(x - 1, 0), min(x + 1 + 1, arr.shape[1])
                neighbours = list(arr[start_row : end_row, start_col : end_col].flatten())
                if 1 not in neighbours:
                    arr[y, x] = 1
        return arr

    def unit_arrays(self):
        arrs = []
        for j in range(self.msize[0] + 1):
            arrs.extend(self.unit_array(i, j) for i in range(self.msize[1]))
        return unique_arrs_list(arrs)

if __name__ == '__main__':
    from pprint import pprint
    tc = SmartTectonicConfig('configs/conf.tec')
    for i, arr in enumerate(tc.unit_arrays()):
        print(f'\n-----{i + 1}-----\n')
        print(arr) 