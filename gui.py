import PySimpleGUI as sg
import easygui as eg
import os.path
from PIL import Image, ImageFilter, ImageTk
from rembg import remove

sg.theme("DarkGreen3")

file_list_column = [
    [
        sg.Text("Image File"),
        sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
        sg.FileBrowse(),
    ],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-ACTION LIST-")],
]

image_viewer_column = [
    [sg.Button("Save"), sg.Button("Reset")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Editor", layout)
img = None

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FILE-":
        try:
            image_file_path = values["-FILE-"]
            if os.path.isfile(image_file_path) and image_file_path.lower().endswith(
                (".png", ".gif", ".jpg")
            ):
                window["-IMAGE-"].update(
                    filename=image_file_path,
                )
                img = Image.open(image_file_path)
                window["-ACTION LIST-"].update(
                    [
                        "EMBOSS",
                        "SHARPEN",
                        "FIND_EDGES",
                        "EDGE_ENHANCE",
                        "SMOOTH",
                        "BLUR",
                        "Grayscale",
                        "Remove background",
                    ]
                )
        except:
            pass
    elif event == "-ACTION LIST-":
        try:
            if values["-ACTION LIST-"][0] == "EMBOSS":
                img = img.filter(ImageFilter.EMBOSS)
            elif values["-ACTION LIST-"][0] == "SMOOTH":
                img = img.filter(ImageFilter.SMOOTH)
            elif values["-ACTION LIST-"][0] == "SHARPEN":
                img = img.filter(ImageFilter.SHARPEN)
            elif values["-ACTION LIST-"][0] == "FIND_EDGES":
                img = img.filter(ImageFilter.FIND_EDGES)
            elif values["-ACTION LIST-"][0] == "EDGE_ENHANCE":
                img = img.filter(ImageFilter.EDGE_ENHANCE)
            elif values["-ACTION LIST-"][0] == "Grayscale":
                img = img.convert("L")
            elif values["-ACTION LIST-"][0] == "BLUR":
                img = img.filter(ImageFilter.BLUR)
            elif values["-ACTION LIST-"][0] == "Remove background":
                img = remove(img)

            image = ImageTk.PhotoImage(image=img)
            window["-IMAGE-"].update(data=image)
        except:
            pass
    if event == "Save":
        try:
            output_path = eg.filesavebox(title="Save file to..")
            img.save(output_path)
        except:
            pass
    if event == "Reset":
        try:
            image_file_path = values["-FILE-"]
            img = Image.open(image_file_path)
            image = ImageTk.PhotoImage(image=img)
            window["-IMAGE-"].update(data=image)
        except:
            pass

window.close()
