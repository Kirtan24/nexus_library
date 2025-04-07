from tkinter import Tk, PhotoImage
from app.config import APP_NAME
from app.app import App

def main():
    root = Tk()
    root.title(APP_NAME)

    try:
        icon_path = "assets/logo/logo.png"
        icon = PhotoImage(file=icon_path)
        root.iconphoto(False, icon)
    except Exception as e:
        print(f"Error loading icon: {e}")

    root.state("zoomed")

    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()