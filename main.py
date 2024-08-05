import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setup_connections()

    def load_ui(self):
        """Charge le fichier UI pour la fenêtre principale."""
        uic.loadUi('main.ui', self)

    def setup_connections(self):
        """Configure les connexions des signaux et slots."""
        self.validatePushButton.clicked.connect(self.show_second_window)

    def show_second_window(self):
        """Crée et affiche la fenêtre secondaire, puis ferme la fenêtre principale."""
        tool_button_states = self.get_tool_button_states()
        self.second_window = SecondApp(tool_button_states)
        self.second_window.show()
        self.close()  # Ferme la fenêtre principale

    def get_tool_button_states(self):
        """Récupère les états des CheckBox dans la fenêtre principale."""
        states = {
            'fullpower': self.FullPowercheckBox.isChecked(),
            'lowbattery': self.LowBatterycheckBox.isChecked()
        }
        return states

class SecondApp(QMainWindow):
    def __init__(self, tool_button_states):
        super().__init__()
        self.load_ui()
        self.display_tool_button_states(tool_button_states)
        self.setup_connections()

    def load_ui(self):
        """Charge le fichier UI pour la fenêtre secondaire."""
        uic.loadUi('second.ui', self)

    def setup_connections(self):
        """Configure les connexions des signaux et slots pour la fenêtre secondaire."""
        self.startPushButton.clicked.connect(self.update_label_from_combobox)
        self.ecoModecomboBox.currentIndexChanged.connect(self.save_selected_item)

    def display_tool_button_states(self, states):
        """Met à jour les éléments de la fenêtre secondaire en fonction des états des CheckBox."""
        self.update_light(self.fullPowerLight, states['fullpower'])
        self.update_light(self.lowBatteryLight, states['lowbattery'])
        self.update_ecoModecomboBox(states)

    def update_light(self, label, state):
        """Met à jour l'image du label en fonction de l'état (vert pour actif, rouge pour inactif)."""
        if state:
            label.setPixmap(QtGui.QPixmap('images/green_light.png'))
        else:
            label.setPixmap(QtGui.QPixmap('images/red_light.png'))

    def update_ecoModecomboBox(self, states):
        """Met à jour les éléments de la ComboBox en fonction des états des CheckBox."""
        self.ecoModecomboBox.clear()  # Vide la ComboBox avant de la mettre à jour
        
        if states['fullpower']:
            self.add_fullpower_items(states['lowbattery'])
        else:
            self.add_no_fullpower_items(states['lowbattery'])

    def add_fullpower_items(self, lowbattery):
        """Ajoute les éléments de la ComboBox lorsque le mode 'fullpower' est activé."""
        self.ecoModecomboBox.addItem("OFF")
        self.ecoModecomboBox.addItem("Sleep")
        self.ecoModecomboBox.addItem("ECO 0")
        self.ecoModecomboBox.addItem("ECO 1")
        self.ecoModecomboBox.addItem("ECO 2")
        if lowbattery:
            self.ecoModecomboBox.addItem("Low Battery")

    def add_no_fullpower_items(self, lowbattery):
        """Ajoute les éléments de la ComboBox lorsque le mode 'fullpower' est désactivé."""
        self.ecoModecomboBox.addItem("OFF")
        self.ecoModecomboBox.addItem("Sleep")
        self.ecoModecomboBox.addItem("ECO 0")
        if lowbattery:
            self.ecoModecomboBox.addItem("Low Battery")

    def save_selected_item(self):
        """Sauvegarde l'élément sélectionné dans la ComboBox."""
        self.selected_item = self.ecoModecomboBox.currentText()

    def update_label_from_combobox(self):
        """Met à jour le QLabel avec l'élément sélectionné lorsque le bouton 'Push Start' est pressé."""
        if hasattr(self, 'selected_item'):
            self.selectedItemLabel.setText(f"{self.selected_item}")
        else:
            self.selectedItemLabel.setText("No ECO mode selected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
