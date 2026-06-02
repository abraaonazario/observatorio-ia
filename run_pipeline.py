import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_resources_exist():
    """Checks if processed data files and trained ML models exist."""
    required_files = [
        "data/processed/dataset_with_similarities.csv",
        "data/processed/chunk_embeddings.npy",
        "models/classifier_derivada.pkl",
        "models/classifier_matriz.pkl",
        "models/encoders.pkl"
    ]
    return all(os.path.exists(f) for f in required_files)

def run_ml_pipeline():
    """Runs all modules in the ML pipeline sequentially."""
    logging.info("==================================================================")
    logging.info("INICIANDO PIPELINE DE MACHINE LEARNING DO OBSERVATORIO IA")
    logging.info("==================================================================")
    
    # 1. Ingestão de Dados
    logging.info("Etapa 1/4: Ingestao de dados (Excel + PDFs do ZIP)...")
    from ingestion.ingestion_manager import ingest_dataset
    df_raw = ingest_dataset("PLANILHA AGRARIO 2024  (3).xlsx", "DATALUTA MOV_AGRARIO_2024-20260525T235037Z-3-001.zip")
    
    # 2. Pré-processamento e Chunking Semântico
    logging.info("Etapa 2/4: Limpeza de texto e segmentacao semantica com spaCy...")
    from preprocessing.text_preprocessor import preprocess_and_chunk_dataset
    df_chunked = preprocess_and_chunk_dataset("data/processed/dataset_processado.csv")
    
    # 3. Geração de Embeddings e Scores de Similaridade
    logging.info("Etapa 3/4: Geracao de embeddings e calculo de similaridade cosseno...")
    from embeddings.embedding_generator import process_embeddings_and_similarities
    df_sims, embs = process_embeddings_and_similarities("data/processed/dataset_chunked.csv")
    
    # 4. Treinamento de Modelos Supervisionados
    logging.info("Etapa 4/4: Treinamento dos classificadores supervisionados...")
    from training.classifier_trainer import ModelTrainer
    trainer = ModelTrainer("data/processed/dataset_with_similarities.csv", "data/processed/chunk_embeddings.npy")
    results = trainer.train_and_evaluate()
    
    logging.info("==================================================================")
    logging.info(f"PIPELINE CONCLUIDO COM SUCESSO! Acuracia Derivada: {results['accuracy_derivada']*100:.2f}% | Acuracia Matriz: {results['accuracy_matriz']*100:.2f}%")
    logging.info("==================================================================")

def launch_flask_app():
    """Launches the Flask web server."""
    logging.info("Iniciando servidor Flask do Observatorio IA...")
    web_app_path = "web/app.py"
    
    # Executa o servidor Flask
    try:
        subprocess.run([sys.executable, web_app_path], check=True)
    except KeyboardInterrupt:
        logging.info("Servidor Flask interrompido pelo usuario. Encerrando.")
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {e}")

if __name__ == "__main__":
    # Garantir que estamos no diretório correto do projeto
    cwd = os.getcwd()
    logging.info(f"Diretorio de execucao: {cwd}")
    
    if not check_resources_exist():
        logging.warning("Alguns recursos (dados processados ou modelos de ML) estao ausentes.")
        logging.info("Iniciando treinamento inicial automatizado...")
        run_ml_pipeline()
    else:
        logging.info("Todos os dados processados e modelos foram detectados!")
        logging.info("Deseja forçar o retreinamento? Se sim, execute 'python run_pipeline.py --force'.")
        
        if len(sys.argv) > 1 and sys.argv[1] == "--force":
            logging.info("Forçando o re-treinamento integral do pipeline...")
            run_ml_pipeline()
            
    # Inicia a aplicação web Flask
    launch_flask_app()
