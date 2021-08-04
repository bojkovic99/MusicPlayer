






"""
        # bg image
        self.pozadina = ImageTk.PhotoImage(Image.open('images/faceRecognition.jpg').resize((300, 350)))
        labela = Label(self, image=self.pozadina, bg="#24244a")
        labela.grid(row=0, column=0, padx=0, pady=0, rowspan=3)

        # controlFrame.grid(row=0, column=1, pady=50)
        # controlFrame.configure(bg="#24244a")
        # self.curUsername = ""
        # self.emptyL = Label(self, text="     ")
        # self.emptyL.grid(row=0, column=0)

        # web cam button

        self.camImg = ImageTk.PhotoImage(Image.open('images/cam3.png').resize((90, 65)))
        # self.btn2 = Button(self, image=self.btn2Img, bg='#0a3f6b', borderwidth=0, command=self.registerFun,
        #                  activebackground="#0a3f6b")
        self.btnWebCam = Button(self, image=self.camImg, bg='#24244a', fg="white", command=self.setLabel,
                                activebackground="#24244a", borderwidth=0)
        self.btnWebCam.grid(row=0, column=1, pady=0)

        self.eL = Label(self, bg="#24244a", text="     ")
        self.eL.grid(row=2, column=1)

        self.infoImg = ImageTk.PhotoImage(Image.open('images/infoPNG.png').resize((25, 25)))

        self.emptyLabel = Label(self,
                                text=" Please, click on camera icon to\n open your web camera.",
                                bg="#24244a", fg="white")
        self.emptyLabel.grid(row=2, column=1)
        self.emptyLabel["compound"] = LEFT
        self.emptyLabel["image"] = self.infoImg

        self.faceR = FaceRecog()

    def setLabel(self):
        self.emptyLabel.configure(text=" Press 'q' when you \n want to log in!")
        self.openWebCam()

    def openWebCam(self):
        # Pozivom run fje otvara se kamerica
        loginUsername = app.getLoginPage().faceR.run()
        if loginUsername != "":
            foundUser = loginDb(loginUsername)
            print(loginUsername)
            if foundUser is None:
                app.getLoginPage()
                print("Prazan User")
            else:
                curUser = foundUser
                self.curUsername = loginUsername

                app.getFrame1().replace_menu()
                app.getFrame1().tkraise()
        else:
            app.getStartPage().tkraise()

    def getCurusername(self):
        return self.curUsername
"""

