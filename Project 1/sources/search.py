'''
Este arquivo é adaptado de AIMA-PYTHON

Por Gustavo Salibi (174135)
'''

import matplotlib.pyplot as plt
import random
import heapq
import math
from collections import deque, Counter


# Classe genérica para definição de problemas. Outras classes
# que implementam um problema devem ser subclasses desta
class Problem(object):
    def __init__(self, print_name='', initial=None, goal=None, **kwds):
        self.__dict__.update(print_name=print_name, initial=initial, goal=goal, **kwds)

    # deve ser sobrescrito pela subclasse
    def actions(self, state):
        raise NotImplementedError

    # deve ser sobrescrito pela subclasse
    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def step_cost(self, s, action, s1):
        return 1

    def h(self, node):
        return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


# Define um nó em uma árvore de busca
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(
            state=state, parent=parent, action=action, path_cost=path_cost
        )

    def __repr__(self):
        return '<{}>'.format(self.state)

    def __len__(self):
        return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other):
        return self.path_cost < other.path_cost


# Indica que um algoritmo não encontrou solução
failure = Node('failure', path_cost=math.inf)
# Indica que busca de aprofundamento iterativa foi cortada
cutoff = Node('cutoff', path_cost=math.inf)


# expande um nó, gerando seus filhos
def expand(problem, node):
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.step_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


FIFOQueue = deque  # first-in-first-out
LIFOQueue = list  # ast-in-first-out


# Fila onde o item com o mínimo f(item) é sempre exibido primeiro
class PriorityQueue:
    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []  # um heap de par (score, item)
        for item in items:
            self.add(item)

    def add(self, item):  # adiciona item a fila
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    # remove e retorna o item com o menor valor
    def pop(self):
        return heapq.heappop(self.items)[1]

    def top(self):
        return self.items[0][1]

    def __len__(self):
        return len(self.items)


# busca os nós com o valor mínimo de f(node) primeiro. É utilizada
# para implementar vários métodos de busca. Para isso, basta variar f
def best_first_search(problem, f):
    global reached  # salva nós visitados
    frontier = PriorityQueue([Node(problem.initial)], key=f)
    reached = {}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure


# busca nós mais rasos na árvore primeiro, usando bfs
def breadth_first_bfs(problem):
    return best_first_search(problem, f=len)


# busca nós com menores custos de caminho primeiro
def uniform_cost_search(problem):
    return best_first_search(problem, f=g)


# busca nós com o valor mínimo de f(n) = g(n) + h(n)
def astar_search(problem, h=None):
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + h(n))


# busca nós com o valor mínimo de f(n) = h(n)
def greedy_bfs(problem, h=None):
    h = h or problem.h
    return best_first_search(problem, f=h)


# busca definida para testar heuristica straight_line com astar_search
def astar_straight_line(problem):
    return astar_search(problem, h=problem.h1)


# busca definida para testar heuristica manhatam com astar_search
def astar_manhattan(problem):
    return astar_search(problem, h=problem.h2)


# busca definida para testar heuristica straight_line com greedy_search
def greedy_straight_line(problem):
    return greedy_bfs(problem, h=problem.h1)


# busca definida para testar heuristica manhatam com greedy_search
def greedy_manhattan(problem):
    return greedy_bfs(problem, h=problem.h2)


# retorna custo do caminho
def g(n):
    return n.path_cost

# distância em linha reta entre dois pontos
def straight_line_distance(A, B):
    return sum(abs(a - b)**2 for (a, b) in zip(A, B)) ** 0.5


# distância manhattan: |x1 - x2| + |y1 - y2|
def manhattan_distance(A, B):
    return sum(abs(a - b) for (a, b) in zip(A, B))


# representa navega￿ção em 2D com obst￿áculos por onde o caminho at￿é a
# ￿ção n￿ão pode passar
class GridProblem(Problem):
    def __init__(self, print_name='', initial=(10, 10), goal=(50, 50), obstacles=(), **kwds):
        Problem.__init__(self, print_name=print_name, initial=initial, goal=goal,
                         obstacles=set(obstacles) - {initial, goal}, **kwds)

    # dire￿ções onde o rob￿ô pode se movimentar (45 graus)
    directions = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0), (1, 0),
                  (-1, +1), (0, +1), (1, +1)]

    def step_cost(self, s, action, s1):
        return straight_line_distance(s, s1)

    # heur￿ística 1: dist￿ância em linha reta
    def h1(self, node):
        return straight_line_distance(node.state, self.goal)

    # heir￿ística 2: dist￿ância Manhattan
    def h2(self, node):
        return manhattan_distance(node.state, self.goal)

    # tanto os estados quanto as a￿ções s￿ão representados por pares (x,y)
    def result(self, state, action):
        return action if action not in self.obstacles else state

    # o robô pode se movimentar para qualquer espa￿￿￿ço do plano excluindo os obst￿áculos
    def actions(self, state):
        x, y = state
        return {(x + dx, y + dy) for (dx, dy) in self.directions} - self.obstacles


# uma linha de ponto inicial (x, y), tamanho length, e dire￿ção (dx, dy)
def line(x, y, dx, dy, length):
    return {(x + i * dx, y + i * dy) for i in range(length)}


# torna o resultado determin￿ístico para ser reproduzido novamente
random.seed(42)


# retorna um conjunto de linhas geradas aleatoriamente
def random_lines(X=range(1, 51), Y=range(1, 51), N=100, lengths=range(3, 9)):
    result = set()
    for _ in range(N):
        x, y = random.choice(X), random.choice(Y)
        dx, dy = random.choice(((0, 1), (1, 0)))
        result |= line(x, y, dx, dy, random.choice(lengths))
    return result


# Delega todos os atributos ao objeto e os conta em ._counts
class CountCalls:
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    # delega ao objeto original, depois de incrementar um contador
    def __getattr__(self, attr):
        self._counts[attr] += 1
        return getattr(self._object, attr)


# Mostra estatísticas resumidas para cada search
def report(searchers, problems, print_map=None):
    for searcher in searchers:
        total_reached = 0
        print(searcher.__name__ + ':')
        total_counts = Counter()
        for p in problems:
            prob = CountCalls(p)
            soln = searcher(prob)
            counts = prob._counts
            counts.update(steps=len(soln), cost=soln.path_cost)
            total_counts += counts
            total_reached += len(reached)
            report_counts(counts, p.print_name, reached)
            if p == print_map:
                plot_grid_problem(p, soln, reached, searcher.__name__)
        total = [None] * total_reached
        report_counts(total_counts, 'TOTAL', total)
        print('\n')


# imrprime uma linha do counts report
def report_counts(counts, name, reached=()):
    print('{:5} | states reached: {:7,d} | nodes: {:7,d} | cost: {:6.1f} | steps: {:5,d}'.format(
          name, len(reached), counts['result'], counts['cost'],
          counts['steps'], name))


def plot_grid_problem(grid, solution, reached=(), title='Search'):
    "Use matplotlib to plot the grid, obstacles, solution, and reached."
    plt.figure(figsize=(16, 10))
    plt.title(title)
    plt.axis('equal')
    plt.grid(color='black', linestyle='-', linewidth=0.1)
    plt.scatter(*transpose(grid.obstacles), marker=',', c='black')
    plt.scatter(*transpose(reached), 1**2, marker='.', c='blue')
    plt.scatter(*transpose(path_states(solution)), marker=',', c='green')
    plt.scatter(*transpose([grid.initial]), 9**2, marker='D', c='c')
    plt.scatter(*transpose([grid.goal]), 9**2, marker='8', c='red')
    plt.show()



def transpose(matrix):
    return list(zip(*matrix))




