# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QWidget)
import pandas as pd
import ast
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from thefuzz import fuzz
from thefuzz import process
import math

# import os


data = pd.read_csv('Raw Database.csv')
data['Description'] = data['Description'].str.strip()
data = data[~data['InvoiceNo'].str.contains('C')]

items = data['Description'][data['Country'] =="Portugal"].unique()

basket_Por = (data[data['Country'] =="Portugal"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

basket_Por = pd.get_dummies(basket_Por).astype(bool)

frq_items_Por = apriori(basket_Por, min_support = 0.04, use_colnames = True)
rules_Por = association_rules(frq_items_Por, metric ="lift", min_threshold = 1)
rules_Por = rules_Por.sort_values(['confidence', 'lift'], ascending =[False, False])


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 388)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 270, 611, 91))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ResetBtn = QPushButton(self.horizontalLayoutWidget)
        self.ResetBtn.setObjectName(u"ResetBtn")
        self.ResetBtn.clicked.connect(self.reset_clicked)

        self.horizontalLayout.addWidget(self.ResetBtn)

        self.SearchBtn = QPushButton(self.horizontalLayoutWidget)
        self.SearchBtn.setObjectName(u"SearchBtn")

        self.horizontalLayout.addWidget(self.SearchBtn)

        self.PredictBtn = QPushButton(self.horizontalLayoutWidget)
        self.PredictBtn.setObjectName(u"PredictBtn")

        self.horizontalLayout.addWidget(self.PredictBtn)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(20, 10, 251, 41))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ItemLab = QLabel(self.horizontalLayoutWidget_2)
        self.ItemLab.setObjectName(u"ItemLab")

        self.horizontalLayout_2.addWidget(self.ItemLab)

        self.ItemTxbx = QLineEdit(self.horizontalLayoutWidget_2)
        self.ItemTxbx.setObjectName(u"ItemTxbx")
        self.ItemTxbx.textChanged.connect(self.searchtxt_changed)

        self.horizontalLayout_2.addWidget(self.ItemTxbx)

        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(20, 60, 611, 201))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ItemLst = QListWidget(self.horizontalLayoutWidget_3)
        self.ItemLst.setObjectName(u"ItemLst")
        self.ItemLst.clicked.connect(self.item_clicked)

        self.horizontalLayout_3.addWidget(self.ItemLst)

        self.PredictLst = QListWidget(self.horizontalLayoutWidget_3)
        self.PredictLst.setObjectName(u"PredictLst")

        self.horizontalLayout_3.addWidget(self.PredictLst)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(330, 20, 121, 16))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Suki v1.0", None))
        self.ResetBtn.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.SearchBtn.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.PredictBtn.setText(QCoreApplication.translate("MainWindow", u"Predict", None))
        self.ItemLab.setText(QCoreApplication.translate("MainWindow", u"Search:", None))

        __sortingEnabled = self.ItemLst.isSortingEnabled()
        self.ItemLst.setSortingEnabled(False)

        for index, item in enumerate(items):
            self.ItemLst.insertItem(index, item)

        self.ItemLst.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainWindow", u"Recommendation:", None))
    # retranslateUi


    #CustomFunctions
    def predict(self, antecedent, rules=rules_Por, max_results=10):
        # get the rules for this antecedent
        temp = set()
        temp.add(antecedent)
        preds = rules[rules['antecedents'] == temp]
        try:
            self.value = preds['confidence'].iloc[:max_results].unique().mean()
        finally:
            pass
        # a way to convert a frozen set with one element to string
        preds = preds['consequents'].apply(iter).apply(next)
        return preds.iloc[:max_results].unique()

    def item_clicked(self):
        select = self.ItemLst.currentItem().text()
        self.PredictLst.clear()
        recommendations = self.predict(select)
        for index, recommendation in enumerate(recommendations):
            self.PredictLst.insertItem(index, recommendation)
        self.PredictLst.insertItem(self.PredictLst.count() + 1, '')
        if self.value == 1.0:
            self.PredictLst.insertItem(self.PredictLst.count() + 1, f'Confidence Level: 0.25')
        elif math.isnan(self.value)==True:
            self.PredictLst.insertItem(self.PredictLst.count() + 1, f'Confidence Level: N/A')
        else:
            self.PredictLst.insertItem(self.PredictLst.count() + 1, f'Confidence Level: {self.value}')

    def searchtxt_changed(self):
        if not self.ItemTxbx.text():
            for index, item in enumerate(items):
                self.ItemLst.insertItem(index, item)
        else:
            text = self.ItemTxbx.text()
            results = process.extract(text, items, limit=50)
            self.ItemLst.clear()
            for index, result in enumerate(results):
                self.ItemLst.insertItem(index, result[0])
    def reset_clicked(self):
        for index, item in enumerate(items):
            self.ItemLst.insertItem(index, item)
        self.ItemTxbx.setText('')
        self.PredictLst.clear()


