import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelEncoder

# Passo 1 – Base original
training_data = [
    {"accuracy": 80, "game_time": 150, "average_time_per_attempt": 30, "attempts": 5, "performance": "Bom"},
    {"accuracy": 60, "game_time": 240, "average_time_per_attempt": 40, "attempts": 6, "performance": "Regular"},
    {"accuracy": 40, "game_time": 180, "average_time_per_attempt": 36, "attempts": 5, "performance": "Ruim"},
    {"accuracy": 100, "game_time": 120, "average_time_per_attempt": 20, "attempts": 6, "performance": "Excelente"},
    {"accuracy": 70, "game_time": 210, "average_time_per_attempt": 30, "attempts": 7, "performance": "Bom"},
]

df_original = pd.DataFrame(training_data)

# Passo 2 – Codifica o rótulo
le = LabelEncoder()
df_original["performance_code"] = le.fit_transform(df_original["performance"])

# Passo 3 – Gera dados sintéticos
X, y = make_classification(
    n_samples=100,
    n_features=4,
    n_informative=4,
    n_redundant=0,
    n_classes=4,
    n_clusters_per_class=1,
    random_state=42
)

# Passo 4 – Normaliza os dados com base nas médias reais
def rescale(column_name, values):
    mean = df_original[column_name].mean()
    std = df_original[column_name].std()
    return np.clip((values * std + mean), a_min=0, a_max=None)

df_synthetic = pd.DataFrame()
df_synthetic["accuracy"] = rescale("accuracy", X[:, 0]).round().astype(int)
df_synthetic["game_time"] = rescale("game_time", X[:, 1]).round().astype(int)
df_synthetic["average_time_per_attempt"] = rescale("average_time_per_attempt", X[:, 2]).round(1)
df_synthetic["attempts"] = np.clip(rescale("attempts", X[:, 3]).round().astype(int), 1, 20)

# Passo 5 – Adiciona a variável alvo (performance)
df_synthetic["performance"] = le.inverse_transform(y)

# Exibe amostra
print(df_synthetic.head())
df_synthetic.to_json("dados_sinteticos.json", orient="records", indent=4, force_ascii=False)
print(f"Total de registros sintéticos: {len(df_synthetic)}")
# Salvar como JSON
