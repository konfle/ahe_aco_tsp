# Opis Struktury Danych

Ten projekt zawiera struktury danych przechowujące informacje o miastach wraz z ich współrzędnymi geograficznymi.

## Struktura Danych

Struktura danych jest reprezentowana jako słownik (format pliku JSON), gdzie kluczem jest nazwa miasta, 
a wartością jest słownik zawierający jego współrzędne geograficzne oraz odległości do innych miast w strukturze danych.

Przykładowy fragment struktury danych:

```json
{
    "Badenia-Wirtembergia": {"lat": 48.7758, "lng": 9.1829, "distances": {}},
    "Bawaria": {"lat": 48.1351, "lng": 11.5820, "distances": {}},
    "Berlin": {"lat": 52.5200, "lng": 13.4050, "distances": {}},
    ...
}
```

## Dodawanie Nowych Danych

Aby dodać nowe dane do istniejącej struktury, należy utworzyć nowy klucz z nazwą nowego regionu i wypełnić go 
odpowiednimi danymi. Następnie, jeśli to konieczne, odległości do innych miast należy uzupełnić ręcznie lub
użyć odpowiedniej funkcji obliczającej odległości.

## Uwagi
W przypadku modyfikacji lub rozszerzenia struktury danych, należy zadbać o zachowanie spójności danych oraz dostarczyć 
odpowiednią dokumentację w pliku źródłowym.