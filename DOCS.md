# $\text{Documentation}$
## $\text{Classes}$

> Classe `Cell` : \
> Caractérise une cellule de la grille du jeu par le groupe auquel elle appartient et sa valeur dans ce groupe. 
>
> - `group` [`int`]
> - `value` [`int`]
>
> *Méthodes* :
> - `__init__`, `__str__`, `__repr__` : Méthodes spéciales pré-existentes (seulement modifiées).

> Classe `Tectonic` : \
> Caractérise le jeu dans son ensemble (configuration de grilles, cellules), et permet sa résolution.
>
> - `config` [`str`, `Path`] : Configuration initiale non complète dans un fichier texte dont on précise le chemin relatif ou absolu (exemple de configuration dans le fichier `configs/conf.tec`).
>
> *Méthodes* :
> - `__init__`, `__str__`, `__repr__` : Méthodes spéciales pré-existentes (seulement modifiées).
> - `extract_cells()` -> `List[Cell]` : Extrait les cellules du fichier de configuration et renvoie une liste simple les contenant.
> - `extract_matrix()` -> `np.array` : Extrait la grille de jeu entière, avec les cellules dans l'ordre du fichier de configuration, sous la forme d'un tableau `numpy`.
> - `get_groups()` -> `set` : Renvoie un set contenant tous les groupes existants sur la grille.
> - `get_group_values(group: int)` -> `List[int]` : Renvoie toutes les valeurs des cellules présentes dans un groupe. Toute cellule non définie (car non renseignée sur la grille initiale) aura la valeur `None`.
> - `asserts()` -> `None` : Vérifie que tous les groupes n'ont aucune valeur double dans la grille initiale.
> - `group_permutations(group: int)` -> `np.array` : Renvoie un tableau numpy de toutes les permutations possibles d'un groupe (en fonction des valeurs renseignées initialement).
> - `groups_permutations()` -> `np.array` : Renvoie toutes les permutations de tous les groupes permutés simultanément (donc un très grand array `numpy` de dimension 3).
> - `groups_to_grid(groups_permutation: np.array)` -> `np.array`: Transforme une permutation de groupes en sa correspondance sur la grille du jeu.
> - `grid_permutations()` -> `np.array` : Renvoie toutes les permutations de grilles de jeu possibles répondant au conditions initiales (beaucoup (beaucoup) de grilles).
> - `is_solution(grid: np.array)` -> `bool` : Vérifie qu'une permutation de grille du jeu est bien solution, renvoie un booléen l'indiquant.
> - `solution()` -> `np.array` : Renvoie la (les ?) solution(s) trouvée(s) par le programme.