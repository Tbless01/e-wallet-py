# from turtledemo.penrose import f
#
# import PySimpleGUI as simple
# import os.path
#
# # simple.Window(title="Hello World", layout=[[]], margins=(250, 150)).read()
#
# # layout = [
# #     [simple.Text("Hello from PySimpleGUI")],
# #     [simple.Button("OK")]
# # ]
# #
# # window = simple.Window("Demo", layout, margins=(250, 150))
# #
# # while True:
# #     event, values = window.read()
# #
# #     if event == "OK" or event == simple.WIN_CLOSED:
# #         break
# #
# # window.close()
#
# file_list_column = [
#     [
#         simple.Text("Image Folder"),
#         simple.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
#         simple.FolderBrowse(),
#     ],
#
#     [
#         simple.Listbox(
#             values=[], enable_events=True, size=(40, 20),
#             key="-FILE LIST-"
#         )
#     ],
# ]
#
# image_viewer_column = [
#     [simple.Text("Choose an image from the list on the left: ")],
#     [simple.Text(size=(40, 1), key="-TOUT-")],
#     [simple.Image(key="-IMAGE-")],
# ]
#
# layout = [
#     [
#         simple.Column(file_list_column),
#         simple.VSeparator(),
#         simple.Column(image_viewer_column),
#     ]
# ]
#
# window = simple.Window("Image Viewer", layout)
#
# while True:
#     event, values = window.read()
#     if event == "EXIT" or event == simple.WIN_CLOSED:
#         break
#     if event == "-FOLDER-":
#         folder =values["-FOLDER"]
#         try:
#             file_list = os.listdir(folder)
#
#         except:
#             file_list = []
#
#         fnames = [
#             f
#             for file in file_list
#             if os.path.isfile(os.path.join(folder, f))
#             and f.lower().endswith((".png", ".gif"))
#         ]
#         window["-FILE LIST-"].update(fnames)
#     elif event == "-FILE LIST-":
#         try:
#             filename = os.path.join(
#                 values["-FOLDER-"], values["-FILE LIST"][0]
#             )
#             window["-TOUT-"].update(filename=filename)
#         except:
#             pass
#
#
#
