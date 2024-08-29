import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import time ,glob

def is_whatsapp_running(window_title):
    return any(window.title == window_title for window in gw.getWindowsWithTitle(window_title))

def get_permission():
    while True:
        response = input("Allow recording WhatsApp window? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Invalid input. Please enter 'y' for Yes or 'n' for No.")

if __name__ == "__main__":
    window_title = "WhatsApp"  # Title of the WhatsApp window

    while True:
        if is_whatsapp_running(window_title):
            if get_permission():
                output_filename = "whatsapp_recording.avi"  # Output filename

                window = gw.getWindowsWithTitle(window_title)
                if not window:
                    print(f'Window with title "{window_title}" not found.')
                    break
                
                window = window[0]
                bbox = (window.left, window.top, window.width, window.height)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_filename, fourcc, 20, (bbox[2], bbox[3]))

                while is_whatsapp_running(window_title):
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
        time.sleep(1)  # Check every second if WhatsApp is running

    if glob.glob("*.avi"):
        from Soi import Manalyze

        query = Manalyze('whatsapp_recording.avi')
        outt = query.main()
        if type(outt) == type(" "):
            print(outt)
        else: 
            print(outt[2])
           

