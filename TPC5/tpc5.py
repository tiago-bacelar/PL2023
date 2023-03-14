import re
import sys
from enum import Enum

coins = [ 1, 2, 5, 10, 20, 50, 100, 200 ]

money = r'\s*(?:([1-9]\d*)e)?(?:([1-9]\d?)c)?\s*'
levantar = re.compile(r'levantar', re.I)
moeda = re.compile(r'moeda\s+(.+)', re.I)
pousar = re.compile(r'(?:pousar)', re.I)
dial = re.compile(r'T=(?:(6[04]1\d{6})|(00\d{9})|(2\d{8})|(800\d{6})|(808\d{6}))', re.I)

def moneyToStr(money):
    euros = money // 100
    cents = money % 100
    
    if euros == 0:
        return f"{cents}c"
    elif cents == 0:
        return f"{euros}e"
    else:
        return f"{euros}e{cents}c"
    
def parseMoney(str):
    if m := re.fullmatch(money, str):
        euros = int(m.group(1)) if m.group(1) else 0
        cents = int(m.group(2)) if m.group(2) else 0    
        return euros * 100 + cents
    else:
        return None

def coinChange(money):
    aux = len(coins) - 1
    ans = {}
    
    while money > 0:
        if coins[aux] > money:
            aux -= 1
        else:
            money -= coins[aux]
            if coins[aux] in ans:
                ans[coins[aux]] += 1
            else:
                ans[coins[aux]] = 1
    
    return ans

class Fase(Enum):
    STAND_BY = 0
    ACTIVE = 1
    CALL = 2

class State:
    def __init__(self):
        self.saldo = 0
        self.fase = Fase.STAND_BY
    
    def levantar(self):
        print('maq: "Introduza moedas."')
        self.fase = Fase.ACTIVE
        
    def moedas(self, txt):
        print('maq: "', end='')
        
        for a in txt.split(','):
            aux = parseMoney(a)
            if aux and aux in coins:
                self.saldo = round(self.saldo + aux, 2)
            else:
                print(f'{a} - moeda inválida; ', end='')
        
        print(f'saldo = {moneyToStr(self.saldo)}"')
        
    def dial(self, groups):
        if groups[0]:
            print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
            return
        
        mins = {1: 150, 2: 25, 3: 0, 4: 10}
        
        for i in range(0, 5):
            if groups[i]:
                if self.saldo < mins[i]:
                    print('maq: "Não tens saldo suficiente para esse telefonema. Insira mais moedas ou disque novo número!"')
                else:
                    self.saldo = round(self.saldo - mins[i], 2)
                    self.fase = Fase.CALL
                    print(f'maq: "saldo = {moneyToStr(self.saldo)}"')
                return
               
    def pousar(self):
        if self.saldo != 0:
            troco = map(lambda mf: f"{mf[1]}x{moneyToStr(mf[0])}", coinChange(self.saldo).items())
            print(f'maq: "troco= {", ".join(troco)}; ', end='')
        
        print('Volte sempre!')
        self.saldo = 0
        self.fase = Fase.STAND_BY
        
    def process(self, input):
        if self.fase == Fase.STAND_BY:
            if re.fullmatch(levantar, input):
                self.levantar()
                return
        elif self.fase == Fase.ACTIVE:
            if m := re.fullmatch(moeda, input):
                self.moedas(m.group(1))
                return
            if m := re.fullmatch(dial, input):
                self.dial(m.groups())
                return
            if re.fullmatch(pousar, input):
                self.pousar()
                return
        elif self.fase == Fase.CALL:
            if re.fullmatch(pousar, input):
                self.pousar()
                return
            
        print('maq: "Comando inválido. Por favor tente novamente."')
        
    def end(self):
        if self.fase == Fase.ACTIVE or self.fase == Fase.CALL:
            self.pousar()

maquina = State()

for line in sys.stdin:
    maquina.process(line.strip(' \n'))

maquina.end()