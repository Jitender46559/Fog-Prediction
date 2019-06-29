import sys
import math
import pickle
import sqlite3
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMD FOG PREDICTION")
        self.setWindowIcon(QIcon('Images\logo.png'))

        # Set Background Image
        self.label_1 = QLabel(self)
        self.label_1.setPixmap(QPixmap('Images\cloud.jpg'))
        self.label_1.setGeometry(0,0,700,900)

        # Set Header Image
        self.label_2 = QLabel(self)
        self.label_2.setPixmap(QPixmap('Images\Header.jpg'))
        self.label_2.setGeometry(0, 0, 700, 153)

        # Set Logo Image
        self.label_3 = QLabel(self)
        self.label_3.setPixmap(QPixmap('Images\imd_logo1.png'))
        self.label_3.setGeometry(15, 5, 140, 153)

        # Set ESSO Image
        self.label_3 = QLabel(self)
        self.label_3.setPixmap(QPixmap('Images\esso1.png'))
        self.label_3.setGeometry(600, 5, 140, 153)

        # Set Header Text
        self.head_text = QLabel('''                                                                  पृथ्वी विज्ञान मंत्रालय 
                                                    MINSITRY OF EARTH SCIENCES
                                                     भारत मौसम विज्ञान विभाग 
                                           INDIA METEOROLOGICAL DEPARTMENT
                                                 प्रादेशिक मौसम केंद्र, नई दिल्ली
                                 REGIONAL METEOROLOGICAL CENTER, NEW DELHI
                                                                                           
                        ''' , self)

        self.setGeometry(50,50,700,900)
        self.UI()

    def UI(self):

        # For Wind Speed
        self.wsLabel = QLabel("Wind Speed (knots) :", self)
        self.wsLabel.move(120, 182)
        self.wsTextBox = QLineEdit(self)
        self.wsTextBox.move(320, 180)

        # For Visibility
        self.visibilityLabel = QLabel("Visibility :", self)
        self.visibilityLabel.move(120, 232)
        self.visibilityTextBox = QLineEdit(self)
        self.visibilityTextBox.move(320, 230)

        # For Weather Condition
        self.weatherLabel = QLabel("Weather Condition :", self)
        self.weatherLabel.move(120, 282)
        self.weatherTextBox = QLineEdit(self)
        self.weatherTextBox.move(320, 280)

        # For Lowest Cloud
        self.lstLabel = QLabel("Lowest Cloud (Octas) :", self)
        self.lstLabel.move(120, 332)
        self.lstTextBox = QLineEdit(self)
        self.lstTextBox.move(320, 330)

        # For Low Cloud
        self.lwLabel = QLabel("Low Cloud (Octas) :", self)
        self.lwLabel.move(120, 382)
        self.lwTextBox = QLineEdit(self)
        self.lwTextBox.move(320, 380)

        # For Middle Cloud
        self.mdLabel = QLabel("Middle Cloud (Octas) :", self)
        self.mdLabel.move(120, 432)
        self.mdTextBox = QLineEdit(self)
        self.mdTextBox.move(320, 430)

        # For Minimun Temperature
        self.tempLabel = QLabel("Minimum Temperature :", self)
        self.tempLabel.move(120, 482)
        self.tempTextBox = QLineEdit(self)
        self.tempTextBox.move(320, 480)

        # For Dew Point
        self.dpLabel = QLabel("Dew Point :", self)
        self.dpLabel.move(120, 532)
        self.dpTextBox = QLineEdit(self)
        self.dpTextBox.move(320, 530)

        # For Morning Visibility
        self.morning_visLabel = QLabel("Morning Visibility :", self)
        self.morning_visLabel.move(120, 582)
        self.morning_visTextBox = QLineEdit(self)
        self.morning_visTextBox.move(320, 580)

        # Create a Button
        self.predButton = QPushButton("PREDICT", self)
        self.predButton.move(300, 620)
        self.predButton.setGeometry(200, 660, 300, 50)

        # connect button to function on_click
        self.predButton.clicked.connect(self.on_click)

        # Create Display Box
        self.displayTextBox = QLineEdit(self)
        self.displayTextBox.move(250, 780)
        self.displayTextBox.setGeometry(180, 750, 350, 70)

        self.show()

    # Action on Predict button click
    def on_click(self):
        self.__calculateRH()
        self.__convertSpeed()
        self.fog = self.__prediction()
        self.__storeData()
        self.wsTextBox.setText("")
        self.visibilityTextBox.setText("")
        self.weatherTextBox.setText("")
        self.lstTextBox.setText("")
        self.lwTextBox.setText("")
        self.mdTextBox.setText("")
        self.tempTextBox.setText("")
        self.dpTextBox.setText("")
        self.morning_visTextBox.setText("")
        self.displayTextBox.setText(str(self.fog))

    # Calculate RH value
    def __calculateRH(self):
        try:
            self.rh_value = 100 * (math.exp(
                (17.625 * float(self.dpTextBox.text())) / (243.04 + float(self.dpTextBox.text()))) / math.exp(
                (17.625 * float(self.tempTextBox.text())) / (243.04 + float(self.tempTextBox.text()))))
        except:
            print("Value Error")
            pass

    # Convert Speed into (m/s)
    def __convertSpeed(self):
        try:
            self.windSpeed = float(self.wsTextBox.text()) * 0.514
        except:
            print("Value Error")
            pass

    # Find prediction using machine learning model
    def __prediction(self):
        try:
            filename = 'Model_V1.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            ws = int(self.wsTextBox.text())
            vis = int(self.visibilityTextBox.text())
            weather = int(self.weatherTextBox.text())
            lst_cloud = int(self.lstTextBox.text())
            lw_cloud = int(self.lwTextBox.text())
            mid_cloud = int(self.mdTextBox.text())
            temp = int(self.tempTextBox.text())
            dew = int(self.dpTextBox.text())
            rh = float(self.rh_value)
            w_speed = float(self.windSpeed)
            data = [[ws, vis, weather, lst_cloud, lw_cloud, mid_cloud, temp, dew, rh, w_speed]]
            predict = loaded_model.predict(data)
            fog_map = {
                "0" : "SHALLOW FOG",
                "1" : "MODERATE FOG",
                "2" : "DENSE FOG",
                "3" : "VERY DENSE FOG",
                "4" : "NEGLIGIBLE FOG"
            }
            return fog_map[str(predict[0])]
        except:
            print("Loading Model Failed")
            pass

    def __storeData(self):
        conn = sqlite3.connect('FOG_Prediction.db')
        c = conn.cursor()
        try:
            c.execute(
                'CREATE TABLE IF NOT EXISTS RECORD_FOG (TIME TEXT PRIMARY KEY, WIND_SPEED REAL, VISIBILITY REAL, WEATHER REAL, LOWEST_CLOUD REAL, LOW_CLOUD REAL, MID_CLOUD REAL, TEMPERATURE REAL, DEW_POINT REAL, RH_VALUE REAL, MORNING_VISIBILITY REAL, FOG_TYPE TEXT)')
        except:
            print("Table is not created")
            pass
        time = str(datetime.datetime.now().date())
        ws = int(self.wsTextBox.text())
        vis = int(self.visibilityTextBox.text())
        weather = int(self.weatherTextBox.text())
        lst_cloud = int(self.lstTextBox.text())
        lw_cloud = int(self.lwTextBox.text())
        mid_cloud = int(self.mdTextBox.text())
        temp = int(self.tempTextBox.text())
        dew = int(self.dpTextBox.text())
        rh = float(self.rh_value)
        mvis = int(self.morning_visTextBox.text())
        fog = str(self.fog)
        try:
            c.execute(
                "INSERT INTO RECORD_FOG (TIME, WIND_SPEED, VISIBILITY, WEATHER, LOWEST_CLOUD, LOW_CLOUD, MID_CLOUD, TEMPERATURE, DEW_POINT, RH_VALUE, MORNING_VISIBILITY, FOG_TYPE) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (time, ws, vis, weather, lst_cloud, lw_cloud, mid_cloud, temp, dew, rh, mvis, fog))
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("WARNING !!!!")
            msg.setText("Already Filled for Today")
            msg.exec_()
            pass
        conn.commit()
        c.close()
        conn.close()



def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__=="__main__":
    main()
