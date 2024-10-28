
def z(n):
    alf = list("абвгдеёжзиёклмнопрстуфхцчшщъыбэюя")
    ar = []
    prar = []
    while True:
        if len(alf) == 0:
            ar.append(prar)
        
        if len(prar) == n:
            ar.append(prar)
            prar = []
            