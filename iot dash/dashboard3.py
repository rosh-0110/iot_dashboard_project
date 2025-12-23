import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from scapy.all import ARP, Ether, srp

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connected ESP Devices Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Connected ESP Devices:")
        self.device_list = QListWidget()
        self.refresh_button = QPushButton("Refresh")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.device_list)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        self.refresh_button.clicked.connect(self.refresh_devices)
        self.refresh_devices()

    def refresh_devices(self):
        self.device_list.clear()
        devices = self.get_connected_devices()
        for device in devices:
            self.device_list.addItem(device)

    def get_connected_devices(self):
        devices = []
        try:
            target_ip = "192.168.137.1/24"  # Change this to your network's IP range
            arp = ARP(pdst=target_ip)
            ether = Ether(dst="bc:dd:c2:fd:e9:74")
            packet = ether/arp
            result = srp(packet, timeout=3, verbose=0)[0]

            for sent, received in result:
                mac_address = received.hwsrc
                ip_address = received.psrc
                if self.is_esp_device(mac_address):
                    devices.append(f"IP: {ip_address} - MAC: {mac_address}")
        except Exception as e:
            print(f"Error retrieving devices: {e}")
        return devices

    def is_esp_device(self, mac_address):
        esp_prefixes = [
            "30:AE:A4",  # ESP32
            "bc:dd:c2",  # ESP8266
            "fd:e9:74",  # ESP8266
            "5C:CF:7F",  # ESP32
            "cc:7b:5c",  # ESP32
            "35:eb:f0",  # ESP32
        ]
        return any(mac_address.startswith(prefix) for prefix in esp_prefixes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
