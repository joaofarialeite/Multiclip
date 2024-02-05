from tkinter import Tk, Frame, BOTH, Menu, TclError, Label, RAISED, SUNKEN, SOLID, messagebox, Toplevel, Entry,Button, simpledialog,PhotoImage
import pyperclip


# VARIAVEIS A USAR GLOBALMENTE
text_clipboard = []
i=0
max_labels = 10

# Definir as dimensões mínimas da janela
min_width = 300
min_height = 200

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

def apply_custom_style(label):
    label.config(
        # borderwidth=3, 
        # relief="raised", 
        # pady=5, 
        wraplength=label.winfo_reqwidth()
        # background="#E1EFFF", 
        # foreground="#000080", 
        # font=("Helvetica", 12)
    )

def change_labels_size():

    global max_labels
    
    while True:
        new_size = simpledialog.askinteger("Change Labels Size", f"Current max labels: {max_labels} |  Max labels possible: 15\n{' '*27}Enter new size:", initialvalue=max_labels,parent=root)

        if new_size > 0:

            if new_size <=  15 : #(root.winfo_screenheight() / 2):
                max_labels = new_size
                messagebox.showinfo("Success", f"Max labels set to: {max_labels}", 
                                    parent=root) # serve para colocar a box no mesmo sitio que a box que a criou
                break
            else:
                messagebox.showerror("Error", "Labels size too large. Please choose a smaller size.",parent=root)
                continue
        else:
            messagebox.showerror("Error", "Please enter a valid positive integer.")
            continue

def clearAll():
    result = messagebox.askyesno("Clear All", "Are you sure you want to clear all clippings from the application?", icon='warning')
    if result:
        # Limpar a lista text_clipboard
        text_clipboard.clear()

    for widget in root.winfo_children():
        # Verificar se o widget é um menu
        if widget.winfo_class() == "Menu":
            continue  # Ignorar o menu
        widget.destroy()


def copy_label_content(text):

    pyperclip.copy(text)

def invoca_update():

    update_clipboard(1)

def update_clipboard(event):
    global i
    i+=1

    text_clipboard.append((root.clipboard_get(),i))
    print(text_clipboard)


    # if text_clipboard[0][0] == pyperclip.paste():
    #     return


    for widget in root.winfo_children():

        if widget.winfo_class() == "Menu":
            continue
        widget.destroy()

    text_clipboard.reverse()

    max_width = 0
    total_height = 0

    for tuplo in text_clipboard[:max_labels]:
        new_label = Label(root, text=tuplo[0], relief=RAISED, pady=5)
        new_label.config( wraplength=new_label.winfo_reqwidth())
        #apply_custom_style(new_label)
        new_label.pack()

        # Adiciona a função de cópia ao clicar na label
        new_label.bind("<Button-1>", lambda event, text=new_label["text"]: copy_label_content(text))

        # Atualizar as dimensões máximas
        max_width = max(max_width, new_label.winfo_reqwidth())
        total_height += new_label.winfo_reqheight()

    max_width = max(max_width, min_width)
    total_height = max(total_height, min_height)

    # Para nao ser maior que o monitor
    total_height = min(total_height, (root.winfo_screenheight() / 2))
    max_width = min(max_width, (root.winfo_screenwidth()))

    center_window(root,max_width,total_height)
    root.after(ms=10000, func=invoca_update)




#WINDOW
root = Tk()
root.title('MultiClip')
icon_image = PhotoImage(file='/Users/jfl/Desktop/Clippy/multiclip.png')
root.iconphoto(True, icon_image)
root.wm_iconbitmap('/Users/jfl/Desktop/Clippy/multiclip.ico')
root.geometry(f"{min_width}x{min_height}")

#Centrar a window
center_window(root,min_width,min_height)

#MENU DA WINDOW
menubar = Menu(root)
root.config(menu=menubar)
optionsMenu = Menu(menubar)
optionsMenu.add_command(label="Clear All",command= clearAll)
optionsMenu.add_command(label="Labels size",command= change_labels_size)
menubar.add_cascade(label="Options",menu= optionsMenu)



#TECLA QUE VAI ATUALIZAR A WINDOW
root.bind('<Button-1>', update_clipboard)

#INICIAR A WINDOW
root.mainloop()





# def change_labels_size():
#     # Janela de configuração para definir o número máximo de labels
#     config_window = Toplevel(root)
#     config_window.title("Change Labels Size")

#     # Label informativa
#     info_label = Label(config_window, text=f"Current max labels: {max_labels}")
#     info_label.pack()

#     # Entrada para o novo tamanho
#     new_size_entry = Entry(config_window)
#     new_size_entry.pack()

#     # Botão para aplicar as alterações
#     apply_button = Button(config_window, text="Apply", command=lambda: apply_label_size(new_size_entry.get(), config_window))
#     apply_button.pack()
# def apply_label_size(new_size, config_window):
#     global max_labels
#     try:
#         new_size = int(new_size)
#         if new_size > 0:
#             max_labels = new_size
#             messagebox.showinfo("Success", f"Max labels set to: {max_labels}")
#         else:
#             messagebox.showerror("Error", "Please enter a valid positive integer.")
#     except ValueError:
#         messagebox.showerror("Error", "Please enter a valid positive integer.")

#     config_window.destroy()

#alteracoes