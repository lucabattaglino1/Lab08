import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):

        # controllo anni
        if self._view._txtYears.value is None or self._view._txtYears.value == "":
            self._view.create_alert("Seleziona un anno valido")
            return

        # controllo ore
        if self._view._txtHours.value is None or self._view._txtHours.value == "":
            self._view.create_alert("Seleziona un orario valido")
            return

        # conversione
        try:
            maxY = int(self._view._txtYears.value)
            maxH = float(self._view._txtHours.value)
        except:
            self._view.create_alert("Inserisci valori numerici")
            return

        # controllo NERC
        if self._view._ddNerc.value is None:
            self._view.create_alert("Seleziona un NERC")
            return

        nerc = self._idMap[self._view._ddNerc.value]

        # chiamata al model
        sol, valore = self._model.worstCase(nerc, maxY, maxH)

        # pulisco output
        self._view._txtOut.controls.clear()

        # stampa risultato
        self._view._txtOut.controls.append(ft.Text(f"Tot clienti: {valore}"))
        self._view._txtOut.controls.append(ft.Text(f"Numero eventi: {len(sol)}"))

        for e in sol:
            self._view._txtOut.controls.append(
                ft.Text(f"{e.date_event_began} - clienti: {e.customers_affected}")
            )

        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
