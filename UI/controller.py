import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model



    def handleCreaGrafo(self, e):
        goal=self.view.txtGoalFatti.value

        if goal=="":
            self.view.create_alert("Inserire valore")
            return
        try:
            intGoal=float(goal)
        except ValueError:
            self.view.create_alert("Non numerico")
            return
        self.model.creaGrafo(intGoal)
        n,a=self.model.getDetails()
        self.view.txtGrafo.controls.append(ft.Text(f"Nodi: {n}. Archi: {a}"))
        self.view.btnTopPlayer.disabled=False
        self.view.btnDreamTeam.disabled=False
        self.view.update_page()
        pass


    def handleTopPlayer(self, e):
        top,somma,lista=self.model.getTopPlayer()
        self.view.txtGrafo.controls.append(ft.Text(f"\nTop player:"))
        self.view.txtGrafo.controls.append(ft.Text(f"{top}"))
        self.view.txtGrafo.controls.append(ft.Text(f"Somma minuti in più di altri: {somma}\n"))
        for a in lista:
            self.view.txtGrafo.controls.append(ft.Text(f"{a[0]} | {a[1]["peso"]}"))

        self.view.update_page()
        pass

    def handleDreamTeam(self, e):
        n = self.view.numeroGiocatori.value

        if n == "":
            self.view.create_alert("Inserire valore")
            return
        try:
            intN = int(n)
        except ValueError:
            self.view.create_alert("Non numerico")
            return
        sol,c=self.model.cammino(intN)
        self.view.txtGrafo.controls.append(ft.Text(f"\nPeso max: {c}"))
        for a in sol:
            self.view.txtGrafo.controls.append(ft.Text(f"{a}"))
        self.view.update_page()
        pass



    def fillDD(self):
        pass


           