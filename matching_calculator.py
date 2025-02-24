import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QComboBox, QGridLayout
from PyQt6.QtGui import QPixmap
from math import sqrt
PI = 3.14

class MatchingNetworkApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matching Network Calculator")
        self.setGeometry(400, 250, 500, 570)

        layout = QGridLayout()

        # Zin
        self.labelZin = QLabel("Zin:")
        self.lineEditZin = QLineEdit()
        layout.addWidget(self.labelZin,0,0)
        layout.addWidget(self.lineEditZin,0,1)

        # Rl
        self.labelRl = QLabel("Rl:")
        self.lineEditRl = QLineEdit()
        layout.addWidget(self.labelRl,1,0)
        layout.addWidget(self.lineEditRl,1,1)

        # Frequency
        self.labelFrequency = QLabel("Frequency(Hz):  ")
        self.lineEditFrequency = QLineEdit()
        layout.addWidget(self.labelFrequency,2,0)
        layout.addWidget(self.lineEditFrequency,2,1)

        # Q
        self.labelQ = QLabel("Q:")
        self.lineEditQ = QLineEdit()
        layout.addWidget(self.labelQ,3,0)
        layout.addWidget(self.lineEditQ,3,1)
        self.labelQ.hide()
        self.lineEditQ.hide()

        # Circuit Type
        self.labelCircuitType = QLabel("Circuit Type:")
        self.comboBox = QComboBox()
        self.comboBox.addItem("L")
        self.comboBox.addItem("Pi")
        self.comboBox.addItem("T")
        layout.addWidget(self.labelCircuitType,4,0)
        layout.addWidget(self.comboBox,4,1)

        #Type
        self.labelType = QLabel("Type:")
        self.comboBoxType = QComboBox()
        self.comboBoxType.addItem("DC Feed")
        self.comboBoxType.addItem("DC Block")
        layout.addWidget(self.labelType,5,0)
        layout.addWidget(self.comboBoxType,5,1)

        # Calculate Button
        self.buttonCalculate = QPushButton("Calculate")
        layout.addWidget(self.buttonCalculate,6,0,1,2)

        # Result
        self.labelResult = QLabel("Result:")
        layout.addWidget(self.labelResult,7,0)

        # Result Textbox
        self.textBrowserResult = QLineEdit()
        layout.addWidget(self.textBrowserResult,7,1)
        
        # Image
        self.labelImage = QLabel()
        layout.addWidget(self.labelImage,8,0,1,2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Connect button click events to functions
        self.buttonCalculate.clicked.connect(self.calculate)

        # Connect ComboBox currentIndexChanged event to function
        self.comboBox.currentIndexChanged.connect(self.show_hide_q_input)

    def show_hide_q_input(self):
        # Show/Hide Q input based on selected circuit type
        if self.comboBox.currentIndex() == 1 or self.comboBox.currentIndex() == 2:  # Pi Section or T Section
            self.labelQ.show()
            self.lineEditQ.show()
        else:
            self.labelQ.hide()
            self.lineEditQ.hide()

    def calculate(self):  
        # Get user inputs
        Zin_text = self.lineEditZin.text()
        Rl_text = self.lineEditRl.text()
        f_text = self.lineEditFrequency.text()
        Q_text = self.lineEditQ.text()

        # Check if any input field is empty
        if not (Zin_text and Rl_text and f_text):
            self.textBrowserResult.setText("Nhập thiếu giá trị, mời bạn nhập lại")
            self.labelImage.clear()
            return

        # Check if Q is required but not provided
        if self.comboBox.currentIndex() in [1, 2] and not Q_text:
            self.textBrowserResult.setText("Nhập thiếu giá trị, mời nhập lại")
            self.labelImage.clear()
            return

        # Convert inputs to appropriate type and check values
        try:
            Zin = complex(Zin_text)
            Rl = float(Rl_text)
            f = float(f_text)
            type_index = self.comboBoxType.currentIndex()
            circuit_type_index = self.comboBox.currentIndex()
            if circuit_type_index == 1 or circuit_type_index == 2:
                Q = float(Q_text)
        except ValueError:
            self.textBrowserResult.setText("Nhập sai định dạng đầu vào, mời nhập lại")
            self.labelImage.clear()
            return
        
        RE_Zin = Zin.real
        w = 2 * PI * f
        
        if RE_Zin == Rl:
            self.textBrowserResult.setText("Nhập sai định dạng đầu vào, mời nhập lại")
            self.labelImage.clear()
            return
        if circuit_type_index == 0:  # L Section
            self.calculate_L_section(RE_Zin, Rl, w, type_index)
        elif circuit_type_index == 1:  # Pi Section
            self.calculate_Pi_section(RE_Zin, Rl, Q, w, type_index)
        elif circuit_type_index == 2:  # T Section
            self.calculate_T_section(RE_Zin, Rl, Q, w, type_index)

    def calculate_L_section(self, RE_Zin, Rl, w, type_index):
        if RE_Zin < Rl:
            Q = sqrt(Rl/RE_Zin - 1)
        elif RE_Zin > Rl:
            Q = sqrt(RE_Zin/Rl - 1)
            
        # Calculate L and C values
        if type_index == 0:  # DC Feed
            if RE_Zin < Rl:
                C = Q / (w * Rl)
                Cs = C * (Q * Q + 1) / (Q * Q)
                L = 1 / (w * w * Cs)
                pixmap = QPixmap("images/L_dc_feed_a.png")
            else:
                C = Q / (RE_Zin * w)
                L = (Q * Rl) / w
                pixmap = QPixmap("images/L_dc_feed_b.png")
        elif type_index == 1:  # DC Block
            if RE_Zin < Rl:
                L = Rl / (Q * w)
                Ls = L * (Q * Q) / (Q * Q + 1)
                C = 1 / (w * w * Ls)
                pixmap = QPixmap("images/L_dc_block_a.png")
            else:
                L = RE_Zin / (Q * w)
                C = 1 / (Q * Rl * w)
                pixmap = QPixmap("images/L_dc_block_b.png")
        # Update result in text browser
        result_text = f"C = {C:.2e}(F);  L = {L:.2e}(H)"
        self.textBrowserResult.setText(result_text)
        self.labelImage.setPixmap(pixmap)
        
    def calculate_Pi_section(self, Rs, Rl, Q, w, type_index):
        Rhigher = max ( Rs, Rl)
        Rlower = min (Rs, Rl)
        Rvirtual = Rhigher / (Q*Q+1)
        Xp2 = Rhigher / Q
        Xs2 = Q * Rvirtual
        Q1 = sqrt(Rlower / Rvirtual - 1)
        Xp1 = Rlower / Q1
        Xs1 = Rvirtual * Q1
        Xs = Xs1 + Xs2
        
        if type_index == 0: #DC Feed
            if Rl > Rs: 
                Zc1, Zl, Zc2 = Xp1, Xs, Xp2
            else:
                Zc2, Zl, Zc1 = Xp1, Xs, Xp2
            C1 = 1/ (Zc1 * w)
            L = Zl / w
            C2 = 1 / (Zc2 * w)
            result_text = f"C1 = {C1:.2e}(F); L = {L:.2e}(H); C2 = {C2:.2e}(F)"
            pixmap = QPixmap("images/PI_DC_FEED.png")
        elif type_index == 1: #DC Block
            if Rl > Rs: 
                Zl1, Zc, Zl2 = Xp1, Xs, Xp2
            else:
                Zl2, Zc, Zl1 = Xp1, Xs, Xp2
            L1 = Zl1 / w
            C = 1 / (Zc * w)
            L2 = Zl2 / w
            result_text = f"L1 = {L1:.2e}(H); C = {C:.2e}(F); L2 = {L2:.2e}(H)"
            pixmap = QPixmap("images/PI_DC_BLOCK.png")
        self.textBrowserResult.setText(result_text)
        self.labelImage.setPixmap(pixmap)
    
    def calculate_T_section(self, Rs, Rl, Q, w, type_index):
        Rhigher = max ( Rs, Rl)
        Rlower = min (Rs, Rl) 
        Rvirtual = Rlower * (Q*Q + 1)
        Xp1 = Rvirtual / Q
        Xs1 = Q * Rlower
        Q2 = sqrt (Rvirtual / Rhigher - 1)
        Xp2= Rvirtual / Q2
        Xs2 = Q2 * Rhigher
        Xs = Xs1 * Xs2 / (Xs1 + Xs2)
        
        if type_index == 0: #DC Feed
            if Rl > Rs:
                Zl1, Zc, Zl2 = Xp1, Xs, Xp2
            else:
                Zl2, Zc, Zl1 = Xp1, Xs, Xp2
            L1 = Zl1 / w
            C = 1 / (Zc * w)
            L2 = Zl2 / w
            result_text = f"L1 = {L1:.2e}(H); C = {C:.2e}(F); L2 = {L2:.2e}(H)"
            pixmap = QPixmap("images/T_DC_FEED.png")
        elif type_index == 1: #DC Block
            if Rl > Rs:
                Zc1, Zl, Zc2 = Xp1, Xs, Xp2
            else:
                Zc2, Zl, Zc1 = Xp1, Xs, Xp2
            C1 = 1/ (Zc1 * w)
            L = Zl / w
            C2 = 1 / (Zc2 * w)
            result_text = f"C1 = {C1:.2e}(F); L = {L:.2e}(H); C2 = {C2:.2e}(F)"
            pixmap = QPixmap("images/T_DC_BLOCK.png")
        self.textBrowserResult.setText(result_text)
        self.labelImage.setPixmap(pixmap)    
    
def main():
    app = QApplication(sys.argv)
    window = MatchingNetworkApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    