from operator import itemgetter
import networkx as nx

def leer_archivo(archivo):
    cant_prendas = 0
    tiempo_lavado = {}
    incompatibilidades = {}
    file = open(archivo, 'r')
    for line in file.readlines():
        line = line[:-1].split(' ')
        if line[0] == 'c':
            continue
        elif line[0] == 'p':
            cant_prendas = line[2]
        elif line[0] == 'e':
            if line[1] in incompatibilidades:
                incompatibilidades[line[1]].append(line[2])
            else:
                incompatibilidades[line[1]] = [line[2]]
            if line[2] in incompatibilidades:
                incompatibilidades[line[2]].append(line[1])
            else:
                incompatibilidades[line[2]] = [line[1]]
        elif line[0] == 'n':
            tiempo_lavado[line[1]] = int(line[2])
    return cant_prendas, tiempo_lavado, incompatibilidades

#def ordenar_tiempos_lavados(tiempos_lavado):
#    sorted = []
#    while (len(tiempos_lavado) != 0):
#        longest_lavado = max(tiempos_lavado.items(), key=itemgetter(1))
#        sorted.append(longest_lavado[0])
#        del tiempos_lavado[longest_lavado[0]]
#    return sorted
#
#def ordenar_cant_incompatibilidades(incompatibilidades):
#    cant_incompatibilidades = {}
#    for k,v in incompatibilidades.items():
#        cant_incompatibilidades[k] = len(v)
#    sorted = []
#    while (len(cant_incompatibilidades) != 0):
#        longest_lavado = max(cant_incompatibilidades.items(), key=itemgetter(1))
#        sorted.append(longest_lavado[0])
#        del cant_incompatibilidades[longest_lavado[0]]
#    return sorted

def existe_incompatibilidad(prenda, prendas_del_lavado, incompatibilidades):
    for p in prendas_del_lavado:
        if p in incompatibilidades[prenda] or prenda in incompatibilidades[p]:
            return True
    return False

def calcular_tiempo(lavado, tiempos_lavado):
    tiempo_total = 0
    for lavados in lavado.values():
        max_tiempo = 0
        for t in lavados:
            if tiempos_lavado[t] > max_tiempo:
                max_tiempo = tiempos_lavado[t]
        tiempo_total += max_tiempo
    return tiempo_total

def escribir_archivo(lavado):
    L = []
    for k,v in lavado.items():
        for l in v:
            L.append(l + " " + str(k)+"\n")
    # Writing to a file
    file = open('solucion3.txt', 'w')
    file.writelines((L))
    file.close()

#def organizar_lavados():
#    _cant_prendas, tiempos_lavado, incompatibilidades = leer_archivo('primer_problema.txt')
#    lavado = {}
#    #tiempos_lavados_sorted = ordenar_tiempos_lavados(tiempos_lavado.copy())
#    cant_incompatibilidades_sorted = ordenar_cant_incompatibilidades(incompatibilidades.copy())
#    i = 1
#    while len(cant_incompatibilidades_sorted) != 0:
#        lavado[i] = [cant_incompatibilidades_sorted[0]]
#        cant_incompatibilidades_sorted.pop(0)
#        for prenda in cant_incompatibilidades_sorted:
#            if not existe_incompatibilidad(prenda, lavado[i], incompatibilidades):
#                lavado[i].append(prenda)
#                cant_incompatibilidades_sorted.remove(prenda)
#        i += 1
#    print(lavado)
#    print(calcular_tiempo(lavado, tiempos_lavado))
#    escribir_archivo(lavado)
#
#organizar_lavados()

def graph_coloring(incompatibilidades):
    G = nx.Graph(incompatibilidades)
    return nx.coloring.greedy_color(G, strategy='smallest_last')

def buscar_incompatibilidades(lavados, incompatibilidades):
    for lavado in lavados.values():
        for prenda in lavado:
            if existe_incompatibilidad(prenda, lavado, incompatibilidades):
                print("ERROR: HUBIERON INCOMPATIBILIDADES CON EL LAVADO")
                exit(-1)

def listar_lavados(lavado, tiempos_lavado, incompatibilidades):
    lavado_items = {}
    for k,v in lavado.items():
        if v in lavado_items.keys():
            lavado_items[v].append(k)
        else:
            lavado_items[v] = [k]
    buscar_incompatibilidades(lavado_items, incompatibilidades)
    #print(lavado_items)
    return lavado_items

def organizar_lavados_2():
    _cant_prendas, tiempos_lavado, incompatibilidades = leer_archivo('segundo_problema.txt')
    lavados_dicc = graph_coloring(incompatibilidades)
    lavados = listar_lavados(lavados_dicc, tiempos_lavado, incompatibilidades)
    print(calcular_tiempo(lavados, tiempos_lavado))
    escribir_archivo(lavados)

organizar_lavados_2()