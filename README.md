# VoronoiDiagram

Projekt napisany przez Jana Dąbrowskiego i Jakuba Karonia w ramach ćwiczeń z przedmiotu Algorytmy Geometryczne na kierunku informatyka na AGH (semestr zimowy 2023/2024). Celem projektu jest wyznaczanie diagramu Voronoi dwoma sposobami: metodą inkrementacyjną oraz algorytmem Fortune'a.

Instrukcje korzystania z poszczególnych plików:
- Main.ipynb: plik z wizualizacjami działania poszczególnych algorytmów. Komentarz #Editable oznacza, że w komórce znajduje się parametr, który może być zmieniony przez użytkownika (np. ilość punktów).

- visuals: plik, w którym wizualizowane są krok po kroku wszystkie algorymty zastosowane do znalezienia diagramu Voronoi. W pliku znajdują się komórki oznaczone komentarzem #Editable, co oznacza, że można w nich modyfikować niektóre parametry. 

- tests: plik, w którym znajduje się funkcja testująca algorytmy. Przyjmuje argumenty: num_of_points oraz iterations_num. Funkcja generuje num_of_points punktów na płaszczyźnie i wyznacza dla nich algorytm Voronoi. Powtarza to interations_num razy i wypisuje ile razy udało się znaleźć triangulację. 
