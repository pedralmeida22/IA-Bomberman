from Node import *
from mapa import Map
from defs2 import dist_to, choose_move

def getKey(pos):
    if len(pos) != 2:
        return ''
    
    if pos == [1,0]:
        return 'd'
    elif pos == [-1,0]:
        return 'a'
    elif pos == [0,1]:
        return 's'
    elif pos == [0,-1]:
        return 'w' 
    else:
        return ''

def goToPosition(my_pos, next_pos):
    print('goToPosition'.center(50, '-'))
    print('my_pos: ' + str(my_pos))
    print('next_pos: ' + str(next_pos))

    mx,my = my_pos
    nx,ny = next_pos

    res = [nx-mx, ny-my]
    print('res: ' + str(res))
    return getKey(res)


# retorna a key para um inimigo ou '' caso nao encontre
def pathToEnemy(mapa, my_pos, enemy_pos):
    # procura caminho para inimigo
    if enemy_pos is not None:
        # procura caminho para o inimigo
        positions = astar(mapa.map, my_pos, enemy_pos, mapa, False)
        print('positions to enemie: ' + str(positions))

        if positions != [] and positions is not None:
            if len(positions) == 1:
                return 'B'

            # se a posiçao seguinte for igual à posiçao atual
            # tira essa posição da lista
            while dist_to(my_pos, positions[0]) == 0:
                print('my_pos == next_pos')
                print('apagar posições inuteis')
                print('positions' + str(positions))
                positions.pop(0)

            return goToPosition(my_pos, positions[0])

        # nao encontrou caminho
        return ''

# pesquisa caminho para objetivo
def findPath(mapa, my_pos, goal, exact_pos):
    print('Pesquisando caminho para objetivo...')
    positions = astar(mapa.map, my_pos, goal, mapa, exact_pos)
    print('positions goal: ' + str(positions))

    # nao encontra caminho para o objetivo
    if positions == [] or positions == None:
        print('Caminho nao encontrado para objetivo...')
        return []

    # se a proxima posiçao for igual à minha posiçao atual
    while dist_to(my_pos, positions[0]) == 0:
        print('my_pos == next_pos')
        print('apagar posições inuteis')
        positions.pop(0)

    # impossivel seguir caminho -> pesquisa outra vez
    if dist_to(my_pos, positions[0]) > 1:
        print("Next_pos invalida!! - Pesquisar caminho outra vez!!")

    return positions

    

# retorna a key para uma parede
def keyPath(my_pos, positions):
    # nao precisa de pesquisar caminho
    if positions != []:
        print('Não precisa de pesquisar...')
        print('positions: ' + str(positions))

        key = goToPosition(my_pos, positions[0])
        goal = positions[-1]
        positions.pop(0)
        return key, positions, goal
        



def goTo(mapa, my_pos, ways, positions, goal, exact_pos):
    # nao sabe o caminho -> pesquisa
    if positions == []:
        path = findPath(mapa, my_pos, goal, exact_pos)

        # nao foi possivel encontrar caminho -> usa outra função
        if path == []:
            key = choose_move(my_pos, ways, goal)
            return key, [], goal
        
        positions = path

    # ja tem caminho
    return keyPath(my_pos, positions)