from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
from prediction import *

class UI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.width= 900
        self.height= 500
        self.canvas = Canvas(self, width = self.width, height = \
        self.height)
        self.canvas.pack()
        self.info= PhotoImage(file='img/info.png')
        self.coverScreen()

    def coverScreen(self):
        self.canvas.delete('all')
        self.start = Image.open('img/carvana.jpg')
        self.startImg = ImageTk.PhotoImage(self.start)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.startImg)
        self.canvas.create_text(self.width/3, self.height/3, \
        text="Kicked Car", fill="white", font=("ms serif", 48, "bold"))
        self.canvas.create_text(self.width/3, self.height/2, \
        text="Prediction", fill="white", font=("ms serif", 48, "bold"))
        self.startButton = Button(self, text="Start", \
        command=self.dataProcScreen, width= 10)
        self.startButton.config(font=('ms serif', 12))
        self.canvas.create_window(self.width/2, self.height/6*5, \
        window=self.startButton)
        self.iButton= Button(self, command=self.helpScreen)
        self.iButton.config(image=self.info, compound= CENTER, width=30, height=30)
        self.canvas.create_window(self.width/12*11, self.height/12*11, window= self.iButton)

    def helpScreen(self):
        # explain what the app is for
        self.canvas.delete('all')
        self.help1 = Image.open('img/help.jpg')
        self.tkhelp1 = ImageTk.PhotoImage(self.help1)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.tkhelp1)
        self.tkexit= PhotoImage(file='img/exit.png')
        self.tknext= PhotoImage(file='img/next.png')
        self.exit= Button(self, command=self.coverScreen)
        self.exit.config(image= self.tkexit, compound= CENTER)
        self.canvas.create_window(self.width/20*19, self.height/9, window= self.exit)
        self.next= Button(self, command=self.helpScreen2)
        self.next.config(image= self.tknext, compound= CENTER)
        self.canvas.create_window(self.width/20*19, self.height/12*11, window= self.next)

    def helpScreen2(self):
        # explain how to use the app
        self.canvas.delete('all')
        self.help2 = Image.open('img/help2.jpg')
        self.tkhelp2 = ImageTk.PhotoImage(self.help2)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.tkhelp2)
        self.tkexit= PhotoImage(file='img/exit.png')
        self.tkprev= PhotoImage(file='img/previous.png')
        self.exit= Button(self, command=self.coverScreen)
        self.exit.config(image= self.tkexit, compound= CENTER)
        self.canvas.create_window(self.width/20*19, self.height/9, window= self.exit)
        self.previous= Button(self, command=self.helpScreen)
        self.previous.config(image= self.tkprev, compound= CENTER)
        self.canvas.create_window(self.width/20*19, self.height/12*11, window= self.previous)


    def dataProcScreen(self):
        # choose which option for prediction: manual or file
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='black')
        self.manual= Button(self, command= self.manualEntry)
        self.mImg= Image.open('img/manual.jpg')
        self.tkmImg= ImageTk.PhotoImage(self.mImg)
        self.manual.config(image=self.tkmImg, compound=CENTER, width= 300, height=100)
        self.canvas.create_window(self.width/4, self.height/4, window= self.manual)
        self.file= Button(self, command= self.fileEntry)
        self.fImg= Image.open('img/fileup.jpg')
        self.tkfImg= ImageTk.PhotoImage(self.fImg)
        self.file.config(image=self.tkfImg, compound=CENTER, width= 300, height=100)
        self.canvas.create_window(self.width/4, self.height/4*3, window= self.file)
        self.canvas.create_text(self.width/5*3, self.height/4, text="Manual Entry", \
        fill='white', font=('ms serif',30))
        self.canvas.create_text(self.width/5*3, self.height/4*3, text="Browse Files", \
        fill='white', font=('ms serif',30))
        self.backSelect= Button(self, command= self.coverScreen, text= 'Back')
        self.backSelect.config(width=10)
        self.canvas.create_window(self.width/12, self.height/15, window= self.backSelect)


    def manualEntry(self):
        # manual entry form
        self.canvas.delete('all')
        self.formEntry = Image.open('img/form.jpg')
        self.tkformEntry = ImageTk.PhotoImage(self.formEntry)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.tkformEntry)
        self.featuresList= ['MMRCurrentRetailAveragePrice', 'MMRAcquisitionRetailAveragePrice', \
        'MMRAcquisitionAuctionAveragePrice', 'MMRCurrentAuctionAveragePrice', 'VehicleAge',\
        'VehBCost', 'VehOdo']
        self.alphaDict={}
        for i in range(len(self.featuresList)):
            self.canvas.create_text(self.width/5, self.height/6+ 50*i, text=self.featuresList[i], fill='white',\
            font=('ms serif', 14))
            self.alphaDict[i]= Entry(self, width=12)
            self.alphaDict[i].config(font=('ms serif', 14))
            self.canvas.create_window(self.width/2, self.height/6+ 50*i, window= self.alphaDict[i])
        self.submit= Button(self, command=self.preds, text= 'PREDICT')
        self.submit.config(font=('ms serif', 18, 'bold'))
        self.canvas.create_window(self.width/3, self.height/11*10, window= self.submit)
        self.iButton= Button(self, command=self.fieldInfo)
        self.iButton.config(image=self.info, compound= CENTER, width=30, height=30)
        self.canvas.create_window(self.width/15, self.height/10*8, window= self.iButton)
        self.backSelect= Button(self, command= self.dataProcScreen, text= 'Back')
        self.backSelect.config(width=10)
        self.canvas.create_window(self.width/12, self.height/15, window= self.backSelect)

    def fieldInfo(self):
        # part of manual and file upload explaination
        #explain what the form fields mean
        self.canvas.delete('all')
        self.fieldImg = Image.open('img/field.jpg')
        self.tkfieldImg = ImageTk.PhotoImage(self.fieldImg)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.tkfieldImg)
        self.backSelect= Button(self, command= self.manualEntry, text= 'Back')
        self.backSelect.config(width=10, bg= 'black', fg='white')
        self.canvas.create_window(self.width/12, self.height/15, window= self.backSelect)


    def preds(self):
        # get the form values to create feature dict to be inputted into
        # the predict function
        # return prediction given car features
        self.featureDict= {}
        for i in self.alphaDict:
            self.featureDict[self.featuresList[i]]= float(self.alphaDict[i].get())
        val= returnPreds(self.featureDict)
        self.canvas.delete('all')
        self.bad = Image.open('img/badBuy.jpg')
        self.tkbad = ImageTk.PhotoImage(self.bad)
        self.good= Image.open('img/goodBuy.jpg')
        self.tkgood= ImageTk.PhotoImage(self.good)
        if val==1:
            self.canvas.create_image(self.width/2, self.height/2, image= self.tkbad)
        else:
            self.canvas.create_image(self.width/2, self.height/2, image=self.tkgood)
        self.back= Button(self, command= self.manualEntry, text= 'Back')
        self.back.config(width=10, bg= 'black', fg='white')
        self.canvas.create_window(self.width/12, self.height/15, window= self.back)

    def fileEntry(self):
        # open csv file, read in dataframe
        # add predictions to df then save it as new file
        self.file =  filedialog.askopenfilename(initialdir = "/", \
        title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        if self.file != None:
            data = pd.read_csv(self.file)
            data=data[['VehBCost', 'MMRCurrentRetailAveragePrice', \
            'MMRAcquisitionRetailAveragePrice', 'VehOdo', 'VehicleAge', \
            'MMRAcquisitionAuctionAveragePrice', 'MMRCurrentAuctionAveragePrice']]
            fDict= data.to_dict(orient='records')
            for i, row in data.iterrows():
                val= returnPreds(fDict[i])
                if val==1:
                    data.at[i, 'preds']= 'Bad Buy'
                else:
                    data.at[i, 'preds']= 'Good Buy'
            data.to_csv('predictions.csv')
            print('done')
            self.canvas.delete('all')
            self.done = Image.open('img/done.jpg')
            self.tkdone= ImageTk.PhotoImage(self.done)
            self.canvas.create_image(self.width/2, self.height/2, image= self.tkdone)
            self.back= Button(self, command= self.dataProcScreen, text= 'Back')
            self.back.config(width=10)
            self.canvas.create_window(self.width/12, self.height/15, window= self.back)



predUI = UI()
predUI.mainloop()
