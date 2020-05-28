import StatsJugadorIndividualClass
import vars

#Clase que a registra las estadisticas de un equipo durante una partida y a los 5 jugadores y sus stats.
class teamStats:
    def __init__(self, matchID, nombre, win, firstBlood, firstTower, firstInhibitor, firstBaron, firstDragon, firstRiftHerald,
            towerKills, inhibitorKills, baronKills, dragonKills, riftHeraldKills, player1 = None, player2 = None, player3 = None,
             player4 = None, player5 = None, bans = None):

        self.matchID = matchID
        self.nombre = nombre
        self.win = win
        self.firstBlood = firstBlood
        self.firstTower = firstTower
        self.firstInhibitor = firstInhibitor
        self.firstBaron = firstBaron
        self.firstDragon = firstDragon
        self.firstRiftHerald = firstRiftHerald
        self.towerKills =towerKills
        self.inhibitorKills = inhibitorKills
        self.baronKills = baronKills
        self.dragonKills = dragonKills
        self.riftHeraldKills = riftHeraldKills
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.bans =  bans

    #Ordena a los 5 jugadores por posición. 10% de fallar por culpa de nuestros amigos de Riot :D
    def ordenarPlayers(self):
        listaplayers = [self.player1,self.player2,self.player3,self.player4,self.player5]
        listaOrden = [0,1,2,3,4]
        for p in listaplayers:
            if (p.lane == "TOP"):
                listaOrden[0] = p
            if (p.lane == "JUNGLE"):
                listaOrden[1] = p
            if (p.lane == "MIDDLE"):
                listaOrden[2] = p
            if (p.lane == "BOTTOM" and p.role == "DUO_CARRY"):
                listaOrden[3] = p
            if (p.lane == "BOTTOM" and p.role == "DUO_SUPPORT"):
                listaOrden[4] = p

        #A veces el propio LOL no atina con las posiciones, en ese caso devolveremos la lista de personajes sin ordenar por rol.
        if listaOrden[0] == 0 or listaOrden[1] == 1 or listaOrden[2] == 2 or listaOrden[3] == 3 or listaOrden[4] == 4:
            return listaplayers
        else:
            return listaOrden

    def imprimir(self):
        print ("^^^^^^")
        print (str(self.nombre) + " | WIN?: " + str(self.win) + " | Primera sangre: " + str(self.firstBlood) + " | Primera Torre: " + str(self.firstTower)+
               " | Primer Inhibidor: " + str(self.firstInhibitor) + " | Primer Baron: " + str(self.firstBaron) + " | Primer Dragon: " + str(self.firstDragon)+
               " | Primer Herald: " + str(self.firstRiftHerald) + "\nTorres Destruidas: " + str(self.towerKills) + " | Inhibidores Destruidos: " + str(self.inhibitorKills)+
               " | Baron Kills: " + str(self.baronKills) + " | Dragon Kills: " + str(self.dragonKills)+ " | Herald Kills: " + str(self.riftHeraldKills))
        print ("^^^^^^")

    #Genera una lista que contiene a su vez una lista con los campeones ordenados y un string con los campeones ordenador separados por "-"
    def picks(self):
        lPicks = []

        playersOrdenados = self.ordenarPlayers()
        for p in playersOrdenados:
            lPicks.append(p.campeon)
        sPicks = "-".join(lPicks)
        return [lPicks, sPicks]

    def bansList(self):
        lBans = []
        for c in self.bans:
            lBans.append(vars.dicCampeones[str(c)])
        sBans = "-".join(lBans)
        return [lBans,sBans]
