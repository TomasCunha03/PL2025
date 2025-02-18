import sys
acc = 0
sum = True
for (linha) in sys.stdin:
    i = 0
    n = len(linha)
    while (i < n):
        if (linha[i].isdigit()):
            start = i
            while (i < len(linha) and linha[i].isdigit()):
                i = i + 1
            valor = int(linha[start:i])
            if (sum):
                acc = acc + valor
        elif (linha[i:i+2].lower() == "on"):
            sum = True
            i = i + 2
        elif (linha[i:i+3].lower() == "off"):
            sum = False
            i = i + 3
        elif (linha[i] == '='):
            print(acc)
            i = i + 1
        else:
            i = i + 1
