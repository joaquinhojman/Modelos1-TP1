from operator import itemgetter

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

def ordenar_tiempos_lavados(tiempos_lavado):
    sorted = []
    while (len(tiempos_lavado) != 0):
        longest_lavado = max(tiempos_lavado.items(), key=itemgetter(1))
        sorted.append(longest_lavado[0])
        del tiempos_lavado[longest_lavado[0]]
    return sorted

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
    file = open('solucion.txt', 'w')
    file.writelines((L))
    file.close()

def organizar_lavados():
    cant_prendas, tiempos_lavado, incompatibilidades = leer_archivo('primer_problema.txt')
    lavado = {}
    tiempos_lavados_sorted = ordenar_tiempos_lavados(tiempos_lavado.copy())
    i = 1
    while len(tiempos_lavados_sorted) != 0:
        lavado[i] = [tiempos_lavados_sorted[0]]
        tiempos_lavados_sorted.pop(0)
        for prenda in tiempos_lavados_sorted:
            if not existe_incompatibilidad(prenda, lavado[i], incompatibilidades):
                lavado[i].append(prenda)
                tiempos_lavados_sorted.remove(prenda)
        i += 1
    print(lavado)
    print(calcular_tiempo(lavado, tiempos_lavado))
    escribir_archivo(lavado)

organizar_lavados()