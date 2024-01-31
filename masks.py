import tkinter as tk

def mask_numeral(text): 
        # Remove todos os caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, text))
        mask_text = numeros

        return mask_text

def mask_porcentagem(text): 
        # Remove todos os caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, text))
        mask_text = "{}%".format(numeros[0:])

        return mask_text

def mask_coordenadas(text): 
        # Remove todos os caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, text))

        # Formata o número como (-)X.XXXX ou (-)XX.XXXX ou (-)X.XXXXXX ou (-)XX.XXXXXX 
        if len(text)>0 and len(numeros)<5:
            if text[0] == '-':
                mask_text = "-{}".format(numeros[0:4])
            else:
                mask_text = numeros
        elif len(numeros) == 5:
            if text[0] == '-':
                mask_text = "-{}.{}".format(numeros[:1], numeros[1:5])
            else:
                mask_text = "{}.{}".format(numeros[:1], numeros[1:5])
        elif len(numeros) == 6:
            if text[0] == '-':
                mask_text = "-{}.{}".format(numeros[:2], numeros[2:6])
            else:
                mask_text = "{}.{}".format(numeros[:2], numeros[2:6])
        elif len(numeros) == 7:
            if text[0] == '-':
                mask_text = "-{}.{}".format(numeros[:1], numeros[1:7])
            else:
                mask_text = "{}.{}".format(numeros[:1], numeros[1:7])
        elif len(numeros) >= 8:
            if text[0] == '-':
                mask_text = "-{}.{}".format(numeros[:2], numeros[2:8])
            else:
                mask_text = "{}.{}".format(numeros[:2], numeros[2:8])
        else:
            mask_text = numeros

        return mask_text

