import vars
import requests
import json
import os.path
import xlwt
from xlwt import Workbook
import StatsJugadorIndividualClass
import TeamClass
import MatchClass
from datetime import datetime
from time import sleep

#FUNCIÓN QUE DADA LA ID DE UN GAME HACE UN QUERY A LA API DE RIOT Y LO GUARDA EN UN DOCUMENTO JSON.
#PRIMERO COMPRUEBA SI YA SE HA BUSCADO ESE MATCH PARA EVITAR QUERYS EXTRAS A RIOT.
#DEVUELVE LA RUTA DONDE SE ENCUENTRA EL ARCHIVO
def obtenerMatch(idMatch):
    #ruta donde guardaremos el archivo
    rutaGuardar = vars.directorioMatches + str(idMatch) + ".json"
    #Vemos si ya existe el archivo, si es así no hacemos nada.
    if (os.path.isfile(rutaGuardar)):
        pass
    else:
        print ("Generando query y guardando match")
        #Crea el query
        query = vars.matchRequest + str(idMatch) + vars.referenciaKey + vars.apiKey
        #Hace el query y lo guarda en la VAR match
        match = requests.get(query)
        #Comprueba si el query se hizo correctamente
        if (str(match) == "<Response [200]>"):
            print ("Petición enviada a RIOT API. Se pudo hacer el QUERY correctamente",match)
        else:
            print("No se pudo hacer el query. ERROR:", match)
        #guardar archivo JSON
        with open(rutaGuardar, "w") as outfile:
            json.dump(match.json(),outfile)
    return rutaGuardar

#FUNCIÓN QUE DADA LA ID DE UN MATCH Y EL NUMERO DE PARTICIPANTE DEVUELVE UNA LISTA CON LOS STATS DE DICHO PARTICIPANTE
#Cada partida tiene 10 participantes.
#HACE USO DE LA FUNCIÓN idMatch PARA GENERAR EL QUERY A RIOT Y OBTENER LA RUTA DEL MATCH.JSON
def obtenerStatsIndividualMatch(idMatch, participant):
    #Leemos el match file y se lo asignamos a la VAR contenido
    with open(obtenerMatch(idMatch)) as json_file:
        contenido = json.load(json_file)
    #La VAR stats guarda los stats del participante en formato json
    #el -1 es porque participante 1 es en Python participante 0, participante 2 es 1... por eso de que el primer elemento siempre es el 0 :D
    stats = contenido["participants"][participant-1]["stats"]

    #Asignamos cada valor del archivo a un atributo del objeto statsJugador.
    CSmin0_10 = '0'
    creeps10_20 = '0'

    #Debemos hacer esto porque si el game dura menos de 10 minutos no existe creepsPerMinDeltas0_10 y si dura menos de 20, no existe creepsPerMinDeltas10_20
    if contenido["gameDuration"]/60.0 > 10.0:
        CSmin0_10 = contenido["participants"][participant - 1]["timeline"]["creepsPerMinDeltas"]["0-10"]

    if contenido["gameDuration"] / 60.0 > 20.0:
        creeps10_20 = contenido["participants"][participant - 1]["timeline"]["creepsPerMinDeltas"]["10-20"]

    splayer = StatsJugadorIndividualClass.statsJugador(idMatch, contenido["gameCreation"], contenido["participants"][participant - 1]["timeline"]["lane"],
                                                       contenido["gameDuration"], contenido["participants"][participant-1]["championId"], stats["kills"],
                                                       stats["deaths"], stats["assists"], stats["totalDamageDealtToChampions"],stats["totalDamageTaken"],
                                                       stats["totalHeal"], stats["totalTimeCrowdControlDealt"], stats["visionScore"], stats["visionWardsBoughtInGame"],
                                                       stats["wardsPlaced"], stats ["wardsKilled"], stats["goldEarned"], stats ["totalMinionsKilled"],
                                                       stats["neutralMinionsKilledTeamJungle"], stats["neutralMinionsKilledEnemyJungle"],
                                                       CSmin0_10,
                                                       creeps10_20,
                                                       stats["damageDealtToObjectives"], stats["damageDealtToTurrets"], stats["turretKills"], stats["inhibitorKills"],
                                                       contenido["participants"][participant - 1]["timeline"]["role"])


    #Devuelve un objeto que contiene los stats del jugado en el match
    return splayer

#################################
###Con esta función analizamos una partida entera, analizando cada jugador.
###Cada jugador es asignador a un objeto TEAM, que tambien reune estadisticas de la partida (firts Herald, numero de dragones, torres...)
def analisisTeams(idMatch):
    #Sacamos cada jugador del match.
    player1 = obtenerStatsIndividualMatch(idMatch, 1)
    player2 = obtenerStatsIndividualMatch(idMatch, 2)
    player3 = obtenerStatsIndividualMatch(idMatch, 3)
    player4 = obtenerStatsIndividualMatch(idMatch, 4)
    player5 = obtenerStatsIndividualMatch(idMatch, 5)
    player6 = obtenerStatsIndividualMatch(idMatch, 6)
    player7 = obtenerStatsIndividualMatch(idMatch, 7)
    player8 = obtenerStatsIndividualMatch(idMatch, 8)
    player9 = obtenerStatsIndividualMatch(idMatch, 9)
    player10 = obtenerStatsIndividualMatch(idMatch, 10)

    #Obtenemos detalles de la partida y se lo asignamos al equipo Blue
    with open(obtenerMatch(idMatch)) as json_file:
        partida= json.load(json_file)
    blueTeamWin = partida["teams"][0]["win"]
    blueTeamfirstBlood= partida["teams"][0]["firstBlood"]
    blueTeamfirstTower = partida["teams"][0]["firstTower"]
    blueTeamfirstInhibitor = partida["teams"][0]["firstInhibitor"]
    blueTeamfirstBaron = partida["teams"][0]["firstBaron"]
    blueTeamfirstDragon = partida["teams"][0]["firstDragon"]
    blueTeamfirstRiftHerald = partida["teams"][0]["firstRiftHerald"]
    blueTeamtowerKills = partida["teams"][0]["towerKills"]
    blueTeaminhibitorKills = partida["teams"][0]["inhibitorKills"]
    blueTeambaronKills = partida["teams"][0]["baronKills"]
    blueTeamdragonKills = partida["teams"][0]["dragonKills"]
    blueTeamriftHeraldKills = partida["teams"][0]["riftHeraldKills"]

    blueTeambans = [partida["teams"][0]["bans"][0]["championId"], partida["teams"][0]["bans"][1]["championId"],partida["teams"][0]["bans"][2]["championId"],
                    partida["teams"][0]["bans"][3]["championId"], partida["teams"][0]["bans"][4]["championId"]]

    #Y lo asignamos al objeto Team
    blueTeam = TeamClass.teamStats(idMatch, "Blue Team", blueTeamWin, blueTeamfirstBlood,blueTeamfirstTower,blueTeamfirstInhibitor,blueTeamfirstBaron,
                                   blueTeamfirstDragon,blueTeamfirstRiftHerald,blueTeamtowerKills,blueTeaminhibitorKills,blueTeambaronKills,blueTeamdragonKills,
                                   blueTeamriftHeraldKills, player1, player2, player3, player4, player5, blueTeambans)

    # Obtenemos detalles de la partida y se lo asignamos al equipo Red
    redTeamWin = partida["teams"][1]["win"]
    redTeamfirstBlood= partida["teams"][1]["firstBlood"]
    redTeamfirstTower = partida["teams"][1]["firstTower"]
    redTeamfirstInhibitor = partida["teams"][1]["firstInhibitor"]
    redTeamfirstBaron = partida["teams"][1]["firstBaron"]
    redTeamfirstDragon = partida["teams"][1]["firstDragon"]
    redTeamfirstRiftHerald = partida["teams"][1]["firstRiftHerald"]
    redTeamtowerKills = partida["teams"][1]["towerKills"]
    redTeaminhibitorKills = partida["teams"][1]["inhibitorKills"]
    redTeambaronKills = partida["teams"][1]["baronKills"]
    redTeamdragonKills = partida["teams"][1]["dragonKills"]
    redTeamriftHeraldKills = partida["teams"][1]["riftHeraldKills"]

    redTeambans = [partida["teams"][1]["bans"][0]["championId"], partida["teams"][1]["bans"][1]["championId"],partida["teams"][1]["bans"][2]["championId"],
                    partida["teams"][1]["bans"][3]["championId"], partida["teams"][1]["bans"][4]["championId"]]

    # Y lo asignamos al objeto Team
    redTeam = TeamClass.teamStats(idMatch, "Red Team", redTeamWin, redTeamfirstBlood, redTeamfirstTower,
                                   redTeamfirstInhibitor, redTeamfirstBaron,
                                   redTeamfirstDragon, redTeamfirstRiftHerald, redTeamtowerKills,
                                   redTeaminhibitorKills, redTeambaronKills, redTeamdragonKills,
                                   redTeamriftHeraldKills, player6, player7, player8, player9, player10,redTeambans)


    return blueTeam, redTeam


#Crea el objeto match (compuesto de teams [que a su vez compuesto de players] e información del match)
#0 decimos que Blue team es el nuestro, 1 que Red team es el nuestro
def analisisMatch(idMatch, nombreMatch,  num):
    blueTeam, redTeam = analisisTeams(idMatch)
    partida = MatchClass.match(idMatch, nombreMatch, num, blueTeam, redTeam)
    return partida

##############################

#Funciones para generar los excels

##############################

#Crea listas de los equipos y los jugadores de un match para luego pasar estas a la función que escribe el excel
def listasExcel(partida):
    #Usamos la funcion interna de TeamClass para ordenar a los players de Top a Support.
    p1List = creaListaPlayer(partida.blueTeam.ordenarPlayers()[0])
    p2List = creaListaPlayer(partida.blueTeam.ordenarPlayers()[1])
    p3List = creaListaPlayer(partida.blueTeam.ordenarPlayers()[2])
    p4List = creaListaPlayer(partida.blueTeam.ordenarPlayers()[3])
    p5List = creaListaPlayer(partida.blueTeam.ordenarPlayers()[4])

    p6List = creaListaPlayer(partida.redTeam.ordenarPlayers()[0])
    p7List = creaListaPlayer(partida.redTeam.ordenarPlayers()[1])
    p8List = creaListaPlayer(partida.redTeam.ordenarPlayers()[2])
    p9List = creaListaPlayer(partida.redTeam.ordenarPlayers()[3])
    p10List = creaListaPlayer(partida.redTeam.ordenarPlayers()[4])

    t1List, t2List = creaListaTeam(partida)

    #Devuelve primero stats de cada equipo, luego dos variables sobre quien es nuestro equipo, y por ultimo los 10 players
    return [t1List, t2List, p1List ,p2List,p3List,p4List,p5List,p6List,p7List,p8List,p9List,p10List]

#Funcion auxiliar que extrae las variables del objeto StatsJugador y los mete en  una lista que devuelve.
def creaListaPlayer(player):
    lStats = []
    lStats.append(player.lane)
    lStats.append(player.campeon)
    lStats.append(player.kills)
    lStats.append(player.deaths)
    lStats.append(player.assists)
    lStats.append(player.totalDamageDealtToChampions)
    lStats.append(player.totalDamageTaken)
    lStats.append(player.goldEarned)
    lStats.append(player.totalMinionsKilled)
    lStats.append(player.neutralMinionsKilledTeamJungle)
    lStats.append(player.neutralMinionsKilledEnemyJungle)
    lStats.append(player.creepsMin0_10)
    lStats.append(player.creepsMin10_20)
    lStats.append(player.creepsporMinuto)
    lStats.append(player.visionScore)
    lStats.append(player.visionWardsBoughtInGame)
    lStats.append(player.wardsPlaced)
    lStats.append(player.wardsKilled)
    lStats.append(player.damageDealtToObjectives)
    lStats.append(player.damageDealtToTurrets)
    lStats.append(player.turretKills)
    lStats.append(player.inhibitorKills)
    lStats.append(player.totalHeal)
    lStats.append(player.totalTimeCrowdControlDealt)
    return lStats


#Funcion auxiliar que extrae las variables del objeto TeamClass y los mete en  una lista que devuelve. Debe ser un objeto MatchClass, no puede ser el numero de match.
def creaListaTeam(partida):
    #Creando Lista de BlueTeam
    lStatsTeam = []
    lStatsTeam.append(partida.blueTeam.player1.fecha)
    lStatsTeam.append(partida.blueTeam.nombre)
    if (partida.blueSide):
        lStatsTeam.append(vars.team)
    else:
        lStatsTeam.append("Rival")
    lStatsTeam.append(partida.blueTeam.win)
    lStatsTeam.append(partida.blueTeam.player1.gameDuration)
    lStatsTeam.append(partida.blueTeam.picks()[1])
    lStatsTeam.append(partida.blueTeam.bansList()[1])
    lStatsTeam.append(partida.blueTeam.towerKills)
    lStatsTeam.append(partida.blueTeam.inhibitorKills)
    lStatsTeam.append(partida.blueTeam.baronKills)
    lStatsTeam.append(partida.blueTeam.dragonKills)
    lStatsTeam.append(partida.blueTeam.riftHeraldKills)
    lStatsTeam.append(partida.blueTeam.firstBlood)
    lStatsTeam.append(partida.blueTeam.firstTower)
    lStatsTeam.append(partida.blueTeam.firstInhibitor)
    lStatsTeam.append(partida.blueTeam.firstBaron)
    lStatsTeam.append(partida.blueTeam.firstDragon)
    lStatsTeam.append(partida.blueTeam.firstRiftHerald)

    # Creando Lista de RedTeam
    lStatsTeam2 = []
    lStatsTeam2.append(partida.redTeam.player1.fecha)
    lStatsTeam2.append(partida.redTeam.nombre)
    if (partida.redSide):
        lStatsTeam2.append(vars.team)
    else:
        lStatsTeam2.append("Rival")
    lStatsTeam2.append(partida.redTeam.win)
    lStatsTeam2.append(partida.redTeam.player1.gameDuration)
    lStatsTeam2.append(partida.redTeam.picks()[1])
    lStatsTeam2.append(partida.redTeam.bansList()[1])
    lStatsTeam2.append(partida.redTeam.towerKills)
    lStatsTeam2.append(partida.redTeam.inhibitorKills)
    lStatsTeam2.append(partida.redTeam.baronKills)
    lStatsTeam2.append(partida.redTeam.dragonKills)
    lStatsTeam2.append(partida.redTeam.riftHeraldKills)
    lStatsTeam2.append(partida.redTeam.firstBlood)
    lStatsTeam2.append(partida.redTeam.firstTower)
    lStatsTeam2.append(partida.redTeam.firstInhibitor)
    lStatsTeam2.append(partida.redTeam.firstBaron)
    lStatsTeam2.append(partida.redTeam.firstDragon)
    lStatsTeam2.append(partida.redTeam.firstRiftHerald)
    return lStatsTeam, lStatsTeam2



def generaExcelSheet(partida,wb):

    #Llamamos a funcion para crear las listas y se lo asignamos a una list que tendrá 12 posiciones, 2 de equipo, 10 de jugadores
    listaDatos = listasExcel(partida)
    #Creamos el excel
    sheet1 = wb.add_sheet(partida.nombreMatch, cell_overwrite_ok=True)
    #estilos#######
    #color azul
    xlwt.add_palette_colour("custom_blue_color", 0x21)
    wb.set_colour_RGB(0x21, 192, 223, 255)
    #color rojo
    xlwt.add_palette_colour("custom_red_color", 0x22)
    wb.set_colour_RGB(0x22, 251, 204, 150)
    styleBold = xlwt.easyxf('font: bold 1')
    styleNormalBlue = xlwt.easyxf('align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_blue_color')
    styleNormalRed = xlwt.easyxf('align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_red_color')
    #/estilos######
    try:
        sheet1.col(0).width = 256 *12
        sheet1.col(1).width = 256 * 12
        sheet1.col(2).width = 256 * 12
        sheet1.col(3).width = 256 * 8
        sheet1.col(4).width = 256 * 10
        sheet1.col(5).width = 256 * 40
        sheet1.col(6).width = 256 * 40
        sheet1.col(7).width = 256 * 12
        sheet1.col(8).width = 256 * 12
        sheet1.col(9).width = 256 * 14
        sheet1.col(10).width = 256 * 15
        sheet1.col(11).width = 256 * 15
        sheet1.col(12).width = 256 * 15
        sheet1.col(13).width = 256 * 15
        sheet1.col(14).width = 256 * 15
        sheet1.col(15).width = 256 * 15
        sheet1.col(16).width = 256 * 15
        sheet1.col(17).width = 256 * 15
        sheet1.col(18).width = 256 * 15
        sheet1.col(19).width = 256 * 15
        sheet1.col(20).width = 256 * 17
    except ValueError:
        pass

    #ancho de columnas


    escribeLinea(sheet1, vars.titulosPartidaStats, 0, styleBold)
    escribeLinea(sheet1,listaDatos[0],1,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[1], 2,styleNormalRed)
    escribeLinea(sheet1, vars.titulosPlayerStats, 4,styleBold)
    escribeLinea(sheet1, listaDatos[2], 5,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[3], 6,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[4], 7,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[5], 8,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[6], 9,styleNormalBlue)
    escribeLinea(sheet1, listaDatos[7], 11,styleNormalRed)
    escribeLinea(sheet1, listaDatos[8], 12,styleNormalRed)
    escribeLinea(sheet1, listaDatos[9], 13,styleNormalRed)
    escribeLinea(sheet1, listaDatos[10], 14,styleNormalRed)
    escribeLinea(sheet1, listaDatos[11], 15,styleNormalRed)


def escribeLinea(sheet, lista, linea, style):
    j = 0
    for celda in lista:
        sheet.write(linea,j,celda,style)
        j = j + 1



def generaExcelCompleto(listaNumMatch, listaNombreMatch, listaLado):
    #Creamos todos los objetos matches, que se guardarán en la lista listaPartidas
    i = 0
    listaPartidas = []
    for mNumber in listaNumMatch:
        listaPartidas.append(analisisMatch(listaNumMatch[i],listaNombreMatch[i],listaLado[i]))
        i = i +1

    #Creamos el nombre del archivo
    nombreArchivo = vars.directorioScrimsExcel + "SCRIMS_" + str(datetime.now().strftime("%d_%m_%Y_%H%M")) + ".xls"
    #Generamos el excel y sus distintas sheets
    wb = Workbook()
    #Guardamos todos los datos de las scrims (solo el resumen de las partidas, no los players
    listaResumenScrims = []
    #Guardamos tambien a cada jugador de nuestro equipo individualmente
    listaPlayer1 = []
    listaPlayer2 = []
    listaPlayer3 = []
    listaPlayer4 = []
    listaPlayer5 = []
    for partida in listaPartidas:
        generaExcelSheet(partida,wb)
        #Guardamos el resumen de partida en
        listasPartida = listasExcel(partida)
        lStatsTeam = listasPartida[0]
        lStatsTeam2 = listasPartida[1]
        if lStatsTeam[2] == vars.team:
            listaPlayer1.append(listasPartida[2])
            listaPlayer2.append(listasPartida[3])
            listaPlayer3.append(listasPartida[4])
            listaPlayer4.append(listasPartida[5])
            listaPlayer5.append(listasPartida[6])
        else:
            listaPlayer1.append(listasPartida[7])
            listaPlayer2.append(listasPartida[8])
            listaPlayer3.append(listasPartida[9])
            listaPlayer4.append(listasPartida[10])
            listaPlayer5.append(listasPartida[11])
        listaResumenScrims.append(lStatsTeam)
        listaResumenScrims.append((lStatsTeam2))
    #Generamos la sheet de resumen de Scrims
    generaExcelResumen(listaResumenScrims, wb)
    #Generamos Excels de jugadores individuales
    generaExcelJugadorIndividual(listaPlayer1,wb,"TOP STATS")
    generaExcelJugadorIndividual(listaPlayer2, wb, "JUNGLE STATS")
    generaExcelJugadorIndividual(listaPlayer3, wb, "MID STATS")
    generaExcelJugadorIndividual(listaPlayer4, wb, "ADC STATS")
    generaExcelJugadorIndividual(listaPlayer5, wb, "SUPPORT STATS")
    wb.save(nombreArchivo)


def generaExcelResumen(lista, wb):
    pass
    sheet = wb.add_sheet("Resumen Scrims", cell_overwrite_ok=True)
    # estilos#######
    # color azul
    xlwt.add_palette_colour("custom_blue_color", 0x21)
    wb.set_colour_RGB(0x21, 192, 223, 255)
    # color rojo
    xlwt.add_palette_colour("custom_red_color", 0x22)
    wb.set_colour_RGB(0x22, 251, 204, 150)
    styleBold = xlwt.easyxf('font: bold 1')
    styleNormalBlue = xlwt.easyxf(
        'align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_blue_color')
    styleNormalRed = xlwt.easyxf(
        'align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_red_color')
    # /estilos######

    # ancho de columnas
    try:
        sheet.col(0).width = 256 * 12
        sheet.col(1).width = 256 * 12
        sheet.col(2).width = 256 * 12
        sheet.col(3).width = 256 * 8
        sheet.col(4).width = 256 * 10
        sheet.col(5).width = 256 * 40
        sheet.col(6).width = 256 * 40
        sheet.col(7).width = 256 * 12
        sheet.col(8).width = 256 * 12
        sheet.col(9).width = 256 * 14
        sheet.col(10).width = 256 * 15
        sheet.col(11).width = 256 * 15
        sheet.col(12).width = 256 * 15
        sheet.col(13).width = 256 * 15
        sheet.col(14).width = 256 * 15
        sheet.col(15).width = 256 * 15
        sheet.col(16).width = 256 * 15
        sheet.col(17).width = 256 * 15
        sheet.col(18).width = 256 * 15
        sheet.col(19).width = 256 * 15
        sheet.col(20).width = 256 * 17
    except ValueError:
        pass

    # /ancho de columnas

    escribeLinea(sheet, vars.titulosPartidaStats, 0, styleBold)
    i = 1
    for linea in lista:
        if (linea[1] == "Red Team"):
            escribeLinea(sheet, linea, i, styleNormalRed)
        elif (linea[1] == "Blue Team"):
            escribeLinea(sheet, linea, i, styleNormalBlue)
        i = i +1
        if (i%3==0):
            i = i +1

def generaExcelJugadorIndividual(lista, wb, sheetName):
    pass
    sheet = wb.add_sheet(sheetName, cell_overwrite_ok=True)
    # estilos#######
    # color azul
    xlwt.add_palette_colour("custom_blue_color", 0x21)
    wb.set_colour_RGB(0x21, 192, 223, 255)
    # color rojo
    xlwt.add_palette_colour("custom_red_color", 0x22)
    wb.set_colour_RGB(0x22, 251, 204, 150)
    styleBold = xlwt.easyxf('font: bold 1')
    styleNormalBlue = xlwt.easyxf(
        'align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_blue_color')
    styleNormalRed = xlwt.easyxf(
        'align: vert centre, horiz center')
    # /estilos######

    # ancho de columnas
    try:
        sheet.col(0).width = 256 * 12
        sheet.col(1).width = 256 * 12
        sheet.col(2).width = 256 * 12
        sheet.col(3).width = 256 * 8
        sheet.col(4).width = 256 * 10
        sheet.col(5).width = 256 * 40
        sheet.col(6).width = 256 * 40
        sheet.col(7).width = 256 * 12
        sheet.col(8).width = 256 * 12
        sheet.col(9).width = 256 * 14
        sheet.col(10).width = 256 * 15
        sheet.col(11).width = 256 * 15
        sheet.col(12).width = 256 * 15
        sheet.col(13).width = 256 * 15
        sheet.col(14).width = 256 * 15
        sheet.col(15).width = 256 * 15
        sheet.col(16).width = 256 * 15
        sheet.col(17).width = 256 * 15
        sheet.col(18).width = 256 * 15
        sheet.col(19).width = 256 * 15
        sheet.col(20).width = 256 * 17
    except ValueError:
        pass

    # /ancho de columnas

    escribeLinea(sheet, vars.titulosPlayerStats, 0, styleBold)
    i = 1
    for statsPartida in lista:
        escribeLinea(sheet, statsPartida, i, styleNormalRed)
        i = i+2



##Generador Excel Para datos individuales SOLOQ y FLEXQ:
def generaExcelRankeds(listaPartidas, nombre):
    rutaArchivo = vars.directorioRanked + nombre + "_" + str(datetime.now().strftime("%d_%m_%Y_%H%M")) + ".xls"
    wb = Workbook()
    sheet = wb.add_sheet("Analisis Stats Ranked", cell_overwrite_ok=True)

    # estilos#######
    # color azul
    xlwt.add_palette_colour("custom_green_color", 0x21)
    wb.set_colour_RGB(0x21, 191, 255, 215)
    # color rojo
    xlwt.add_palette_colour("custom_red_color", 0x22)
    wb.set_colour_RGB(0x22, 251, 204, 150)
    styleBold = xlwt.easyxf('font: bold 1')
    styleNormalBlue = xlwt.easyxf(
        'align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_green_color')
    styleNormalRed = xlwt.easyxf(
        'align: vert centre, horiz center; pattern: pattern solid, fore_colour custom_red_color')
    # /estilos######
    #Ancho columnas
    try:
        sheet.col(0).width = 256 * 12
        sheet.col(1).width = 256 * 24
        sheet.col(2).width = 256 * 6
        sheet.col(3).width = 256 * 6
        sheet.col(4).width = 256 * 10
        sheet.col(5).width = 256 * 15
        sheet.col(6).width = 256 * 15
        sheet.col(7).width = 256 * 5
        sheet.col(8).width = 256 * 5
        sheet.col(9).width = 256 * 5
        sheet.col(10).width = 256 * 16
        sheet.col(11).width = 256 * 15
        sheet.col(12).width = 256 * 10
        sheet.col(13).width = 256 * 5
        sheet.col(14).width = 256 * 12
        sheet.col(15).width = 256 * 13
        sheet.col(16).width = 256 * 13
        sheet.col(17).width = 256 * 13
        sheet.col(18).width = 256 * 14
        sheet.col(19).width = 256 * 14
        sheet.col(20).width = 256 * 13
        sheet.col(21).width = 256 * 15
        sheet.col(22).width = 256 * 13
        sheet.col(23).width = 256 * 15
        sheet.col(24).width = 256 * 12
        sheet.col(25).width = 256 * 12
        sheet.col(26).width = 256 * 12
        sheet.col(27).width = 256 * 13
        sheet.col(28).width = 256 * 13
    except ValueError:
        pass
    #Escribir en el excel

    escribeLinea(sheet,vars.titulosPlayerStatsRanked,0,styleBold)
    i = 1
    for stats in listaPartidas:
        if stats[2] == "Win":
            escribeLinea(sheet, stats, i, styleNormalBlue)
        else:
            escribeLinea(sheet, stats, i, styleNormalRed)
        i = i + 2
    wb.save(rutaArchivo)

##################################
#FIN Funciones generadoras Excel
##################################

##Función que dada un archivo devuelve 3 listas (una con los numeros de match, otra con el nombre de la scrim, y una ultima con el lado del equipo.
##Ejecuta generaExcelCompleto
def generadorStatsScrims(nombreArchivo):
    rutaArchivo = vars.directiorioScrimsTexto + nombreArchivo
    print ("abriendo archivo:",rutaArchivo)
    f = open(rutaArchivo)
    lineas = f.read().splitlines()

    listaNumMatch = []
    listaNombreMatch = []
    listaLado = []

    for linea in lineas:
        listaNumMatch.append(linea.split(", ")[0])
        listaNombreMatch.append(linea.split(", ")[1])
        listaLado.append(int(linea.split(", ")[2]))
    print(listaNumMatch)
    print(listaNombreMatch)
    print(listaLado)

    generaExcelCompleto(listaNumMatch,listaNombreMatch,listaLado)


#######################################################
#FUNCIONES PARA GENERAR STATS JUGADOR A PARTIR DE SOLOQ y FLEXQ entre dos fechas
#######################################################

#Funcion que genera un query para obtener encryptedAccountId a partir de nombre de invocador (necesario para ver lista de matches).
#No hace de nuevo el query de un invocador si ya los hemos hecho anteriormente con ese nombre
#Devuelve el EncriptedAccountID
def generaAccountID(nombreSummoner):
    rutaGuardar = vars.directorioAccounts+ str(nombreSummoner) + ".json"
    query = vars.idAccountRequest + nombreSummoner + vars.referenciaKey + vars.apiKey
    #Vemos si ya existe el archivo, si es así no hacemos nada.
    if (os.path.isfile(rutaGuardar)):
        pass
    else:
        print ("Generando query y guardando ID_ACCOUNT")
        #Hace el query y lo guarda en la VAR account
        account = requests.get(query)
        #Comprueba si el query se hizo correctamente
        if (str(account) == "<Response [200]>"):
            print ("Petición enviada a RIOT API. Se pudo hacer el QUERY correctamente",account)
        else:
            print("No se pudo hacer el query. ERROR:", account)
        #guardar archivo JSON
        with open(rutaGuardar, "w") as outfile:
            json.dump(account.json(),outfile)
    #Abrimos el archivo que acabamos de crear para devolver IDAccount
    with open(rutaGuardar) as json_file:
        contenido = json.load(json_file)

    return contenido["accountId"]

#Función que genera lista de Matchs de un jugador entre dos fechas
#Invoca función generaAccountID con el nombre de summoner, hace un query a la API de RIOT para generar un archivo json con todas las games entre dos fechas
#fechas que antes convertimos a epoch con una función auxiliar.
#Por ultimo abre el documento json que hemos guardado y devuelve una lista con las ID de todos los Matches de Ranked soloq y flexq, tipoDeCola, campeón elegido y fecha
#Tal que así [[matchID, Fecha, TipoDeCola, Campeón, Lane], [matchID, Fecha, TipoDeCola, Campeón, Lane]...]
def generaListaMatchs(nombreSummoner, fechaInicio, fechaFinal):
    #Generamos los atributos que pasaremos al query para buscar la lista de Matches
    idAccount = generaAccountID(nombreSummoner)
    inicioEpoch= auxiliarFechaAEpoch(fechaInicio)
    finalEpoch= auxiliarFechaAEpoch(fechaFinal)

    #El Query para pedir la lista de matches, es un poco diferente a los demás al tener parámetros extra.
    query = vars.matchListRequest + str(idAccount) + "?endTime=" + str(finalEpoch) + "&beginTime=" + str(inicioEpoch) + "&api_key=" + vars.apiKey

    rutaGuardar = vars.directorioListMatches + str(nombreSummoner) + "_" + str(inicioEpoch) + "_" + str(finalEpoch) + ".json"

    #Vemos si ya existe el archivo, si es así no hacemos nada. Sino guardamos el archivo json en su directorio correspondiente.
    if (os.path.isfile(rutaGuardar)):
        pass
    else:
        print ("Generando query y guardando LIST_MATCHES")
        #Hace el query y lo guarda en la VAR account
        listMatches= requests.get(query)
        #Comprueba si el query se hizo correctamente
        if (str(listMatches) == "<Response [200]>"):
            print ("Petición enviada a RIOT API. Se pudo hacer el QUERY correctamente",listMatches)
        else:
            print("No se pudo hacer el query. ERROR:", listMatches)
        #guardar archivo JSON
        with open(rutaGuardar, "w") as outfile:
            json.dump(listMatches.json(),outfile)

    #Abrimos el archivo que acabamos de crear para devolver IDAccount
    with open(rutaGuardar) as json_file:
        contenido = json.load(json_file)

    #Lista que contiene todos los codigos de Match que son Rankeds, para filtrar en la lista de matches y solo sacar rankeds
    listaRankeds = list(vars.dicTipoMatches.keys())
    #Lista que devolveremos al final. La creamos vacía.
    listaRankedMatches = []
    #Asignamos valores a nuestra lista.
    for matchDescripcion in contenido["matches"]:
        #filtramos por rankeds
        if(str(matchDescripcion["queue"]) in listaRankeds):
            listaRankedMatches.append([matchDescripcion["gameId"], matchDescripcion["timestamp"],vars.dicTipoMatches[str(matchDescripcion["queue"])],matchDescripcion["champion"],
                                       matchDescripcion["lane"]])
    #Le damos la vuelta a los matches para que vaya del game mas antiguo al mas reciente
    listaRankedMatches.reverse()
    return listaRankedMatches

#Función que genera la info del summoner en cada match en una lista compuesta de listas, estas ultimas tienen los stats del summoner en cada partida.
#Metemos un delay para no sobresaturar nuestro limite en al api de Riot :D
def generaStatsListaMatch(listaMatches):
    listaPlayersStats = []
    for match in listaMatches:
        ruta_match = obtenerMatch(match[0])
        #Vemos en que indice se encuentra el jugador dentro de match.json para extraer sus estadisticas.
        indiceJugadorMatch = auxParticipantID(ruta_match, match[3])

        #Creamos el objeto jugador con sus Stats (el campeon es nuestro player)
        player = obtenerStatsIndividualMatch(match[0],indiceJugadorMatch)
        #Convertimos el objeto en una lista con los stats que queremos añadir
        playerStats = creaListaPlayer(player)
        #Añadimos otros atributos:
        playerStats.insert(0, player.fecha)
        playerStats.insert(1, match[2])
        playerStats.insert(2, auxWinGame(ruta_match,indiceJugadorMatch))
        playerStats.insert(3, player.gameDuration)
        playerStats.insert(6, auxCampeonEnemigo(match[0], player, indiceJugadorMatch))

        #Añadimos a la lista de listas :D
        listaPlayersStats.append(playerStats)
        sleep(vars.delay)
    print(listaPlayersStats)
    return listaPlayersStats

#Función auxiliar que encuentra ParticipantID es el campeónID proporcionado:
#Para encontrar que player
def auxParticipantID(id_Match, id_campeon):
    with open(id_Match) as json_file:
        contenido = json.load(json_file)
    indice = None
    for participante in contenido["participants"]:
        if participante["championId"] == id_campeon:
            indice = participante["participantId"]
            break
    return indice


#Función que convierte una fecha en formato epoch ms
#La fecha hay que pasarla con formato dd.mm.yyyy
def auxiliarFechaAEpoch (fecha):
    #Añadimos a nuestra fecha el inicio del día para que quede algo así:  "dd.mm.yyyy 00:00:00,01" y convierta a epoch ms (que es lo que usa RIOT)
    fechaCompleta =  fecha + " 00:00:00,01"
    fechaEpoch = int(datetime.strptime(fechaCompleta, '%d.%m.%Y %H:%M:%S,%f').timestamp() * 1000)
    return fechaEpoch


#Funcion auxiliar que devuelve si el summoner ha ganado su game:
def auxWinGame(rutaMatch, participantID):
    win = "No se puede conseguir"
    with open(rutaMatch) as json_file:
        contenido = json.load(json_file)
    teamBlueWin = contenido["teams"][0]["win"]
    teamRedWin = contenido["teams"][1]["win"]

    if participantID >0 and participantID<= 5:
        win = teamBlueWin
    elif participantID >5 and participantID<= 10:
        win = teamRedWin
    return win

#Función auxiliar que devuelve el campeón al que se enfrenta nuestro summoner:
def auxCampeonEnemigo(idMatch, player, participantID):
    campeon = player.campeon
    campeonEnemigo = "Fallo"
    blueTeam, redTeam = analisisTeams(idMatch)
    if participantID >0 and participantID <=5:
        i = 0
        for jugador in blueTeam.ordenarPlayers():
            if jugador.campeon == player.campeon:
                campeonEnemigo = redTeam.ordenarPlayers()[i].campeon
            i = i +1
    elif participantID>5 and participantID<=10:
        i = 0
        for jugador in redTeam.ordenarPlayers():
            if jugador.campeon == player.campeon:
                campeonEnemigo = blueTeam.ordenarPlayers()[i].campeon
            i = i +1
    return campeonEnemigo


#Función principal que engloba a las 3 funciones para generar la lista de Stats de un jugador en ranked durante un periodo de tiempo

def generaStatsRankedJugador (nombreInvocador, fechaInicio, fechaFinal):
    listaMatches = generaListaMatchs(nombreInvocador, fechaInicio, fechaFinal)
    print ("Se van a hacer un total de:", str(len(listaMatches)), "querys a la API de RIOT, ¿Deseas continuar?y/n")
    respuesta = input()
    if respuesta == 'y':
        print("\nSe procede a los QUERYS con un delay de:", vars.delay, "segudos entre query")
        listaStats = generaStatsListaMatch(listaMatches)
        generaExcelRankeds(listaStats, nombreInvocador)
    else:
        print("\nSe aborta el programa")