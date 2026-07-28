from app import App
from database import criar_tabelas

criar_tabelas()

app = App()
app.mainloop()