from mapa import Map
import math
import random

# para qualquer posicao retorna um lista de possoveis movimentos
def get_possible_ways2(mapa, position):  
    ways = []

    x, y = position
    #print(mapa.map)
    print(position)
    print('direita: ' + str(mapa.map[x + 1][y]) + ' baixo: ' + str(mapa.map[x][y + 1]) + ' esquerda: ' + str(
        mapa.map[x - 1][y]) + ' cima: ' + str(mapa.map[x][y - 1]))

    print((x, y+1) in mapa._walls)
    print([x, y+1] in mapa._walls)
    
    if not mapa.is_blocked([x+1, y]):
        
        ways.append('d')
    if not mapa.is_blocked([x, y+1]):
        
        ways.append('s')
    if not mapa.is_blocked([x-1, y]):
        ways.append('a')
        
    if not mapa.is_blocked([x, y-1]):
        
        ways.append('w')

    return ways


def get_possible_ways(mapa, position):  
    ways = []

    x, y = position
    print('direita:'+str(mapa.map[x+1][y])+'baixo:'+str(mapa.map[x][y+1])+'esquerda:'+str(mapa.map[x-1][y])+'cima:'+str(mapa.map[x][y-1]))
    
    tile1 = mapa.map[x+1][y]
    tile2 = mapa.map[x-1][y]
    tile3 = mapa.get_tile((x,y+1))
    tile4 = mapa.get_tile((x,y-1))

    if tile1 != 1 and not (x+1,y) in mapa.walls:
        ways.append('d')
    if tile3 != 1 and not (x,y+1) in mapa.walls:
        ways.append('s')
    if tile2 != 1 and not (x-1,y) in mapa.walls:
        ways.append('a')
    if tile4 != 1 and not (x,y-1) in mapa.walls:
        ways.append('w')

    return ways


# retorna distancia entre duas posiçoes
def dist_to(pos1, pos2):
    if len(pos1) != 2 or len(pos1) != 2:
        return ''

<<<<<<< HEAD
def goToPosition(my_pos, next_pos):
    print('goToPosition'.center(50, '-'))
    print('my_pos: ' + str(my_pos))
    print('next_pos: ' + str(next_pos))

    mx,my = my_pos
    nx,ny = next_pos

    res = [nx-mx, ny-my]
    print('res: ' + str(res))
    return getKey(res)

def choose_key(mapa, ways, my_pos, positions, goal, last_pos_wanted):
    # já sabe o caminho
    if positions != []:
        while my_pos == positions[0]:
            print('my_pos == next_pos')
            positions.pop(0)

        key = goToPosition(my_pos, positions[0])
        positions.pop(0)
        return key, positions

    else: # pesquisar caminho
        positions = astar(mapa.map, my_pos, goal, mapa,last_pos_wanted)
        print('positions: ' + str(positions))

        if positions == [] or positions == None:
            print('Caminho nao encontrado...')
            return choose_move(my_pos,ways,goal),[]
            #return ''

        if len(positions) > 1:
            positions.pop(0)


        return goToPosition(my_pos, positions[0]),positions


def choose_key2(mapa, ways, my_pos, positions, wall, oneal, last_pos_wanted):
    # já sabe o caminho

    if positions != []:
        key = goToPosition(my_pos, positions[0])
        positions.pop(0)
        if positions:
            return key,positions[-1]
        else:
            return key,[]

    else:  # pesquisar caminho
        if oneal is not None:
            positions = astar(mapa.map, my_pos, oneal)
            print('positions enemie: ' + str(positions))
            if positions == [] or positions == None:
                positions = astar(mapa.map, my_pos, wall)
                print('positions wall: ' + str(positions))
                if positions == [] or positions == None:
                    print('Caminho nao encontrado...')
                    # return choose_move(my_pos,ways,goal)
                    return choose_random_move(ways),''
                goal = wall
            goal = oneal
        else:
            positions = astar(mapa.map, my_pos, wall)
            print('positions wall: ' + str(positions))
            if positions == [] or positions == None:
                print('Caminho nao encontrado...')
                # return choose_move(my_pos,ways,goal)
                return '', ''
            goal = wall
        if len(positions)>1:
            positions.pop(0)

        if len(positions) <= 1 and last_pos_wanted:
            return choose_move(my_pos, ways, goal),goal

        return goToPosition(my_pos, positions[0]),goal


def choose_key3(mapa, ways, my_pos, positions, wall, oneal, last_pos_wanted):
    # já sabe o caminho

    if positions != []:
        print('Não precisa de pesquisar...')
        print('positions: ' + str(positions))

        if dist_to(my_pos, positions[0]) > 1:
            print("Next_pos invalida!!")
            return choose_move(my_pos, ways, wall), [], wall

        key = goToPosition(my_pos, positions[0])
        goal = positions[-1]
        positions.pop(0)
        return key, positions, goal
        '''
        if positions:
            return key, positions, positions[-1]
        else:
            return key, [], positions[-1]
        '''

    else:  # pesquisar caminho
        # procura caminho para inimigo
        if oneal is not None:
            # procura caminho para o inimigo
            positions = astar(mapa.map, my_pos, oneal, mapa)
            print('positions enemie: ' + str(positions))

            # se nao encontra caminho para o inimigo
            # então procura caminho para a parede
            if positions == [] or positions == None:
                print('Caminho nao encontrado para o inimigo...')
                positions = astar(mapa.map, my_pos, wall, mapa)
                print('positions wall: ' + str(positions))

                # nao encontra caminho para a parede
                if positions == [] or positions == None:
                    print('Caminho nao encontrado para a parede...')
                    # usa outra função para encontrar caminho
                    return choose_move(my_pos, ways, wall), [], wall

                # caminho para parede

                # se a proxima posiçao for igual à minha posiçao atual
                while dist_to(my_pos, positions[0]) == 0:
                    print('my_pos == next_pos')
                    print('apagar posições inuteis')
                    positions.pop(0)

                # positions.pop(0)                # *Problemas*
                return goToPosition(my_pos,positions[0]), positions, positions[-1]
            
            else:
                # caminho para inimigo
                # se a proxima posiçao for igual à minha posiçao atual
                while dist_to(my_pos, positions[0]) == 0:
                    print('my_pos == next_pos')
                    print('apagar posições inuteis')
                    positions.pop(0)

                # positions.pop(0)
                return goToPosition(my_pos, positions[0]), positions, positions[-1]
        

        else: # procura caminho para parede (ja nao ha inimigos)
            positions = astar(mapa.map, my_pos, wall)
            print('positions wall: ' + str(positions))
            
            if positions == [] or positions == None:
                print('Caminho nao encontrado...')
                # return choose_move(my_pos,ways,goal)
                return choose_move(my_pos,ways,wall), [], wall
        
        if len(positions)>1:
            positions.pop(0)

        if len(positions) <= 1 and last_pos_wanted:
            return choose_move(my_pos, ways, wall), positions, wall

        return goToPosition(my_pos, positions[0]), positions, wall
=======
    x1, y1 = pos1
    x2, y2 = pos2
>>>>>>> 70a4e9999c3a70c24959a7705a21855a7aa55d0d

    return math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))
               

# verifica se duas posicoes estao na msm direcao 
def check_same_direction(pos1, pos2):
    if len(pos1) != 2 or len(pos2) != 2:
        return False

    x1, y1 = pos1
    x2, y2 = pos2

    if x1 == x2 or y1 == y2:
        return True

    return False


# calcula e retorna a parede mais proxima (mt ineficiente)
def next_wall(bomberman_pos, walls):
    if walls == []:
        return 

    nwall = walls[0]
    min_cost = dist_to(bomberman_pos, walls[0])
    for wall in walls:
        cost = dist_to(bomberman_pos, wall)
        if cost < min_cost:
            min_cost = cost
            nwall = wall

    return nwall

def in_range(bomberman_pos,raio,obstaculo,mapa):
    cx,cy = bomberman_pos
    if obstaculo == None:
        return False
    bx,by = obstaculo
    
    if by == cy:
        for r in range(raio + 1):
            if mapa.is_stone((bx + r, by)):
                break  # protected by stone to the right
            if (cx, cy) == (bx + r, by):
                return True
        for r in range(raio + 1):
            if mapa.is_stone((bx - r, by)):
                break  # protected by stone to the left 
            if (cx, cy) == (bx - r, by):
                return True
    if bx == cx:
        for r in range(raio + 1):
            if mapa.is_stone((bx, by + r)):
                break  # protected by stone in the bottom
            if (cx, cy) == (bx, by + r):
                return True
        for r in range(raio + 1):
            if mapa.is_stone((bx, by - r)):
                break  # protected by stone in the top
            if (cx, cy) == (bx, by - r):
                return True
    return False

