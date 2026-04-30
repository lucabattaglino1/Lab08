from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()


    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._bestValue = 0

        self.loadEvents(nerc.id)

        self.ricorsione([], 0, maxY, maxH)

        return self._solBest, self._bestValue

    # ore di disservizio
    def getDurata(self, evento):
        delta = evento.date_event_finished - evento.date_event_began
        return delta.total_seconds()

    # totale ore parziale
    # prende ogni evento, calcola la durata,
    # la trasforma in ore, somma tutto
    def sommaOre(self, parziale):
        totale = 0

        for evento in parziale:
            durata = evento.date_event_finished - evento.date_event_began
            ore = durata.total_seconds() / 3600
            totale = totale + ore

        return totale

    # funzione obiettivo per massimizzare i clienti
    def sommaClienti(self, parziale):

        totale = 0

        for evento in parziale:
            totale = totale + evento.customers_affected

        return totale

    def anniValidi(self, parziale, maxY):

        if len(parziale) == 0:
            return True

        # inizializzo min e max
        anno_min = parziale[0].date_event_began.year
        anno_max = parziale[0].date_event_began.year

        # scorri tutti gli eventi
        for evento in parziale:
            anno = evento.date_event_began.year

            # aggiorno min
            if anno < anno_min:
                anno_min = anno

            # aggiorno max
            if anno > anno_max:
                anno_max = anno

        # controllo la differenza
        return (anno_max - anno_min) <= maxY

    # parziale --> soluzione corrente
    # pos --> dove sono nella lista
    def ricorsione(self, parziale, pos, maxY, maxH):

        # primo e secondo vincolo
        if self.sommaOre(parziale) <= maxH and self.anniValidi(parziale, maxY):

            valore = self.sommaClienti(parziale)

            # aggiorno la soluzione migliore
            if valore > self._bestValue:
                self._bestValue = valore
                self._solBest = list(parziale)

        # provo ad aggiungere altri eventi
        for i in range(pos, len(self._listEvents)):

            evento = self._listEvents[i]

            # SCELGO
            parziale.append(evento)

            # se ancora valido → continuo
            if self.sommaOre(parziale) <= maxH and self.anniValidi(parziale, maxY):
                self.ricorsione(parziale, i + 1, maxY, maxH)

            # TORNO INDIETRO (backtracking)
            parziale.pop()

    def loadEvents(self, event_type_id):
        self._listEvents = DAO.getAllEvents(event_type_id)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc