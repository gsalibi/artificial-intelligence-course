'''
Este arquivo é adaptado de AIMA-PYTHON

Por Gustavo Salibi (174135)
'''
from sources.search import *

# Representação do mapa sugerido no enunciado discretizado com o dobro
frame = line(0, 0, 0, 1, 121)  # borda esqueda
frame |= line(120, 0, 0, 1, 121)  # borda direita
frame |= line(0, 0, 1, 0, 121)  # borda baixo
frame |= line(0, 120, 1, 0, 121)  # borda cima


# mapas utilizados nos testes
m1 = GridProblem(print_name='m1',
                 initial=(20, 20), goal=(100, 100), obstacles=frame| line(40, 0, 0, 1, 81) | line(80, 40, 0, 1, 81))
m2 = GridProblem(print_name='m2',initial=(1, 1), goal=(119, 119),
                 obstacles=frame | random_lines(X=range(1, 102),Y=range(1, 102), N=10, lengths=range(10, 25)))
m3 = GridProblem(print_name='m3', initial=(3, 4), goal=(78, 100),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=100, lengths=range(6, 18)))
m4 = GridProblem(print_name='m4', initial=(50, 2), goal=(50, 105),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=150, lengths=range(6, 18)))
m5 = GridProblem(print_name='m5', initial=(3, 88), goal=(100, 18),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=200, lengths=range(6, 18)))
m6 = GridProblem(print_name='m6', initial=(18, 96), goal=(77, 2),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=250, lengths=range(6, 18)))
m7 = GridProblem(print_name='m7', initial=(13, 100), goal=(2, 2),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=300, lengths=range(6, 18)))
m8 = GridProblem(print_name='m8', initial=(75, 43), goal=(2, 100),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=350, lengths=range(4, 18)))
m9 = GridProblem(print_name='m9', initial=(2, 62), goal=(105, 85),
                 obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=400, lengths=range(2, 12)))
m10 = GridProblem(print_name='m10', initial=(2, 118), goal=(118, 2),
                  obstacles=frame | random_lines(X=range(1, 102), Y=range(1, 102), N=400, lengths=range(2, 12)))


# Imprime estat￿ísticas dos algoritmos de busca utilizados
# Imprime um mapa para cada algoritmo de busca. Para visualizar outro mapa, basca mudar o valor de print_map
report((breadth_first_bfs,
        uniform_cost_search,
        astar_straight_line,
        astar_manhattan,
        greedy_straight_line,
        greedy_manhattan),
       [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10],
       print_map=m1)
