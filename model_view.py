import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

class PermissionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Permissions")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("Allow recording WhatsApp window?")
        layout.addWidget(label)

        allow_button = QPushButton("Allow")
        allow_button.clicked.connect(self.accept)
        layout.addWidget(allow_button)

        deny_button = QPushButton("Deny")
        deny_button.clicked.connect(self.reject)
        layout.addWidget(deny_button)

        self.setLayout(layout)

def is_whatsapp_active(window_title):
    return gw.getActiveWindowTitle() == window_title

if __name__ == "__main__":
    app = QApplication([])

    window_title = "WhatsApp"  # Title of the WhatsApp window
    permission_dialog = PermissionDialog()

    while True:
        if is_whatsapp_active(window_title):
            result = permission_dialog.exec()
            if result == QDialog.Accepted:
                output_filename = "whatsapp_recording.avi"  # Output filename

                window = gw.getWindowsWithTitle(window_title)
                if not window:
                    print(f'Window with title "{window_title}" not found.')
                    break
                
                window = window[0]
                bbox = (window.left, window.top, window.width, window.height)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_filename, fourcc, 20, (bbox[2], bbox[3]))

                while is_whatsapp_active(window_title):
                    img = pyautogui.screenshot(region=bbox)
                    frame = np.array(img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    out.write(frame)
                    time.sleep(1 / 20)

                out.release()
                cv2.destroyAllWindows()
            else:
                print("Recording denied.")
            break

    app.exit()
