from tkinter import messagebox

class CoordenadasInvalidasError(Exception):
    pass

def validate_latitude(text,subcampo):
    text = text + 0.000001
    texto = str(text)
    numeros = ''.join(filter(str.isdigit, texto))
    if len(numeros)<5:
        raise CoordenadasInvalidasError(subcampo + ":\nAs coordenadas devem conter pelo menos 5 dígitos.")
    else:
        if text > 5.17:
            raise CoordenadasInvalidasError(subcampo + ":\nFavor inserir coordenadas situadas no território brasileiro.")
        elif text < -33.45:
            raise CoordenadasInvalidasError(subcampo + ":\nFavor inserir coordenadas situadas no território brasileiro.")