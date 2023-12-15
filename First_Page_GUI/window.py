
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from customtkinter import *
from tkinter import messagebox
import cv2
import os
from PIL import Image, ImageTk
import openpyxl


def btn_clicked():
    print("Button Clicked")

def on_enter(e):
    e.widget['background'] = '#84756B'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'




def create_window1():
    window = tk.Toplevel()
    #window = tk.Tk()
    window.title("Login Form")
    # window.geometry("800x600")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d" % (w, h))
    window.configure(bg="#F2E9EA")
    frame = tk.Frame(window, bg="#F2E9EA")
    # window.attributes('-full screen', True)
    frame.pack()
    # Create and start the SelfieApp
    with SelfieApp(window, "D:\\download\\projectfinal\\tend.jpg") as selfie_app:
        window.mainloop()
        print(selfie_app.username)



def create_window2():
    window2 = tk.Toplevel()
    window2.title("Class Attendance")
    label = Label(window2, text='Class of Today', justify=tk.LEFT, bg="#F2E9EA", font=28)
    label.pack(pady=20)

    def load_data():
        path = "D:\\download\\projectfinal\\attendance.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        list_values = list(sheet.values)
        cols = list_values[0]
        tree = ttk.Treeview(frame, column=cols, show="headings")
        for col_name in cols:
            tree.heading(col_name, text=col_name)
        tree.pack(expand=True, fill='y')

        for value_tuple in list_values[1:]:
            tree.insert('', tk.END, values=value_tuple)

    frame =Frame(window2)
    frame.pack(pady=100)
    #tree = ttk.Treeview(frame)
    load_data()
    w, h = window2.winfo_screenwidth(), window2.winfo_screenheight()
    window2.geometry("%dx%d" % (w, h))
    window2.configure(bg="#F2E9EA")
    #window2.set_background("D:\\download\\projectfinal\\tend.jpg")
    #background_img = PhotoImage(file=f"D:\\download\\projectfinal\\tend.jpg")
    #background = canvas.create_image(image=background_img)

    window2.mainloop()




class SelfieApp:
    def __init__(self, window , bg_image_path):
        self.window = window
        self.window.title("Selfie App")

        # set background Image
        self.set_background(bg_image_path)

        # open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            tk.messagebox.showerror("Error", "Unable to open the camera. Exiting.")
            self.window.destroy()
            return

        # Create a canvas to display the selfie
        self.canvas = tk.Canvas(window, width=640, height=480, highlightthickness=0)
        self.canvas.pack(pady=13)

        font2 = CTkFont(size=30, weight="bold", slant='italic')
        # Button to capture selfie
        self.btn_capture = CTkButton(master=window, text="Capture", text_color="#5B3256", font=font2, bg_color="#8793A1",
                                     corner_radius=50, hover_color="#563C5C", fg_color="#F2E9EA",
                                     command=self.capture_selfie)
        self.btn_capture.pack(pady=0)
        self.img = None

        # Button to close application
        self.btn_try_again = CTkButton(master=window, text="Try Again", text_color="#5B3256", font=font2, corner_radius=50,
                                  hover_color="#563C5C", fg_color="#F2E9EA", command=self.try_again)
        self.btn_try_again.pack(side="right", padx=40 , pady=10)

        # Start updating the display
        self.update()

    def set_background(self, image_path):
        # Load the image
        bg_image = Image.open("D:\\download\\projectfinal\\tend.jpg")  # Replace with your image file path
        bg_image = ImageTk.PhotoImage(bg_image)

        # to resize the img
        # Open the image and resize it
        original_image = Image.open(image_path)
        resized_image = original_image.resize((1500, 750))

        # Convert the resized image to a PhotoImage
        bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to display the background image
        bg_label = tk.Label(self.window, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Ensure that the label persists
        bg_label.image = bg_image

        # Create a login label
        login_label = tk.Label(self.window, text="JOIN CLASS", fg="#5B3256", bg="#F2E9EA", font='times 50 bold italic')
        login_label.pack(pady=20)

        # create a username label
        username_label = tk.Label(self.window, text="Username:", bg="#F2E9EA", fg="#5B3256",
                                  font='times 25 bold italic')
        username_label.pack(pady=0)


        # create a entry label
        self.username_entry = tk.Entry(self.window, width=23, font=30, fg="#5B3256")
        self.username_entry.pack(pady=5)


        # Ensure that the labels persist
        login_label.image = bg_image
        username_label.image = bg_image
        self.username_entry.image = bg_image

    def capture_selfie(self):
        self.captured = True
        ret, frame = self.cap.read()
        # frame = cv2.resize(frame, 100, fx=0.1, fy=0.1)


        # Check if the frame is valid
        if not ret:
            tk.messagebox.showerror("Error", "Unable to capture selfie.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(frame_rgb)
        # Save the captured selfie
        self.photo = ImageTk.PhotoImage(image=self.img)

        self.username = self.username_entry.get()
        # path = 'E:/FaceRecognitionProject/ImageAttendance'
        # self.img.save(os.path.join(path, f"{self.username}.jpg"))

        # Update the canvas with the captured selfie
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        self.canvas.image = self.photo

        self.submit_selfie()


    def submit_selfie(self):
        if self.img is not None:
            # Save the captured selfie to a file
            # self.username = self.username_entry.get()
            path = 'E:/FaceRecognitionProject/ImageAttendance'
            #self.img.save(os.path.join(path, f"{self.username}.jpg"))
            self.canvas = os.path.join(path, f"{self.username}.jpg")
            self.img.save(self.canvas)


            os.startfile(self.canvas)



    def update(self):
        ret, frame = self.cap.read()
        # print(frame.shape)

        # Check if the frame is valid
        if not ret:
            tk.messagebox.showerror("Error", "Unable to read camera frame.")
            self.window.destroy()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = ImageTk.PhotoImage(image=img)

        # Update the canvas with the latest frame

        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas.image = img

        # Repeat the update after 10 milliseconds
        self.window.after(10, self.update)

    def try_again(self):
        # Get the username entered by the user
        username = self.username_entry.get()

        # Delete the saved picture by the username
        path_to_delete = os.path.join('E:/FaceRecognitionProject/ImageAttendance', f"{username}.jpg")
        if os.path.exists(path_to_delete):
            os.remove(path_to_delete)

        # Delete the captured selfie
        self.img = None

        # Update the canvas to open the camera again
        self.update()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Release the camera when the application is closed
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()




#main first window
window1=Tk()

window1.geometry("842x524")
window1.configure(bg = "#edf6f9")
canvas = Canvas(
    window1,
    bg = "#edf6f9",
    height = 524,
    width = 842,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    421.0, 262.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = create_window2,
    relief = "flat")

b0.place(
    x = 78, y = 363,
    width = 251,
    height = 53)

b0.bind("<Enter>", on_enter)
b0.bind("<Leave>", on_leave)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = create_window1,
    relief = "flat")

b1.place(
    x = 78, y = 274,
    width = 251,
    height = 53)

b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

window1.resizable(False, False)
window1.mainloop()