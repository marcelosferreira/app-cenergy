import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tela com Scrollbar")

# Crie uma frame para conter o Text widget e a barra de rolagem
frame = ttk.Frame(root, width=300, height=200)
frame.pack()

# Crie uma barra de rolagem vertical
scrollbar = ttk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Crie um Text widget e associe-o à barra de rolagem
text_widget = tk.Text(frame, wrap="none", yscrollcommand=scrollbar.set)
text_widget.pack(fill="both", expand=True)

# Configure a barra de rolagem para controlar o Text widget
scrollbar.config(command=text_widget.yview)

# Adicione algum texto ao Text widget
lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque ac nisl vel quam efficitur lacinia. Donec in tortor
et justo vehicula sodales. Sed hendrerit odio id libero bibendum, 
in fermentum tellus volutpat. Nam vel erat id purus feugiat cursus 
non ac elit. Integer id malesuada purus, non mattis libero. Sed eu 
consequat purus. Proin malesuada odio eget lectus tempor, nec 
volutpat felis interdum. Morbi suscipit tristique aliquet. Nullam
at urna a purus venenatis tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque ac nisl vel quam efficitur lacinia. Donec in tortor
et justo vehicula sodales. Sed hendrerit odio id libero bibendum, 
in fermentum tellus volutpat. Nam vel erat id purus feugiat cursus 
non ac elit. Integer id malesuada purus, non mattis libero. Sed eu 
consequat purus. Proin malesuada odio eget lectus tempor, nec 
volutpat felis interdum. Morbi suscipit tristique aliquet. Nullam
at urna a purus venenatis tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque ac nisl vel quam efficitur lacinia. Donec in tortor
et justo vehicula sodales. Sed hendrerit odio id libero bibendum, 
in fermentum tellus volutpat. Nam vel erat id purus feugiat cursus 
non ac elit. Integer id malesuada purus, non mattis libero. Sed eu 
consequat purus. Proin malesuada odio eget lectus tempor, nec 
volutpat felis interdum. Morbi suscipit tristique aliquet. Nullam
at urna a purus venenatis tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque ac nisl vel quam efficitur lacinia. Donec in tortor
et justo vehicula sodales. Sed hendrerit odio id libero bibendum, 
in fermentum tellus volutpat. Nam vel erat id purus feugiat cursus 
non ac elit. Integer id malesuada purus, non mattis libero. Sed eu 
consequat purus. Proin malesuada odio eget lectus tempor, nec 
volutpat felis interdum. Morbi suscipit tristique aliquet. Nullam
at urna a purus venenatis tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque ac nisl vel quam efficitur lacinia. Donec in tortor
et justo vehicula sodales. Sed hendrerit odio id libero bibendum, 
in fermentum tellus volutpat. Nam vel erat id purus feugiat cursus 
non ac elit. Integer id malesuada purus, non mattis libero. Sed eu 
consequat purus. Proin malesuada odio eget lectus tempor, nec 
volutpat felis interdum. Morbi suscipit tristique aliquet. Nullam
at urna a purus venenatis tincidunt."""

text_widget.insert("1.0", lorem_ipsum)

root.mainloop()
