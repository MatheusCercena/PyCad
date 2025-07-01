import win32com.client

def get_acad():
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application").ActiveDocument
        return acad, acad.ModelSpace
    except Exception as erro:
        raise RuntimeError("Erro ao conectar com o AutoCAD") from erro

