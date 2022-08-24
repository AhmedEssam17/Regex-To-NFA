import tkinter as tk

from PIL import Image, ImageTk
import FA


class NfaPage(tk.Frame):
    regex = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Middle Page Label
        border = tk.LabelFrame(self, bg="white")
        border.pack(fill="both", expand="yes", padx=0, pady=0)
        label = tk.Label(self, text="Regex-to-NFA", font=("Arial Bold", 20), bg="#FFD6EA")
        label.place(x=310, y=20)

        entryLabel = tk.Label(self, text="Regular Expression Entry", font=("Arial black", 18), bg="#FFD6EA")
        entryLabel.place(x=50, y=100)

        global entryBox
        entryBox = tk.Entry(self, width=30, bd=5, font=("Arial", 18))
        entryBox.place(x=50, y=150)

        def convert2fa():
            NfaPage.regex = entryBox.get()

            a = FA.Regex2NFA(self.regex)
            a.create_nfa()
            nfa = Image.open('nfa.gv.png')
            nfa = ImageTk.PhotoImage(nfa)

            global nfa_label
            nfa_label = tk.Label(image=nfa)
            nfa_label.image = nfa
            nfa_label.place(x=50, y=300)

        # Converts entered Regex to NFA and displays it
        convertButton = tk.Button(self, text="Convert & Display NFA", font=("Arial", 18),
                            command=lambda: convert2fa(), bg="#FD3294")
        convertButton.place(x=500, y=150)

        # Resets entry box and deletes previously generated NFA
        resetButton = tk.Button(self, text="Reset", font=("Arial", 18),
                              command=lambda: self.reset(), bg="#FD3294")
        resetButton.place(x=500, y=200)

    def reset(self):
        entryBox.delete(0, 'end')
        nfa_label.place_forget()



class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating a window
        window = tk.Frame(self, bg='#111111')
        window.pack()

        window.grid_rowconfigure(0, minsize=600)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for f in [NfaPage]:
            frame = f(window, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.display_frame(NfaPage)

    def display_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


if __name__ == '__main__':
    win = Gui()
    win.title("Regex-to-NFA")
    win.mainloop()




