import kagglehub
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Pobranie najnowszej wersji datasetu
path = kagglehub.dataset_download("catherinerasgaitis/mxmh-survey-results")

# Ścieżka do pliku CSV w pobranym folderze
data_file = f"{path}/mxmh_survey_results.csv"

# Wczytanie danych do DataFrame Pandas
data = pd.read_csv(data_file)

# Ustawienie szerokości wyświetlania Pandas
pd.set_option('display.max_columns', None)

# Usunięcie kolumn Timestamp, Primary streaming service i Permissions, jeśli istnieją
data = data.drop(columns=['Timestamp', 'Primary streaming service', 'Permissions'], errors='ignore')

# Usunięcie duplikatów
data = data.drop_duplicates()

# Zliczanie wierszy z brakującymi danymi przed uzupełnianiem missing values
missing_rows_count = data.isnull().any(axis=1).sum()
print(f"Liczba wierszy z brakującymi danymi przed uzupełnieniem: {missing_rows_count}")

# Identyfikacja kolumn numerycznych i tekstowych
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
text_columns = data.select_dtypes(include=['object']).columns

# Uzupełnianie brakujących wartości
# Liczbowe kolumny: uzupełnianie medianą
for col in numeric_columns:
    data[col] = data[col].fillna(data[col].median())

# Tekstowe kolumny: uzupełnianie wartością najczęściej występującą (mode)
for col in text_columns:
    data[col] = data[col].fillna(data[col].mode()[0])

# Identyfikacja i zastępowanie wartości odstających medianą dla kolumn numerycznych
for col in numeric_columns:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Zastąp wartości odstające medianą
    median_value = data[col].median()
    data[col] = np.where((data[col] < lower_bound) | (data[col] > upper_bound), median_value, data[col])

# Usunięcie kolumn zawierających wyłącznie brakujące wartości
data = data.dropna(axis=1, how='all')

#Zapisanie wyczyszczonych i przekształconych danych do pliku CSV
data.to_csv("processed_data_before_normalization.csv", index=False)
print("Wyczyszczone i przekształcone dane zapisano do pliku 'processed_data_before_normalization.csv'.")

# Obliczanie podstawowych statystyk opisowych przed konwersją danych
print("\nPodstawowe statystyki opisowe przed konwersją danych:")
descriptive_stats = data.describe(include='all')
print(descriptive_stats)

def visualize_detailed_stats(df):
    print("Wizualizacja szczegółowych statystyk opisowych:")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    stats_data = {
        'Średnia': df[numeric_columns].mean(),
        'Mediana': df[numeric_columns].median(),
        'Odchylenie standardowe': df[numeric_columns].std(),
        'Zakres': df[numeric_columns].max() - df[numeric_columns].min()
    }

    stats_df = pd.DataFrame(stats_data)

    for stat in stats_df.columns:
        plt.figure(figsize=(12, 6))
        sns.barplot(x=stats_df.index, y=stats_df[stat], palette="coolwarm")
        plt.xticks(rotation=45, ha="right")
        plt.title(f"{stat} dla kolumn numerycznych")
        plt.ylabel(stat)
        plt.xlabel("Kolumny")
        plt.tight_layout()
        plt.show()

# Wywołanie wizualizacji szczegółowych statystyk
visualize_detailed_stats(data)

#Wykonywanie wizualizacji przed normalizacją danych
print("\nWykonywanie wizualizacji przed normalizacją...")
for col in numeric_columns:
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.hist(data[col], bins=20, edgecolor='k')
    plt.title(f"Histogram: {col}")
    plt.xlabel(col)
    plt.ylabel("Liczność")

    plt.subplot(1, 2, 2)
    plt.boxplot(data[col], vert=False)
    plt.title(f"Boxplot: {col}")
    plt.xlabel(col)

    plt.tight_layout()
    plt.show()

# Zapis statystyk do pliku CSV
descriptive_stats.to_csv("descriptive_stats.csv", index=True)

# Konwersja danych tekstowych na numeryczne
# Label Encoding dla prostych kolumn z niewielką liczbą unikalnych wartości
label_encoder = LabelEncoder()
simple_text_columns = ['While working', 'Music effects', 'Instrumentalist', 'Composer', 'Exploratory', 'Foreign languages']
for col in simple_text_columns:
    if col in data.columns:
        data[col] = label_encoder.fit_transform(data[col])

# Label Encoding dla kolumn z kategoriami częstotliwości
frequency_columns = [col for col in data.columns if col.startswith('Frequency')]
frequency_mapping = {
    'Never': 0,
    'Rarely': 1,
    'Sometimes': 2,
    'Very frequently': 3
}
for col in frequency_columns:
    if col in data.columns:
        data[col] = data[col].map(frequency_mapping)

# Label Encoding dla kolumny 'Fav genre'
if 'Fav genre' in data.columns:
    data['Fav genre'] = label_encoder.fit_transform(data['Fav genre'])

# Aktualizacja listy kolumn numerycznych po konwersji danych
numeric_columns = data.select_dtypes(include=['float64', 'int64', 'uint8']).columns

# Normalizacja wszystkich kolumn numerycznych do zakresu [0, 1]
# Komentarz: Decyzja o normalizacji całego zestawu numerycznego w zakresie [0, 1] wynika z potrzeby jednolitego zakresu dla modeli ML
min_max_scaler = MinMaxScaler()
data[numeric_columns] = min_max_scaler.fit_transform(data[numeric_columns])
print("\nDane po normalizacji (zakres [0, 1]) dla wszystkich kolumn numerycznych:")
print(data[numeric_columns].head())

# Wizualizacje po normalizacji
print("\nWykonywanie wizualizacji po normalizacji...")
for col in numeric_columns:
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.hist(data[col], bins=20, edgecolor='k')
    plt.title(f"Histogram: {col}")
    plt.xlabel(col)
    plt.ylabel("Liczność")

    plt.subplot(1, 2, 2)
    plt.boxplot(data[col], vert=False)
    plt.title(f"Boxplot: {col}")
    plt.xlabel(col)

    plt.tight_layout()
    plt.show()

# Korelacje między zmiennymi
print("\nKorelacje między zmiennymi:")
correlation_matrix = data.corr()
filtered_corr = correlation_matrix[(correlation_matrix > 0.10) | (correlation_matrix < -0.10)]
plt.figure(figsize=(15, 12))  # Zwiększenie rozmiaru wykresu
sns.heatmap(filtered_corr, annot=True, fmt=".1f", cmap="coolwarm", cbar=True, annot_kws={"size": 8}, mask=filtered_corr.isnull())
plt.xticks(rotation=45, ha="right", fontsize=8)  # Rotacja i zmniejszenie czcionki osi x
plt.yticks(fontsize=8)  # Zmniejszenie czcionki osi y
plt.title("Macierz korelacji (tylko istotne korelacje)", fontsize=16)
plt.tight_layout()
plt.show()

# Wyświetlenie podstawowych informacji o danych
print("Podstawowe informacje o danych:")
print(data.info())

# Wyświetlenie kilku pierwszych wierszy danych
print("\nPrzykładowe wiersze danych ze wszystkimi kolumnami:")
print(data.head().to_string())

#Zapisanie wyczyszczonych i przekształconych danych do pliku CSV
data.to_csv("processed_data_after_normalization.csv", index=False)
print("Wyczyszczone i przekształcone dane zapisano do pliku 'processed_data_after_normalization.csv'.")