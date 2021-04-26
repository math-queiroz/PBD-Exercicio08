import random
import math
from collections import Counter

class Pessoa:
    def __init__ (self, idade, sexo, salario, intencao_de_voto):
        self.idade = idade
        self.sexo = sexo
        self.salario = salario
        self.intencao_de_voto = intencao_de_voto

    def __str__ (self):
        return f'Idade: {self.idade}, Sexo: {self.sexo}, Salario: R$ {self.salario:.2f}, Intencao_de_voto: {self.intencao_de_voto}'

    def __eq__ (self, other):
        return self.intencao_de_voto == other.intencao_de_voto

    def __hash__ (self):
        return 0 if self.intencao_de_voto == 'Haddad' else 1

def gerar_base (n):
    lista = []
    for _ in range(n):
        idade = random.randint(18,35)
        sexo = random.choice(['M', 'F'])
        salario = 1200 + random.random() * 1300
        intencao_de_voto = random.choice(['Haddad', 'Bolsonaro'])
        p = Pessoa(idade, sexo, salario, intencao_de_voto)
        lista.append(p)
    return lista

def rotulo_de_maior_frequencia (pessoas):
    frequencias = Counter(pessoas)
    mais_frequentes = frequencias.most_common(1)
    return mais_frequentes[0][0]

def rotulo_de_maior_frequencia_sem_empate (pessoas):
    frequencias = Counter(pessoas) # Returns: i.e. {('Bolsonaro', 5), ('Haddad', 5)}
    rotulo, frequencia = frequencias.most_common(1)[0] # Returns: i.e. {('Bolsonaro', 5)}
    qtd_mais_frequentes = len([count for count in frequencias.values() if count == frequencia]) # Returns: i.e. 2
    return rotulo if (qtd_mais_frequentes == 1) else rotulo_de_maior_frequencia_sem_empate(pessoas[:-1])

def distancia(p1, p2):
    i = math.pow(p1.idade - p2.idade, 2)
    s = math.pow((1 if p1.sexo == 'M' else 0) - (1 if p2.sexo == 'M' else 0), 2)
    sal = math.pow(p1.salario - p2.salario, 2)
    return math.sqrt(i + s + sal)

def knn(k, observacoes_rotuladas, nova_observacao):
    ordenados_por_distancia = sorted(observacoes_rotuladas, key=lambda obs: distancia(obs, nova_observacao))
    k_mais_proximos = ordenados_por_distancia[:k]
    resultado = rotulo_de_maior_frequencia_sem_empate(k_mais_proximos)
    return resultado.intencao_de_voto

def main():
    # Criação e exibição da base de Pessoas
    base = gerar_base(100)

    # Leave-One-Out Cross-Validation
    acertos, total = (0, len(base))
    for pessoa_out in base:
        pessoas_in = [pessoa for pessoa in base if distancia(pessoa, pessoa_out) > 0]
        previsao = knn(5, pessoas_in, pessoa_out)
        if (previsao == pessoa_out.intencao_de_voto):
            acertos = acertos + 1
    
    # Exibição dos resultados
    print(f'\nTaxa de acerto calculado por Leave-One-Out Cross-Validation: {acertos/total*100:.2f}% (Acertos: {acertos}, Erros: {total-acertos})')
    
main()