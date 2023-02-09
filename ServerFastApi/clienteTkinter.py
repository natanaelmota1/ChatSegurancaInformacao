import tkinter as tk

def send_message():
    message = input_field.get()
    chat_log.config(state='normal')
    chat_log.insert('end', 'Você: ' + message + '\n')
    chat_log.config(state='disabled')
    input_field.delete(0, 'end')

root = tk.Tk()
root.title("Chat")
root.geometry("400x500")

chat_log = tk.Text(root, state='disabled')
chat_log.pack(fill='both', expand=True)

input_frame = tk.Frame(root)
input_frame.pack(side='bottom', fill='x')

input_field = tk.Entry(input_frame)
input_field.pack(fill='x', padx=10, pady=10)

send_button = tk.Button(input_frame, text='Enviar', command=send_message)
send_button.pack(side='right', padx=10, pady=10)

root.mainloop()
