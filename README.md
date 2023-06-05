# Projekt z przedmiotu: Przeszukiwanie i Optumalizacja

Realizowany w zespole: Jan Jędrzejewski, Dominik Łopatecki

## Temat projektu

Rozwiazać problem plecakowy dla danych skorelowanych i nieskorelowanych
używając algorytmu PBIL (Population-Based Incremental Learning), porównując
z inna metodą (algorytmem). Wymagana dokładna analiza statystyczna
przedstawionych wyników. Literatura dostepna u prowadzacego.
Literatura: DOI:10.3390/app11199136.

# Interpretacja problemu plecakowego
Pochodzi od maksymalizacyjnego problemu wyboru przedmiotów, tak by ich wartość sumaryczna była jak największa i jednocześnie mieściły się w plecaku. Przy podanym zbiorze elementów o podanej wadze i wartości należy wybrać taki podzbiór, by suma wartości była możliwie jak największa, a suma wag była nie większa od danej pojemności plecaka.

# Zaimplementowane algorytmy

## PBIL (Population-Based Incremental Learning)
Algorytm ewolucyjny realizowany przy pomocy modelu probabilistycznego. Rozkład prawdopodobieństwa w PBIL reprezentowany jest jako wektor zawierający prawdopodobieństwo wystąpienia przedmiotu w danym bicie.

## Programowanie dynamiczne
Metoda typu Integer Programing, deterministycznie wyznacza optimum globalne. Wadą jest  szybkość wyznaczenia rozwiązania i działąnie tylko dla liczb całkowitoliczbowych.

## Algorytm przeszukiwania drzewa A*
Zestaw przedmotów reprezentujemy jako ciąg bitowy. Problem plecakowy można przedstawić w postaci drzewa binarnego, gdzie liście są mozłiwymi rozwiązaniami.

## Metoda heurystyczna
Do plecaka wybierane są przedmioty o największym współczynniku wartości do wagi.

# Porównanie metod
W notatniku `experiments.ipynb` zamieszczono porównanie metod dla danych wygenerowanych z różnym poziomem korelacji.