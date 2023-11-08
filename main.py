from tkinter import *
from PIL import Image, ImageTk
from datetime import date
from tkinter import messagebox
import base64

window = Tk()
window.title("Secret Notes")
window.minsize(width=400, height=700)
window.config(pady=5, padx=5)

# Load the image
image = Image.open("topsecret1.png")

# Resize the image in the given (width, height)
img = image.resize((int(433/2), int(280/2)))
logo = ImageTk.PhotoImage(img)
label_img = Label(image=logo)
label_img.pack()
'''
canvas = Canvas(height=200, width=200)
logo = ImageTk.PhotoImage(img)
canvas.create_image(100, 100, image=logo)
canvas.pack()
'''
label_title = Label(text="Title")
label_title.pack()

entry_title = Entry()
entry_title.config(width=20)
entry_title.pack()

label_note = Label(text="Note")
label_note.pack()

note = Text()
note.pack()

label_key = Label(text="Secret Key")
label_key.pack()

entry_key = Entry()
entry_key.config(width=20)
entry_key.pack()
def encrypt(key, note):
    enc = []
    for i in range(len(note)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(note[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def encrypt_save():
    title = entry_title.get()
    clear_note = note.get("1.0", END)
    key = entry_key.get()
    if len(title) == 0 or len(clear_note) == 0 or len(key) == 0:
        messagebox.showinfo(title="Warning", message="Please enter all fields")
    else:
        encText = encrypt(key, clear_note)
        entry_title.delete(0, END)
        entry_key.delete(0, END)
        note.delete("1.0", END)
        save(title, encText)

    entry_title.focus()
def save(title, enctext):
    with open('notes.txt', 'a') as file:
        file.write(f"{title} : {date.today()} \n")
        file.write(f"{enctext} \n")
        messagebox.showinfo(title="Information", message="Note encrypted and saved")

def decrypt():
    encrypted_note = note.get("1.0", END)
    key = entry_key.get()
    if len(encrypted_note) == 0 or len(key) == 0:
        messagebox.showinfo(title="Warning", message="Please enter key and note fields")
    else:
        dec = []
        enc = base64.urlsafe_b64decode(encrypted_note).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        decrypted_note = "".join(dec)
        note.delete("1.0", END)
        note.insert("1.0", decrypted_note)
        messagebox.showinfo(title="Information", message="Note decrypted")
button_encrypt = Button(text="Encrypt & Save", command=encrypt_save)

button_encrypt.pack()

button_encrypt = Button(text="Decrypt", command=decrypt)
button_encrypt.pack()

entry_title.focus()
window.mainloop()