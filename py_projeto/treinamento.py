import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Carregar os dados dos arquivos CSV
diretorio = 'C:/Users/joaov/Documents/Programação/Desenvolvimento web/piec2/py_projeto'
arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

dados_combinados = pd.DataFrame()

for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(diretorio, arquivo)
    dados = pd.read_csv(caminho_arquivo)
    
    # Adicionar rótulo baseado no nome do arquivo
    if 'repouso' in arquivo:
        dados['Condicao'] = 'repouso'
    elif 'velocidade 1' in arquivo:
        dados['Condicao'] = 'velocidade 1'
    elif 'velocidade 2' in arquivo:
        dados['Condicao'] = 'velocidade 2'
    elif 'velocidade 3' in arquivo:
        dados['Condicao'] = 'velocidade 3'
    
    dados_combinados = pd.concat([dados_combinados, dados], ignore_index=True)

# Verificar o total de amostras
print(f"Total de amostras carregadas: {len(dados_combinados)}")

# 2. Codificar rótulos
label_encoder = LabelEncoder()
dados_combinados['Condicao_encoded'] = label_encoder.fit_transform(dados_combinados['Condicao'])

# 3. Engenharia de Features
def extrair_features(dados):
    return np.array([
        dados.mean(),  # Média
        dados.std(),   # Desvio padrão
        dados.max(),   # Valor máximo
        dados.min(),   # Valor mínimo
        np.percentile(dados, 25),  # Primeiro quartil
        np.percentile(dados, 75),  # Terceiro quartil
    ])

# Aplicar a função de extração de features em janelas de 100 amostras
X = np.array([extrair_features(dados_combinados['Magnitude'].iloc[i:i+100]) for i in range(0, len(dados_combinados), 100)])
y = dados_combinados['Condicao_encoded'].values[::100]  # Rótulos codificados (uma amostra a cada 100)

# Verificar o tamanho dos dados após a extração de features
print(f"Total de janelas de 100 amostras: {len(X)}")

# 4. Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Verificar o tamanho dos conjuntos de treino e teste
print(f"Tamanho do conjunto de treino: {len(X_train)}")
print(f"Tamanho do conjunto de teste: {len(X_test)}")

# 5. Treinar o modelo com GridSearchCV
param_grid = {
    'n_estimators': [200, 300, 400],  # Mais árvores
    'max_depth': [10, 20, 30],        # Profundidades maiores
    'min_samples_split': [2, 5, 10]   # Valores padrão
}

rf_model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Melhores hiperparâmetros
print("Melhores hiperparâmetros:", grid_search.best_params_)

# 6. Avaliar o modelo
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))
print("Matriz de Confusão:\n", confusion_matrix(y_test, y_pred))

# 7. Salvar o modelo e o label_encoder
joblib.dump(best_model, 'random_forest_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
print("Modelo e label_encoder salvos.")