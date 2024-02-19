import numpy as np

def populasyon_tanimla(populasyon_boyutu, birey_uzunlugu):
    return np.random.randint(2, size=(populasyon_boyutu, birey_uzunlugu))

def amac_fonksiyonu(x):
    return np.sum(x**2)

def caprazlama(parent1, parent2, caprazlama_olasiligi):
    if np.random.rand() < caprazlama_olasiligi:
        nokta1 = np.random.randint(len(parent1))
        nokta2 = np.random.randint(nokta1 ,len(parent1))
        child1 = np.concatenate((parent1[:nokta1], parent2[nokta1:nokta2], parent1[nokta2:]))
        child2 = np.concatenate((parent2[:nokta1], parent1[nokta1:nokta2], parent2[nokta2:]))
        return child1, child2
    else:
        return parent1, parent2

def mutasyon(child, mutasyon_olasiligi):
    mutasyonlu_child = child.copy()
    for i in range(len(mutasyonlu_child)):
        if np.random.rand() < mutasyon_olasiligi:
            mutasyonlu_child[i] = 1 - child[i]
    return mutasyonlu_child

def binary_to_decimal(binary_sayi, alt_limit, ust_limit, problem_boyutu):
    decimal_deger = int(binary_sayi, 2)
    return alt_limit + decimal_deger / ((2 ** problem_boyutu) - 1) * (ust_limit - alt_limit)

def genetik_algoritma(populasyon_boyutu, birey_uzunlugu, problem_boyutu, alt_limit, ust_limit,
                      iterasyon_sayisi, caprazlama_olasiligi, mutasyon_olasiligi):
    populasyon = populasyon_tanimla(populasyon_boyutu, birey_uzunlugu)
    for generasyon in range(iterasyon_sayisi):
        decoded_populasyon = np.zeros((populasyon_boyutu, problem_boyutu))
        for i in range(populasyon_boyutu):
            for j in range(problem_boyutu):
                baslangic = j * 15 #karar değişkeni
                son = (j + 1) * 15
                decoded_populasyon[i, j] = binary_to_decimal(''.join(map(str, populasyon[i, baslangic:son])),
                                                             alt_limit, ust_limit, 15)

        fitness_degeri = np.apply_along_axis(amac_fonksiyonu, 1, decoded_populasyon)

        secim_olasiliklari = fitness_degeri / np.sum(fitness_degeri)
        secilen_indisler = np.random.choice(range(populasyon_boyutu), size=populasyon_boyutu, p=secim_olasiliklari)
        secilen_parentlar = populasyon[secilen_indisler]

        yeni_populasyon = np.zeros_like(populasyon)
        for i in range(0, populasyon_boyutu, 2):
            parent1 = secilen_parentlar[i]
            parent2 = secilen_parentlar[i + 1]

            child1, child2 = caprazlama(parent1, parent2, caprazlama_olasiligi)

            child1 = mutasyon(child1, mutasyon_olasiligi)
            child2 = mutasyon(child2, mutasyon_olasiligi)

            yeni_populasyon[i] = child1
            yeni_populasyon[i + 1] = child2

        populasyon = yeni_populasyon

        en_iyi_indeks =np.argmin(fitness_degeri)
        en_iyi_birey = decoded_populasyon[en_iyi_indeks]
        en_iyi_fitness = fitness_degeri[en_iyi_indeks]
        print(f"Generasyon {generasyon+1}: En iyi birey: {en_iyi_birey}, En iyi fitness degeri: {en_iyi_fitness}")

populasyon_boyutu = 20
birey_uzunlugu = 75
problem_boyutu = 5
alt_limit = -100
ust_limit = 100
iterasyon_sayisi = 10000
caprazlama_olasiligi = 0.7
mutasyon_olasiligi = 0.001

genetik_algoritma(populasyon_boyutu, birey_uzunlugu, problem_boyutu, alt_limit, ust_limit, iterasyon_sayisi, caprazlama_olasiligi, mutasyon_olasiligi)