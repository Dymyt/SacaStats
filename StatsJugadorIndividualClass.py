from copy import deepcopy
import vars
import time

#Esta clase guarda los stats que haya desarrollado un jugador en una partida.
class statsJugador:
    def __init__(self, matchID, fecha, lane, gameDuration, campeon, kills, deaths, assists,  totalDamageDealtToChampions, totalDamageTaken, totalHeal, totalTimeCrowdControlDealt, visionScore,
                 visionWardsBoughtInGame, wardsPlaced, wardsKilled, goldEarned, totalMinionsKilled, neutralMinionsKilledTeamJungle, neutralMinionsKilledEnemyJungle,
                 creepsMin0_10, creepsMin10_20 , damageDealtToObjectives, damageDealtToTurrets, turretKills, inhibitorKills, role):

        self.matchID = matchID
        self.fecha = time.strftime('%d/%m/%Y', time.gmtime(fecha/1000.0))
        self.gameDuration = int(gameDuration / 60)
        self.lane = lane
        self.campeon = vars.dicCampeones[str(campeon)]
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        if deaths == 0:
            self.KDA = "INFINITO"
        else:
            self.KDA = (kills + assists)/deaths
        self.totalDamageDealtToChampions = totalDamageDealtToChampions
        self.totalDamageTaken = totalDamageTaken
        self.totalHeal = totalHeal
        self.totalTimeCrowdControlDealt = totalTimeCrowdControlDealt
        self.visionScore = visionScore
        self.visionWardsBoughtInGame = visionWardsBoughtInGame
        self.wardsPlaced = wardsPlaced
        self.wardsKilled = wardsKilled
        self.goldEarned = goldEarned
        self.totalMinionsKilled = totalMinionsKilled
        self.neutralMinionsKilledTeamJungle = neutralMinionsKilledTeamJungle
        self.neutralMinionsKilledEnemyJungle = neutralMinionsKilledEnemyJungle
        self.creepsMin0_10 = creepsMin0_10
        self.creepsMin10_20 = creepsMin10_20
        self.creepsporMinuto = totalMinionsKilled / self.gameDuration
        self.goldPorMinuto =  goldEarned / self.gameDuration
        self.damageDealtToObjectives = damageDealtToObjectives
        self.damageDealtToTurrets = damageDealtToTurrets
        self.turretKills = turretKills
        self.inhibitorKills = inhibitorKills
        self.role = role

    def imprimir (self):
        print ("*************")
        print ("Fecha: " + str(self.fecha) + "[epoch ms] | Game Duration: " + str(self.gameDuration) + "mins. | Campeón (Lane): " + str(self.campeon) + "("+ str(self.lane) + ")"
               +" | KDA: " + str(self.kills) + "/" + str(self.deaths) + "/" + str(self.assists) + "(" + str(self.KDA) + ")"
               + " | DMG a campeones: " + str(self.totalDamageDealtToChampions) + " | DMG Recibido: " + str(self.totalDamageTaken)
               + " | Heal total: " + str(self.totalHeal) + " | CC Aplicado: " + str(self.totalTimeCrowdControlDealt) + "\n"+
               "Vision Score: " + str(self.visionScore) + " | Pink Wards: " + str(self.visionWardsBoughtInGame) + " | Wards Colocados: "
               + str(self.wardsPlaced) + " | Wards destruidos: " + str(self.wardsKilled) + " | Oro total/por minuto: " +
               str(self.goldEarned)+ "/"+ str(self.goldPorMinuto)+ " | CS total/minuto: " + str(self.totalMinionsKilled) + "/"+
               str(self.creepsporMinuto) + " | CS por min @ 10: " + str(self.creepsMin0_10)+ " | CS por min del 10 a 20: " +
               str(self.creepsMin10_20) + "\n" + "Monstruos de jungla aliada/enemiga: " + str(self.neutralMinionsKilledTeamJungle) + "/"+
               str(self.neutralMinionsKilledEnemyJungle) + " | Daño a objetivos: " + str(self.damageDealtToObjectives) + " | Daño a torres: "+
               str(self.damageDealtToTurrets) + " | Torres destruidas: "+ str(self.turretKills)+ " | Inhibs. destruidos: " + str(self.inhibitorKills))
        print("*************")