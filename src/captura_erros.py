import types

def aplicar_decorador_em_todas(funcoes, decorador):
    for nome, obj in funcoes.items():
        if isinstance(obj, types.FunctionType):  # só funções normais
            funcoes[nome] = decorador(obj)

def captura_erros(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERRO] na função {func.__name__}: {e}")
            input("Aperte qualquer tecla pra fechar essa janela: ...")
            raise
    return wrapper
