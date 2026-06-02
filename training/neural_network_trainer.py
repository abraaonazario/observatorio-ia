import os
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurar semente aleatória para reprodutibilidade
torch.manual_seed(42)
np.random.seed(42)

# ==========================================
# 1. ESPECIFICAÇÃO DO DATASET PYTORCH
# ==========================================
class LandConflictDataset(Dataset):
    def __init__(self, X, y_derivada, y_matriz):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y_derivada = torch.tensor(y_derivada, dtype=torch.long)
        self.y_matriz = torch.tensor(y_matriz, dtype=torch.long)
        
    def __len__(self):
        return len(self.X)
        
    def __getitem__(self, idx):
        return self.X[idx], self.y_derivada[idx], self.y_matriz[idx]

# ==========================================
# 2. ARQUITETURA DE REDE NEURAL MULTI-TASK
# ==========================================
class MultiTaskDNN(nn.Module):
    def __init__(self, input_dim, num_classes_derivada, num_classes_matriz):
        super(MultiTaskDNN, self).__init__()
        
        # Backbone Compartilhado (Shared Representation Learning Layer)
        self.shared_backbone = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Cabeça de Classificação 1: Ação Derivada (Microclasse)
        self.head_derivada = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes_derivada)
        )
        
        # Cabeça de Classificação 2: Ação Matriz (Macroclasse)
        self.head_matriz = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes_matriz)
        )
        
    def forward(self, x):
        # Passagem pelo backbone compartilhado
        shared_features = self.shared_backbone(x)
        
        # Divisão em duas predições paralelas (multi-task learning)
        out_derivada = self.head_derivada(shared_features)
        out_matriz = self.head_matriz(shared_features)
        
        return out_derivada, out_matriz

# ==========================================
# 3. PIPELINE DE TREINAMENTO E VALIDAÇÃO
# ==========================================
class NeuralNetworkTrainer:
    def __init__(self, data_csv_path, embeddings_npy_path, models_dir="models"):
        self.data_csv_path = data_csv_path
        self.embeddings_npy_path = embeddings_npy_path
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
    def load_and_prepare_data(self):
        """Carrega e prepara a fusão de atributos (X) e encoda os targets categóricos (Y)."""
        logging.info("Carregando datasets para treino da Rede Neural...")
        df = pd.read_csv(self.data_csv_path)
        embeddings = np.load(self.embeddings_npy_path)
        
        # Preencher NaNs em metadados
        df['estado'] = df['estado'].fillna('N.I').astype(str)
        df['pauta_acao'] = df['pauta_acao'].fillna('N.I').astype(str)
        df['nome_movimento'] = df['nome_movimento'].fillna('N.I').astype(str)
        df['acao_derivada'] = df['acao_derivada'].fillna('').astype(str)
        df['acao_matriz_derivada'] = df['acao_matriz_derivada'].fillna('OUTROS').astype(str)
        
        # 1. Encoders para features de entrada
        input_encoders = {}
        categorical_cols = ['estado', 'pauta_acao', 'nome_movimento']
        encoded_feats = []
        
        for col in categorical_cols:
            le = LabelEncoder()
            classes = list(df[col].unique())
            if 'OUTROS' not in classes:
                classes.append('OUTROS')
            le.fit(classes)
            df[col + '_encoded'] = le.transform(df[col])
            input_encoders[col] = le
            encoded_feats.append(df[col + '_encoded'].values.reshape(-1, 1))
            
        # Extrair similaridades cosseno
        sim_cols = [col for col in df.columns if col.startswith('sim_score_')]
        sim_features = df[sim_cols].values
        
        # Feature Fusion X
        X = np.hstack([embeddings, sim_features] + encoded_feats)
        logging.info(f"Feature matrix X (Fusão de Atributos) com shape: {X.shape}")
        
        # 2. Encoders para os targets
        target_encoders = {}
        
        # Target Micro (Ação Derivada)
        le_derivada = LabelEncoder()
        y_derivada_encoded = le_derivada.fit_transform(df['acao_derivada'])
        target_encoders['acao_derivada'] = le_derivada
        
        # Target Macro (Ação Matriz)
        le_matriz = LabelEncoder()
        y_matriz_encoded = le_matriz.fit_transform(df['acao_matriz_derivada'])
        target_encoders['acao_matriz_derivada'] = le_matriz
        
        # Salvar todos os encoders unificados
        all_encoders = {**input_encoders, **target_encoders}
        encoders_path = os.path.join(self.models_dir, "nn_encoders.pkl")
        with open(encoders_path, 'wb') as f:
            pickle.dump(all_encoders, f)
        logging.info(f"Todos os encoders salvos em: {encoders_path}")
        
        return X, y_derivada_encoded, y_matriz_encoded, all_encoders
        
    def train_and_evaluate(self, epochs=80, batch_size=64, lr=0.001):
        # Carregar dados
        X, y_derivada, y_matriz, encoders = self.load_and_prepare_data()
        
        # Dimensões e classes
        input_dim = X.shape[1]
        num_classes_derivada = len(encoders['acao_derivada'].classes_)
        num_classes_matriz = len(encoders['acao_matriz_derivada'].classes_)
        
        # Divisão em Treino e Teste (80% treino, 20% teste)
        # Usamos y_matriz para estratificação para garantir que todas as macroclasses estejam no treino e teste
        from collections import Counter
        class_counts = Counter(y_matriz)
        stratify_safe = None if min(class_counts.values()) < 2 else y_matriz
        
        X_train, X_test, y_deriv_train, y_deriv_test, y_mat_train, y_mat_test = train_test_split(
            X, y_derivada, y_matriz, test_size=0.2, random_state=42, stratify=stratify_safe
        )
        
        # Calcular pesos de classes para lidar com desbalanceamento severo (Inverse Frequency Weighting)
        # Classes mais raras receberão pesos exponencialmente maiores na loss
        def get_class_weights(y_targets, num_classes):
            counts = np.bincount(y_targets, minlength=num_classes)
            # Evitar divisão por zero e suavizar pesos
            weights = 1.0 / (counts + 1.0)
            # Normalizar
            weights = weights / np.sum(weights) * num_classes
            return torch.tensor(weights, dtype=torch.float32)
            
        weights_derivada = get_class_weights(y_deriv_train, num_classes_derivada)
        weights_matriz = get_class_weights(y_mat_train, num_classes_matriz)
        
        # Datasets e Loaders
        train_dataset = LandConflictDataset(X_train, y_deriv_train, y_mat_train)
        test_dataset = LandConflictDataset(X_test, y_deriv_test, y_mat_test)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        # Instanciar a rede neural
        model = MultiTaskDNN(input_dim, num_classes_derivada, num_classes_matriz)
        
        # Critérios de perda balanceados
        criterion_derivada = nn.CrossEntropyLoss(weight=weights_derivada)
        criterion_matriz = nn.CrossEntropyLoss(weight=weights_matriz)
        
        # Otimizador Adam com decaimento de peso para regularização L2
        optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
        
        # Scheduler para diminuir o learning rate quando a loss do treino estagnar
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
        
        logging.info("Iniciando treinamento da Rede Neural Multi-Task no PyTorch...")
        
        for epoch in range(1, epochs + 1):
            model.train()
            train_loss = 0.0
            
            for inputs, targets_deriv, targets_mat in train_loader:
                optimizer.zero_grad()
                
                # Forward
                pred_deriv, pred_mat = model(inputs)
                
                # Calcular perdas das duas tarefas paralelas
                loss_deriv = criterion_derivada(pred_deriv, targets_deriv)
                loss_mat = criterion_matriz(pred_mat, targets_mat)
                
                # Loss Total Combinada (Média ponderada: prioriza ligeiramente a tarefa mais complexa)
                total_loss = 0.6 * loss_deriv + 0.4 * loss_mat
                
                # Backward e Otimização
                total_loss.backward()
                optimizer.step()
                
                train_loss += total_loss.item() * inputs.size(0)
                
            train_loss /= len(train_loader.dataset)
            scheduler.step(train_loss)
            
            if epoch % 10 == 0 or epoch == 1:
                logging.info(f"Epoch {epoch}/{epochs} | Loss de Treino: {train_loss:.4f} | LR: {optimizer.param_groups[0]['lr']:.6f}")
                
        # ==========================================
        # 4. AVALIAÇÃO DE DESEMPENHO NO TESTE
        # ==========================================
        model.eval()
        all_preds_deriv = []
        all_preds_mat = []
        
        with torch.no_grad():
            for inputs, _, _ in test_loader:
                pred_deriv, pred_mat = model(inputs)
                
                # Predição por maior valor de probabilidade (argmax)
                preds_deriv = torch.argmax(pred_deriv, dim=1).numpy()
                preds_mat = torch.argmax(pred_mat, dim=1).numpy()
                
                all_preds_deriv.extend(preds_deriv)
                all_preds_mat.extend(preds_mat)
                
        acc_deriv = accuracy_score(y_deriv_test, all_preds_deriv)
        acc_mat = accuracy_score(y_mat_test, all_preds_mat)
        
        logging.info(f"Rede Neural - Acurácia Ação Derivada (Micro): {acc_deriv * 100:.2f}%")
        logging.info(f"Rede Neural - Acurácia Ação Matriz (Macro): {acc_mat * 100:.2f}%")
        
        # Converter classes numéricas de volta aos nomes textuais originais com tratamento resiliente de suporte
        labels_deriv = np.unique(np.concatenate([y_deriv_test, all_preds_deriv]))
        target_names_deriv = [encoders['acao_derivada'].classes_[i] for i in labels_deriv]
        
        labels_mat = np.unique(np.concatenate([y_mat_test, all_preds_mat]))
        target_names_mat = [encoders['acao_matriz_derivada'].classes_[i] for i in labels_mat]
        
        report_deriv = classification_report(y_deriv_test, all_preds_deriv, labels=labels_deriv, target_names=target_names_deriv, zero_division=0)
        report_mat = classification_report(y_mat_test, all_preds_mat, labels=labels_mat, target_names=target_names_mat, zero_division=0)
        
        # Salvar relatórios textuais de validação da rede
        with open(os.path.join(self.models_dir, "nn_report_derivada.txt"), "w", encoding="utf-8") as f:
            f.write(f"Rede Neural Multi-Task - Acurácia Derivada: {acc_deriv * 100:.2f}%\n\n")
            f.write(report_deriv)
            
        with open(os.path.join(self.models_dir, "nn_report_matriz.txt"), "w", encoding="utf-8") as f:
            f.write(f"Rede Neural Multi-Task - Acurácia Matriz: {acc_mat * 100:.2f}%\n\n")
            f.write(report_mat)
            
        # Salvar o modelo PyTorch treinado
        model_path = os.path.join(self.models_dir, "land_conflict_mt_dnn.pth")
        torch.save(model.state_dict(), model_path)
        logging.info(f"Pesos da Rede Neural PyTorch salvos em: {model_path}")
        
        return {
            'accuracy_derivada': acc_deriv,
            'accuracy_matriz': acc_mat,
            'report_derivada': report_deriv,
            'report_matriz': report_mat
        }

if __name__ == "__main__":
    trainer = NeuralNetworkTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
    trainer.train_and_evaluate(epochs=80, batch_size=64, lr=0.001)
