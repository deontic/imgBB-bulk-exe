


import os
import sys
import requests
import threading
import validators
import tkinter as tk
from time import sleep
from tkinter import ttk
from bs4 import BeautifulSoup


# initialize dir

if(not os.path.exists("./imgout")):
    os.makedirs("./imgout")


# tkinter window
gui = tk.Tk()
gui.title("")
gui.iconbitmap(default="transparent.ico")

gui.geometry("400x300")


S = tk.Scrollbar(gui)
T = tk.Text(gui, height=4, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

T.configure(font=("Arial", 15))

s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 15))

button = ttk.Button(gui, text="Download",
                    command=lambda: main(), style="my.TButton")
button.pack(pady=10)
button.place(width=385, height=40, x=-1, y=260)

gui.resizable(False, False)


def exit():
    sleep(2)
    gui.destroy()
    sys.exit()


def main():

    urls = T.get("1.0", tk.END).split("\n")
    urls = list(filter(None, urls))

    print(urls)

    try:
        for url in urls:

            if not validators.url(url):
                continue

            response = requests.get(url)
            code = response.status_code

            if(code != 200):
                print(f"({code}) cannot download url at {url} ")
                continue

            html = response.text

            soup = BeautifulSoup(html, 'html.parser')
            container = soup.find(id="image-viewer-container")
            imgUrl = container.next_element.attrs["src"]
            imgName = container.next_element.attrs["alt"]

            response = requests.get(imgUrl)
            length = len(imgUrl)
            fileType = imgUrl[imgUrl.index(".", length-5):length]

            f = open("./imgout/"+imgName+fileType, "wb")
            f.write(response.content)
            f.close()

            # print(imgName)
            # print(imgUrl)
    except Exception as e:
        print(e)
        exit()

    def set():
        T.config(state=tk.NORMAL)
        T.delete(1.0, tk.END)
        T.insert(tk.END, "exiting...")
        exit()

    # use a thread to set it since gui.mainloop() blocks
    t = threading.Thread(target=set)
    # daemon to let thread abruptly stop at shutdown
    t.daemon = True
    t.start()


gui.mainloop()
