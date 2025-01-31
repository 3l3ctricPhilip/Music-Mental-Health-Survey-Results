# Music & Mental Health (MxMH) Survey Results 

## Na tapet wziąłem dataset "Music & Mental Health" ze strony kaggle.com. Badanie było przeprowadzone na grupie badawczej liczącej 336 osób. Moim głównym obiektem zainteresowania jest wpływ muzyki, a dokładniej jej poszczególnych gatunków na zdrowie psychiczne odbiorców.

## Poniżej tłumaczenie krótkiej notatki ze strony kaggle.com

Muzykoterapia (MT) to wykorzystanie muzyki w celu poprawy stresu, nastroju i ogólnego stanu zdrowia psychicznego danej osoby. MT jest również uznawana za praktykę opartą na dowodach, wykorzystującą muzykę jako katalizator „szczęśliwych” hormonów, takich jak oksytocyna.

MT wykorzystuje jednak szeroką gamę różnych gatunków muzycznych, różniących się w zależności od organizacji.

Zbiór danych MxMH ma na celu określenie, jakie, jeśli w ogóle, istnieją korelacje między gustem muzycznym danej osoby a jej samooceną zdrowia psychicznego. W idealnym przypadku wyniki te mogłyby przyczynić się do bardziej świadomego stosowania MT lub po prostu dostarczyć interesujących informacji na temat umysłu.

Interpretacja danych

Blok 0: Informacje ogólne
Respondenci odpowiadają na ogólne pytania dotyczące tła muzycznego i nawyków słuchania.

Blok 1: Gatunki muzyczne
Respondenci oceniają, jak często słuchają 16 gatunków muzycznych:

Nigdy
Rzadko
Czasami
Bardzo często

Blok 2: Zdrowie psychiczne
Respondenci oceniają lęk, depresję, bezsenność i OCD w skali od 0 do 10, gdzie:

0 - nie doświadczam tego.
10 - doświadczam tego regularnie, stale / lub w skrajnych przypadkach.


# Eksploracja danych
## Podstawowe statystyki opisowe

Liczba wierszy z brakującymi danymi przed uzupełnieniem: 119.
Wiersze uzupełniłem medianą w przypadku kolumn liczbowych, tekstowe kolumny zaś wartością najczęściej występującą (moda). 
Ponadto odnośnie kolumn numerycznych zidentyfikowałem wartości odstające i zastąpiłem medianą.

### Wizualizacje dla podstawowych statystyk opisowych:

![image](https://github.com/user-attachments/assets/bc715ddd-6761-41b3-9009-1cea42dc1e6d)

![image](https://github.com/user-attachments/assets/48e9856b-67dd-477e-ad1c-07f344889847)

![image](https://github.com/user-attachments/assets/e35dc341-f2a9-456d-8700-291eeda972f7)

![image](https://github.com/user-attachments/assets/9017eea9-9693-41fe-8471-61e1327ee3ce)


## Wizualizacje (histogramy, wykresy pudełkowe, wykresy rozrzutu) przed normalizacją danych

![image](https://github.com/user-attachments/assets/bdbe4b03-24ab-4fbe-8808-1a0fecd252a2)

![image](https://github.com/user-attachments/assets/cb5cfa06-a52f-47a6-900d-b8b3b7d3c934)

![image](https://github.com/user-attachments/assets/f5dda9af-d4be-4967-bb3a-14cf2f957730)

![image](https://github.com/user-attachments/assets/46a36a74-429a-4622-86a2-49ad0d1b7713)

![image](https://github.com/user-attachments/assets/a6a0a3d4-4dd1-45c7-9318-a3a257e3628b)

![image](https://github.com/user-attachments/assets/4e460a6a-d134-4f38-ad4a-08ae46fa5eef)

![image](https://github.com/user-attachments/assets/7495fadf-835e-41dd-8a0f-3776e1f975aa)

Następnie dokonałem konwersji danych tekstowych na numeryczne. Wykorzystałem Label Encoder dla prostych kolumn z niewielką liczbą unikalnych wartości: Fav genre (ulubiony gatunek), częstotliwość słuchania danego gatunku wg respondentów - Never: 0 , Rarelty: 1, Sometimes: 2, Very frequently: 3.

Kolejnym krokiem była normalizacja wszystkich kolumn numerycznych do zakresu [0, 1]

## Wizualizacje (histogramy, wykresy pudełkowe, wykresy rozrzutu) po normalizacji danych

Wybrałem najciekawsze z mojego punktu widzenia.

![image](https://github.com/user-attachments/assets/2ab544f1-47b9-412b-b803-fc95bdbd3cb3)

![image](https://github.com/user-attachments/assets/0c2eb965-629f-4e46-8045-4111b09674d7)

![image](https://github.com/user-attachments/assets/b81efa6a-6f52-42f3-b264-35e278016bd9)

![image](https://github.com/user-attachments/assets/291fa906-1cd9-4902-9f8f-bcfda0918f63)

![image](https://github.com/user-attachments/assets/1b7d589f-ab11-4173-9823-8b720b6dc97c)

![image](https://github.com/user-attachments/assets/b97c7925-3c6e-418a-964c-b93870ff0bd4)

Choroby, dolegliwości:

![image](https://github.com/user-attachments/assets/77d95a77-dbe3-4bf0-a715-742ec6bc344f)

![image](https://github.com/user-attachments/assets/35895721-3302-4594-b708-b1b8f99cc506)

![image](https://github.com/user-attachments/assets/3e8838e5-3e41-4b05-8a31-bcf51974f673)

![image](https://github.com/user-attachments/assets/e14df009-f2e1-4ee4-8dcd-d7e7d4d3b126)

## Według mnie najciekawszym aspektem jest macierz korelacji. Wybrałem te komórki, gdzie współczynnik jest większy, niż 0,1 i mniejszy, niż -0,1. Wartości spoza tego przedziału zostały pominięte. Filtracja eliminuje mało istotne korelacje (bliskie 0).

![image](https://github.com/user-attachments/assets/42be7b60-233e-4569-9296-4acd0bc0a1e1)

Słownik:
Anxiety - Niepokój/Lęk,
Depression - Depresja,
Insomnia - Bezsenność,
OCD - Zaburzenia obsesyjno-kompulsyjne (dawniej nerwica natręctw)

# Moje obserwacje:

## Osoby słuchające Rocka i Metalu są w większym stopniu narażone na depresję (współczynnik korelacji: 0,2). Ponadto osoby słuchające Metalu mogą cierpieć na bezsenność częściej, niż słuchacze innych gatunków muzycznych (współczynnik korelacji: 0,2).

### W mniejszym stopniu muzyka Pop oraz Video Game Music (Ścieżki dźwiękowe z gier) mogą wpływać na poziom niepokoju i stany lękowe (współczynnik korelacji: 0,1). Na depresję może mieć wpływ również Rap (pewnie chodzi o polskie produkcje), oraz Folk (w sumie się nie dziwię, artyści pokroju Elliotta Smitha potrafią dobić leżącego). Tutaj współczynnik korelacji również wyniósł 0,1. 

PS Zastanawiam się, kto tworząc ankietę wyodrębnił dwa gatunki jak Rap i Hip hop.













