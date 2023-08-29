class Fracção:
    def __init__(self, numerador, denominador) -> None:
        self.numerador = numerador
        self.denominador = denominador
    
    def __str__(self) -> str:
        return f'{self.numerador}/{self.denominador}'
    
    def resultado(self, divisao_inteira: bool=False):
        if not divisao_inteira:
            return self.numerador/self.denominador
        else:
            return self.numerador//self.denominador
    
    def percentagem(self):
        return self.numerador/self.denominador * 100
    
