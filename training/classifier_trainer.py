import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelTrainer:
    def __init__(self, data_csv_path, embeddings_npy_path, models_dir="models"):
        self.data_csv_path = data_csv_path
        self.embeddings_npy_path = embeddings_npy_path
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
    def load_and_prepare_features(self):
        """Loads dataset and embeddings, encodes categorical variables, and builds the feature matrix X."""
        logging.info("Carregando datasets para treino...")
        df = pd.read_csv(self.data_csv_path)
        embeddings = np.load(self.embeddings_npy_path)
        
        logging.info(f"Dados carregados: {len(df)} registros. Embeddings shape: {embeddings.shape}")
        
        # Preencher NaNs em metadados para evitar erros
        df['estado'] = df['estado'].fillna('N.I').astype(str)
        df['pauta_acao'] = df['pauta_acao'].fillna('N.I').astype(str)
        df['nome_movimento'] = df['nome_movimento'].fillna('N.I').astype(str)
        df['acao_derivada'] = df['acao_derivada'].fillna('').astype(str)
        df['acao_matriz_derivada'] = df['acao_matriz_derivada'].fillna('OUTROS').astype(str)
        
        # Encoders categóricos
        encoders = {}
        categorical_cols = ['estado', 'pauta_acao', 'nome_movimento']
        encoded_feats = []
        
        for col in categorical_cols:
            le = LabelEncoder()
            # Adicionar classe para novos valores não vistos no inference
            classes = list(df[col].unique())
            if 'OUTROS' not in classes:
                classes.append('OUTROS')
            le.fit(classes)
            df[col + '_encoded'] = le.transform(df[col])
            encoders[col] = le
            encoded_feats.append(df[col + '_encoded'].values.reshape(-1, 1))
            
        # Extrair scores de similaridade cosseno (colunas sim_score_*)
        sim_cols = [col for col in df.columns if col.startswith('sim_score_')]
        sim_features = df[sim_cols].values
        
        logging.info(f"Extraídas {len(sim_cols)} colunas de similaridade.")
        
        # Concatenar: Embeddings (384d) + Scores de Similaridade (47d) + Metadados Encodados (3d)
        X = np.hstack([embeddings, sim_features] + encoded_feats)
        logging.info(f"Feature matrix X construída com shape: {X.shape}")
        
        # Salvar encoders
        encoders_path = os.path.join(self.models_dir, "encoders.pkl")
        with open(encoders_path, 'wb') as f:
            pickle.dump(encoders, f)
        logging.info(f"Encoders salvos em: {encoders_path}")
        
        return X, df, encoders

    def train_and_evaluate(self):
        """Trains RandomForestClassifiers for both Ação Derivada and Ação Matriz and saves them."""
        X, df, encoders = self.load_and_prepare_features()
        
        # 1. Treino para Ação Derivada
        y_derivada = df['acao_derivada'].values
        
        logging.info("Dividindo dataset em Treino e Teste (80% treino, 20% teste) para Ação Derivada...")
        # Determine if stratification is safe (each class must have at least 2 samples)
        from collections import Counter
        class_counts = Counter(y_derivada)
        stratify_safe = None if min(class_counts.values()) < 2 else y_derivada
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_derivada, test_size=0.2, random_state=42, stratify=stratify_safe
        )
        
        logging.info("Treinando HistGradientBoostingClassifier para Ação Derivada...")
        sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)
        clf_derivada = HistGradientBoostingClassifier(max_iter=150, max_depth=10, random_state=42)
        clf_derivada.fit(X_train, y_train, sample_weight=sample_weights)
        
        # Avaliar
        y_pred = clf_derivada.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        logging.info(f"Acurácia Ação Derivada: {acc * 100:.2f}%")
        
        report = classification_report(y_test, y_pred, zero_division=0)
        logging.info("Relatório de Classificação — Ação Derivada:\n" + report)
        
        # Salvar relatório textual
        with open(os.path.join(self.models_dir, "classification_report_derivada.txt"), "w", encoding="utf-8") as f:
            f.write(f"Acurácia: {acc * 100:.2f}%\n\n")
            f.write(report)
            
        # 2. Treino para Ação Matriz
        y_matriz = df['acao_matriz_derivada'].values
        
        logging.info("Dividindo dataset em Treino e Teste para Ação Matriz...")
        # Safe stratify check for matriz classes
        from collections import Counter
        class_counts_m = Counter(y_matriz)
        stratify_safe_m = None if min(class_counts_m.values()) < 2 else y_matriz
        X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(
            X, y_matriz, test_size=0.2, random_state=42, stratify=stratify_safe_m
        )
        
        logging.info("Treinando HistGradientBoostingClassifier para Ação Matriz...")
        sample_weights_m = compute_sample_weight(class_weight='balanced', y=y_train_m)
        clf_matriz = HistGradientBoostingClassifier(max_iter=150, max_depth=10, random_state=42)
        clf_matriz.fit(X_train_m, y_train_m, sample_weight=sample_weights_m)
        
        # Avaliar
        y_pred_m = clf_matriz.predict(X_test_m)
        acc_m = accuracy_score(y_test_m, y_pred_m)
        logging.info(f"Acurácia Ação Matriz: {acc_m * 100:.2f}%")
        
        report_m = classification_report(y_test_m, y_pred_m, zero_division=0)
        logging.info("Relatório de Classificação — Ação Matriz:\n" + report_m)
        
        # Salvar relatório textual
        with open(os.path.join(self.models_dir, "classification_report_matriz.txt"), "w", encoding="utf-8") as f:
            f.write(f"Acurácia: {acc_m * 100:.2f}%\n\n")
            f.write(report_m)
            
        # Salvar os modelos treinados
        model_derivada_path = os.path.join(self.models_dir, "classifier_derivada.pkl")
        with open(model_derivada_path, 'wb') as f:
            pickle.dump(clf_derivada, f)
            
        model_matriz_path = os.path.join(self.models_dir, "classifier_matriz.pkl")
        with open(model_matriz_path, 'wb') as f:
            pickle.dump(clf_matriz, f)
            
        logging.info(f"Modelos salvos com sucesso na pasta '{self.models_dir}'.")
        
        return {
            'accuracy_derivada': acc,
            'accuracy_matriz': acc_m,
            'features_dim': X.shape[1]
        }

if __name__ == "__main__":
    trainer = ModelTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
    trainer.train_and_evaluate()
