##### FONT-FUNCTIES #####
def h1(tekst):
    return '# ' + tekst.strip()

def h2(tekst):
    return '## ' + tekst.strip()

def h3(tekst):
    return '### ' + tekst.strip()

def hLevel(tekst, level):
    if tekst is None or tekst == '':
        val = ''
    elif level == 1:
        val = h1(tekst)
    elif level == 2:
        val = h2(tekst)
    elif level == 3:
        val = h3(tekst)
    elif level is None:
        val = B(tekst)
    else:
        val = B(f"{level - 3}. {tekst}")
    return val

def B(tekst):
    return '**' + tekst.strip() + '**'