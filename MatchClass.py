
#la VAR numTeam funciona así:
#Si marcamos 0 significa que somos lado azul y blueSide será True y redSide False.
#Si marcamos 1 significa que somos lado rojo y lo hará al revés.
class match:
    def __init__(self, idMatch, nombreMatch, numTeam, blueTeam, redTeam):
        self.idMatch = idMatch
        if numTeam == 0:
            self.blueSide = True
            self.redSide = False
        elif numTeam == 1:
            self.blueSide = False
            self.redSide = True
        self.nombreMatch = nombreMatch
        self.blueTeam = blueTeam
        self.redTeam = redTeam


