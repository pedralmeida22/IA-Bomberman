from game import Bomb
from mapa import Map
import math
import random
from Node import *

# IMPLEMENTAR
# para parede pesquisa 1x
# para inimigos pesquisa todas as iterações

def vector2dir(vx, vy):
    m = max(abs(vx), abs(vy))
    if m == abs(vx):
        if vx < 0:
            d = 'a'  # 'a'
        else:
            d = 'd'  # 'd'
    else:
        if vy > 0:
            d = 's'  # s
        else:
            d = 'w'  # w
    return d
    

def goto(origem, destino):
    if len(origem) != 2 or len(destino) != 2:
        return ''

    ox, oy = origem
    dx, dy = destino

    return vector2dir(dx - ox, dy - oy)

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

# da lista de possiveis caminhos escolhe o primeiro caminho
def choose_random_move(ways):
    if len(ways) != []:
        return random.choice(ways)

def choose_move(my_pos, ways, goal):
    if len(ways) == 0:
        return ''

    mx, my = my_pos
    
    custo_min = []

    if 'a' in ways:
        custo_min.append(('a', dist_to([mx-1, my], goal)))        
    if 's' in ways:
        custo_min.append(('s', dist_to([mx, my+1], goal)))
    if 'd' in ways:
        custo_min.append(('d', dist_to([mx+1, my], goal)))
    if 'w' in ways:
        custo_min.append(('w', dist_to([mx, my-1], goal)))

    custo_min.sort(key= lambda x: x[1]) # ordenar por custo (distancia)

    return custo_min[0][0]

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
        positions = astar(mapa.map, my_pos, goal, mapa)
        print('positions: ' + str(positions))

        if positions == [] or positions == None:
            print('Caminho nao encontrado...')
            return choose_move(my_pos,ways,goal),[]
            #return ''

        if len(positions) > 1:
            positions.pop(0)

        if len(positions) <= 1 and last_pos_wanted:
            return choose_move(my_pos, ways, goal),[]

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

               

# dando uma key retorna a sua inversa
def inverse(key):
    if key == 'a':
        return 'd'
    elif key == 'd':
        return 'a'
    elif key == 's':
        return 'w'
    elif key == 'w':
        return 's'

# verifica se duas posicoes estao na msm direcao 
def check_same_direction(pos1, pos2):
    if len(pos1) != 2 or len(pos2) != 2:
        return False

    x1, y1 = pos1
    x2, y2 = pos2

    if x1 == x2 or y1 == y2:
        return True

    return False

# retorna distancia entre duas posiçoes
def dist_to(pos1, pos2):
    if len(pos1) != 2 or len(pos1) != 2:
        return ''

    x1, y1 = pos1
    x2, y2 = pos2

    return math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))

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


def enemie_close(bomberman_pos,enimies,mapa):
    for eni in enimies:
        if in_range(bomberman_pos,1,eni['pos'],mapa):
            return True
    return False
    

def bomb_and_run(bomberman_pos, enemy, range,inimigos,mapa,ways):
        lista=[e for e in inimigos if e['name']== enemy]
        lista.sort(key = lambda x: dist_to(bomberman_pos,x['pos']))
        if in_range(bomberman_pos, range, lista[0]['pos'], mapa):
            print('Enemie close! Pôr bomba!')
            key = 'B'
            ways.append('B')



def choose_hide_pos(bomberman_pos, bomb, mapa, previous_key, n, limit,enemies,detonador):
    x,y = bomberman_pos

    print('limite: ' + str(limit))
    print('n: ' + str(n))

    ord_enemies = closer_enemies(bomberman_pos, enemies)
    print('\n\nord_enemies' + str(ord_enemies))
    #print("enemie close: ",ord_enemies[0])
    if detonador:
        raio = 1
    else:
        raio = 4

    if not in_range(bomberman_pos, bomb[2], bomb[0], mapa) and not in_range(bomberman_pos,raio, ord_enemies[0][1], mapa):
        print("Posicao segura!")
        return (bomberman_pos, True)


    if n == limit:
        print('\n\n\n\nLimite recursivo...')
        if bomberman_pos != bomb:
            print('Posicao encontrada nao é segura!')
            return (bomb[0], False)
        else:
            return ([1,1], False)

    ways = get_possible_ways(mapa, bomberman_pos)
    #print(repr(mapa.map))
    print("DEBUG: ways: " + repr(ways) + ", prev: " + previous_key)

    if previous_key in ['a', 'd']: # andou para o lado, experimenta para o cima/baixo
        print("andou para lado ckecking cima")
        if 'w' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou para lado resultou cima")
            return choose_hide_pos([x, y - 1], bomb, mapa, 'w', n + 1, limit,enemies,detonador)
        print("andou para lado ckecking baixo")
        if 's' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou para lado resultou baixo")
            return choose_hide_pos([x,y+1], bomb, mapa, 's', n+1, limit,enemies,detonador)

    if previous_key in ['w', 's']: # andou na vertical, experimenta para os lados
        print("andou na vertical  ckecking direita")
        if 'd' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou na vertical  resultou direita")
            return choose_hide_pos([x + 1, y], bomb, mapa, 'd', n+1, limit,enemies,detonador)
        print("andou na vertical  ckecking esquerda")
        if 'a' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou na vertical resultou esquerda")
            return choose_hide_pos([x - 1, y], bomb, mapa, 'a', n + 1, limit,enemies,detonador)
            
    print("checking direita")
    if 'd' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou direita")
        return choose_hide_pos([x + 1, y], bomb, mapa, 'd', n+1, limit,enemies,detonador)
    print("checking cima")
    if 'w' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou cima")
        return choose_hide_pos([x, y - 1], bomb, mapa, 'w', n + 1, limit,enemies,detonador)
    print("checking esquerda")
    if 'a' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou esquerda")
        return choose_hide_pos([x - 1, y], bomb, mapa, 'a', n + 1, limit,enemies,detonador)
    print("checking baixo")
    if 's' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou baixo")
        return choose_hide_pos([x, y + 1], bomb, mapa, 's', n+1, limit,enemies,detonador)

    
    else:
        return bomberman_pos,False




def choose_hide_pos2(bomberman_pos, bomb, mapa, previous_key, n, limit,enemies,detonador):
    x,y = bomberman_pos

    print('limite: ' + str(limit))
    print('n: ' + str(n))
    ord_enemies = closer_enemies(bomberman_pos, enemies)
    print('\n\nord_enemies' + str(ord_enemies))
    #print("enemie close: ", ord_enemies[0])

    if detonador:
        raio = 1
    else:
        raio = 4

    if not in_range(bomberman_pos, bomb[2], bomb[0], mapa)and not in_range(bomberman_pos,raio, ord_enemies[0][1], mapa) :
        print("Posicao segura!")
        return (bomberman_pos, True)

    if n == limit:
        print('\n\n\n\nLimite recursivo...going to 2 recursive')
        return choose_hide_pos(bomberman_pos,bomb,mapa,'',0,70,enemies,detonador)

    ways = get_possible_ways(mapa, bomberman_pos)
    #print(repr(mapa.map))
    print("DEBUG: ways: " + repr(ways) + ", prev: " + previous_key)

    if previous_key in ['a', 'd']: # andou para o lado, experimenta para o cima/baixo
        print("andou para lado ckecking baixo")
        if 's' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou para lado resultou baixo")           
            return choose_hide_pos2([x,y+1], bomb, mapa, 's', n+1, limit,enemies,detonador)
        print("andou para lado ckecking cima")
        if 'w' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou para lado resultou cima")
            return choose_hide_pos2([x, y - 1], bomb, mapa, 'w', n+1, limit,enemies,detonador)

    if previous_key in ['w', 's']: # andou na vertical, experimenta para os lados
        print("andou na vertical  ckecking esquerda")
        if 'a' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou na vertical resultou esquerda")
            return choose_hide_pos2([x-1,y], bomb, mapa, 'a', n+1, limit,enemies,detonador)
        print("andou na vertical  ckecking direita")
        if 'd' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
            print("andou na vertical  resultou direita")
            return choose_hide_pos2([x + 1, y], bomb, mapa, 'd', n+1, limit, enemies,detonador)

    print("checking baixo")
    if 's' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou baixo")
        return choose_hide_pos2([x, y + 1], bomb, mapa, 's', n+1, limit,enemies,detonador)
    print("checking cima")
    if 'w' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou cima")
        return choose_hide_pos2([x, y - 1], bomb, mapa, 'w', n+1, limit,enemies,detonador)
    print("checking esquerda")
    if 'a' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou esquerda")
        return choose_hide_pos2([x-1,y], bomb, mapa, 'a', n+1, limit,enemies,detonador)
    print("checking direita")
    if 'd' in ways and not in_range(bomberman_pos,0, ord_enemies[0][1], mapa):
        print("resultou direita")
        return choose_hide_pos2([x + 1, y], bomb, mapa, 'd', n+1, limit,enemies,detonador)
    else:
        return choose_hide_pos(bomb[0],bomb,mapa,previous_key,n+1,limit,enemies,detonador)


#Verifica o mais perto   ---> A funcionar
def closer_enemies(my_pos,lista):
    lista1=[]
    if lista == []:
        return [(None,None)]

    for i in range(len(lista)):
        coor=lista[i]['pos']
        lista1.append([dist_to(my_pos,lista[i]['pos']),lista[i]['pos']])

        #Guarda uma lista de tuplos (id e distancia), ordenada por distancias
    lista1.sort(key=lambda x: x[0])  # ordenar por custo (distancia)
    #print (lista1)

    return lista1



#evita os inimigos
def avoid(my_pos,en_pos,mapa):

    # if en_pos[0] == my_pos[0]:
    #     if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] - 1]):  # Bomberman para baixo
    #         print("BAIXO")
    #         return 's'
    #     else:
    #         print("CIMA")
    #         return 'w'
    #
    # elif en_pos[1]==mu


    if en_pos[0]>my_pos[0]:                                             #Inimigo à direita
        if not Map.is_blocked(mapa,[my_pos[0]-1,my_pos[1]]):                       #BOmberman vai à esquerda
            print("ESQUERDA")
            return 'a'
        else:                                                           #Pedra à esquerda
            if en_pos[1]>my_pos[1]:                                     #Inimigo abaixo
                if not Map.is_blocked(mapa,[my_pos[0], my_pos[1]-1]):              #Bomberman para cima
                    print("CIMA")
                    return 'w'
            elif en_pos[1] < my_pos[1]:  # Inimigo acima
                if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] + 1]):  # Bomberman para baixo
                    print("BAIXO")
                    return 's'
                else:
                    print("rip")

            else:                                                       # INIMIGO NO MESMO NIVEL
                if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] - 1]):  # Bomberman para cima
                    print("CIMA")
                    return 'w'
                else:
                    print("BAIXO")
                    return 's'


    elif en_pos[0]<my_pos[0]:                                                               #Inimigo à esquerda
        if not Map.is_blocked(mapa,[my_pos[0] + 1, my_pos[1]]):  # BOmberman vai à direita
            print("DIREITA")
            return 'd'
        else:                                                   # Pedra à direita
            if en_pos[1] > my_pos[1]:  # Inimigo abaixo
                if not Map.is_blocked(mapa,[my_pos[0], my_pos[1] - 1]):  # Bomberman para cima
                    print("CIMA")
                    return 'w'
                else:
                    print("rip")
                    return ''

            elif en_pos[1] < my_pos[1]:
                if not Map.is_blocked(mapa,[my_pos[0], my_pos[1] + 1]):  # Bomberman para baixo
                    print("BAIXO")
                    return 's'
                else:
                    print("rip")
                    return ''


            else:  # Inimigo NO MESMO NIVEL
                if not Map.is_blocked(mapa,[my_pos[0], my_pos[1] - 1]):  # Bomberman para cima
                    print("CIMA")
                    return 'w'
                else:
                    print("BAIXO")
                    return 's'


    else:                                                               #INIMIGO EM LINHA
        if en_pos[1] > my_pos[1]:  # Inimigo acima
            if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] - 1]):  # Bomberman para cima
                print("CIMA")
                return 'w'
            else:
                print("rip")
                return ''

        elif en_pos[1] < my_pos[1]:
            if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] +  1]):  # Bomberman para baixo
                print("BAIXO")
                return 's'
            else:
                print("rip")
                return ''


        else:  # Inimigo NO MESMO NIVEL
            if not Map.is_blocked(mapa, [my_pos[0], my_pos[1] - 1]):  # Bomberman para cima
                print("CIMA")
                return 'w'
            else:
                print("BAIXO")
                return 's'




