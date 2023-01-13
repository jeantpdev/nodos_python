from cmath import exp
import os  # Necesario para poder usar comandos del CMD/Powershell
import json  # Necesario para manipular JSON dentro de python

graph = {}  # Diccionario donde se guardarán todos los grafos
historial = []  # Variable usada para crear la lista del archivo.json

nodo_conexiones = [] # En este diccionario se almacenaran todas las conexiones que tendrán los nodos

def validar_campo_de_texto(pregunta):
    tiene_errores = True
    while tiene_errores == True:
        print(pregunta)
        respuesta = input("escribe tu respuesta\n")
        if len(respuesta) <= 0:
            print("El campo no puede estar vacío")
            tiene_errores = True
        elif respuesta.isnumeric():
            print("El campo no puede ser un número")
            tiene_errores = True
        else:
            tiene_errores = False
            return respuesta

#Menu inicial del programa
def menu_inicio():

    while True:
        try:
            opc = int(input("\
                \n1. Inicio del programa\
                \n2. Consulta de rutas\
                \n3. Salir del programa\n"))

            if opc == 1:
                pregunta = "¿Cómo te llamas?"
                nombre = validar_campo_de_texto(pregunta)
                id_usuario = asignar_id()

                print("Bienvenido {} tu id es {} ".format(nombre, id_usuario))
                cantidad_nodos = crear_nodos()
                conectar_nodos(cantidad_nodos)

                vi = input("Digite el nodo inicial del recorrido\n").upper()
                vf = input("Digite el nodo final del recorrido\n").upper()

                ruta = list(dfs_paths(graph, vi, vf))
                ruta_larga = ruta_mas_larga(ruta)
                ruta_corta = ruta_mas_corta(ruta)
                print(ruta)
                crear_historial_json(nombre, cantidad_nodos,vi, vf, ruta, id_usuario, ruta_larga, ruta_corta)
                graph.clear()

            if opc == 2:
                print("Opción 2: Consulta de rutas")
                while True:
                    try:
                        opc2 = int(input("1. Mostrar todos los registros del JSON\
                                        \n2. Mostrar un registro por ID\
                                        \n3. Regresar\n"))
                    except ValueError:
                        print("Tienes que elegir una de las opciones enumeradas")
                    if opc2 == 1:
                        consulta_rutas_json()
                    if opc2 == 2:
                        buscar_id = int(input("¿Numero de ID a buscar?\n"))
                        mostrar_json_id(buscar_id)
                    if opc2 == 3:    
                        break

            if opc == 3:
                os.system('cls')
                print("Has salido del programa")
                break

        except ValueError:
            os.system('cls')
            print("Elige una de las opciones enumeradas")

#Funcion para crear la cantidad de nodos que existirán
def crear_nodos():
    while True:
        try:
            cantidad_nodos = int(input("Digite la cantidad de nodos\n"))
            if cantidad_nodos < 2:
                os.system('cls')
                print("Tienes que agregar mas de 1 nodo")
            else:
                while True:
                    try:
                        opc = validar_campo_texto(input("¿Estás seguro que agregarás {} nodos?\
                            \n1. Si\
                            \n2.No\nRecuerda escribir Si o No\n".format(cantidad_nodos)))
                        
                    except ValueError:
                        os.system('cls')
                        print("Tienes que digitar una de las opciones listadas")
                        continue
                    
                    if opc == True:
                        return cantidad_nodos
                    if opc == False:
                        print("Tienes que escribir Si o No")
        except ValueError as e:
            os.system('cls')
            print("Tienes que escribir la cantidad en números")

#Función que conecta los nodos entre sí
def conectar_nodos(cantidad_nodos): 
    try:
        for i in range(cantidad_nodos):
            while True:
                print("Nodo actual "+str(i+1)+" de "+str(cantidad_nodos))
                nodo = input("Digite el nombre del nodo en mayuscula "+str("    ")).upper()         
                if comprobar_existencia_nodo(nodo,graph) == True:
                    print(graph)
                    print("No puedes crear el mismo nodo otra vez")
                elif comprobar_existencia_nodo(nodo,graph) == False:
                    if len(nodo) < 1:
                        print("Escribe el nombre del nodo")
                    else:
                        configurar_nodos(nodo)
                        graph.update({nodo: set(nodo_conexiones)})
                        nodo_conexiones.clear()
                        print(graph)
                        break
    except ValueError:
        print("Tienes que escribir el nodo")

#Funcion par agregar o quitar nodos en caso de equivocación
def configurar_nodos(nodo):
    while True: 
        try:
            print(nodo+str(nodo_conexiones))
            rpta = int(input("Elige una de las opciones\
                \n1.Agregar conexion de nodo\
                \n2.No agregar conexion de nodo\
                \n3.Eliminar camino de nodo\n"))

            if rpta == 1: 
                print(nodo+str(nodo_conexiones))
                while True:
                    try:
                        nodo_unir = input("¿Con quién conecta el nodo "+nodo+"?\n")
                        if nodo_unir == nodo:
                            print("No puedes conectar {} con el nodo {} ".format(nodo_unir, nodo))
                        elif nodo_unir in nodo_conexiones:
                            print("El nodo ya existe")
                        elif nodo_unir == "":
                            print("El campo no puede estar vacío")
                        else:
                            nodo_conexiones.append(nodo_unir)
                            break
                    except:
                        continue
            elif rpta == 2:
                 if nodo_unir == "":
                    print("El campo no puede estar vacio")
                 else:
                    break   

    
            elif rpta == 3:  
                if not nodo_conexiones:
                    print("\nLa lista está vacía\n")

                else:
                    print(nodo+str(nodo_conexiones))
                    quitar = input("Escribe el que deseas quitar\n").upper()

                    if quitar in nodo_conexiones:
                        nodo_conexiones.remove(quitar)
                        print("Se ha eliminado el nodo "+quitar+"\n")

                    else:
                        print(quitar+" no existe en el nodo ")
            
            else:
                print("Tienes que elegir una de las opciones listadas\n")

        except:
            print("\nEl campo no puede estar vacío\n")

#Función que devuelve el recorrido de los grafos desde su variable inicial hasta su variable final
def dfs_paths(graph, start, goal):
    # Define stack variable
    stack = [[start]]
    # Do the process while there are paths to follow
    while stack:
        path = stack.pop()
        node = path[-1]
        for next in graph[node] - set(path):
            # If a correct path is founded, then return the path with the generator
            # else write a new path and follow iterating.
            if next == goal:
                yield path + [next]
            else:
                stack.append(path + [next])

#Función que detecta cuál fue la ruta mas recorrida
def ruta_mas_larga(ruta):
    tamano_ruta = 0
    indice_en_lista_recibida = 0
    ruta_larga = []
    for diccionarios_en_lista in range(len(ruta)):
        if tamano_ruta < len(ruta[diccionarios_en_lista]):
            tamano_ruta = len(ruta[diccionarios_en_lista])
            indice_en_lista_recibida = diccionarios_en_lista
    ruta_larga = ruta[indice_en_lista_recibida]
    return ruta_larga 

#Funcion que detecta cual fue la ruta menos recorrida
def ruta_mas_corta(ruta):
    tamano_ruta = 0
    indice_en_lista_recibida = 0
    ruta_corta = []
    for diccionarios_en_lista in range(len(ruta)):
        if  tamano_ruta > len(ruta[diccionarios_en_lista]):
            tamano_ruta = len(ruta[diccionarios_en_lista])
            indice_en_lista_recibida = diccionarios_en_lista   
    ruta_corta = ruta[indice_en_lista_recibida]
    return ruta_corta

#Funcion que se enecarga de crear un historial en formato json
def crear_historial_json(nombre, cantidad_nodos, vi, vf, ruta, id_usuario, ruta_larga, ruta_corta):
    if existe_historial() == True:
        nuevos_datos = diccionario_datos(id_usuario, nombre, cantidad_nodos, vi, vf, ruta, ruta_larga, ruta_corta)
        with open("historial.json") as archivo_json:
            datos = json.load(archivo_json)
        datos.append(nuevos_datos)

        with open("historial.json", 'w') as archivo_json:
            json.dump(datos, archivo_json, indent=3)
            print("Se han añadido los siguientes datos al archivo " + \
                  archivo_json.name+"\n")
            print(nuevos_datos)
    else:
        with open("historial.json", 'w') as archivo_json:
            historial.append(diccionario_datos(id_usuario, nombre, cantidad_nodos, vi, vf, ruta, ruta_larga, ruta_corta))
            json.dump(historial, archivo_json, indent=3)
            print(archivo_json.name+" creado exitosamente")
            print("Se han añadido los siguientes datos al archivo " + \
                  archivo_json.name+"\n")
            print(historial)

#Funcion que consulta las rutas del archivo historial.json y las muestra en consola
def consulta_rutas_json():
    if existe_historial() == True:
        with open("historial.json") as archivo_json:
            datos = json.load(archivo_json)
        json_formateado = json.dumps(datos, indent= 3)
        return print(str(json_formateado))

#Funcion encaragda de buscar dentro del historial, un ID y mostrar los resutlados que contenga
def mostrar_json_id(id):
    if existe_historial() == True:
        with open("historial.json") as archivo_json:
            datos = json.load(archivo_json)
            try:
                v = [x for x in datos if x['Id'] == id]
                print("\n")
                if len(v) == 0:
                    print("No existe ese id")
                else:
                    print(v)
            except:
                print("No existe registro")
    else:
        print("No existe el historial.json")                

#Funcion que comprueba que no se repita un nodo
def comprobar_existencia_nodo(nodo,graph):
    list = [elementos for elementos in graph.keys()]
    if nodo in list:
        return True
    else:
        return False
    
#Funcion encargada de leer una entrada por consola y validar que sea un texto
def validar_campo_texto(opc):
    lista_si = ['si','sí','Si','Sí','sI', 'SI', 'SÍ','sÍ']
    
    if opc.isnumeric():
        print("Tienes que escribir la cantidad en números")
    elif len(opc) <= 0:
        print("El campo no puede estar vacío")    
    elif opc in lista_si:
        return True
    else:
        return False
    
#Funcion que se encarga de verificar si existe un historial en formato JSON devolviendo True sí existe o False si no existe  
def existe_historial():
    try:
        with open('historial.json') as archivo:
            return True
    except FileNotFoundError as e:
        return False

#Funcion que sirve para añadir datos que se le introduzcan dentro de un diccionario
def diccionario_datos(id_usuario, nombre, cantidad_nodos, vi, vf, ruta, ruta_larga, ruta_corta):
    diccionario_nuevo = {
        'Id': id_usuario, 
        'Usuario': nombre, 
        'Cantidad_nodos': cantidad_nodos, 
        'Nodo_vi': vi, 
        'Nodo_vf': vf, 
        'Rutas': ruta, 
        'Ruta mas recorrida': ruta_larga,
        'Ruta menos recorrida': ruta_corta}
    return diccionario_nuevo

#Funcion que asigna ID al usuario dependiendo de la cantidad de registros que haya en el historial.json
def asignar_id():
    if existe_historial() == True:
        with open("historial.json") as archivo_json:
            datos = json.load(archivo_json)
            return len(datos) + 1
    else:
        return 1
    
if __name__ == "__main__":
    # Inicio del programa
    menu_inicio()