import os
import sys
import argparse
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_resources_exist(category, root_dir="."):
    """Checks if processed data files and trained ML models exist for a given category."""
    required_files = [
        os.path.join(root_dir, f"data/processed/{category}/dataset_with_similarities.csv"),
        os.path.join(root_dir, f"data/processed/{category}/chunk_embeddings.npy"),
        os.path.join(root_dir, f"models/{category}/classifier_derivada.pkl"),
        os.path.join(root_dir, f"models/{category}/classifier_matriz.pkl"),
        os.path.join(root_dir, f"models/{category}/encoders.pkl"),
        os.path.join(root_dir, f"models/{category}/land_conflict_mt_dnn.pth"),
        os.path.join(root_dir, f"models/{category}/nn_encoders.pkl")
    ]
    return all(os.path.exists(f) for f in required_files)

def run_ml_pipeline(category, root_dir="."):
    """Runs all modules in the ML pipeline sequentially for a given category."""
    from ingestion.ingestion_manager import ingest_dataset, get_category_files, ingest_from_pdfs_only, ingest_from_excel_only
    import glob, os
    
    logging.info("==================================================================")
    logging.info(f"INICIANDO PIPELINE DE MACHINE LEARNING: {category.upper()}")
    logging.info("==================================================================")
    
    excel_path, zip_path = get_category_files(category, root_dir)
    raw_dir = os.path.join(root_dir, "data", "raw", category)
    loose_pdfs = glob.glob(os.path.join(raw_dir, "**", "*.pdf"), recursive=True)
    
    if excel_path and zip_path:
        # Modo padrão: planilha + ZIP
        logging.info(f"Etapa 1/4: Ingestao de dados ({excel_path} + {zip_path})...")
        df_raw = ingest_dataset(excel_path, zip_path, output_dir=os.path.join(root_dir, f"data/processed/{category}"))
    elif excel_path and not zip_path and not loose_pdfs:
        # Modo Excel-Only: Apenas planilha, sem PDFs
        logging.info(f"Etapa 1/4: Modo Excel-Only — Extraindo textos sintéticos de {excel_path}")
        df_raw = ingest_from_excel_only(excel_path, output_dir=os.path.join(root_dir, f"data/processed/{category}"))
    elif loose_pdfs:
        # Modo PDF-only: somente PDFs soltos na pasta, sem planilha
        logging.info(f"Etapa 1/4: Modo PDF-only — {len(loose_pdfs)} PDFs encontrados em {raw_dir}")
        df_raw = ingest_from_pdfs_only(raw_dir, output_dir=os.path.join(root_dir, f"data/processed/{category}"))
        if df_raw is None:
            logging.warning(f"Falha ao processar PDFs para '{category}'. Puxando próximo...")
            return
    else:
        logging.warning(f"Arquivos (XLSX ou ZIP ou PDFs) ausentes para a categoria '{category}'. Puxando próximo...")
        return
        
    logging.info("Etapa 2/4: Limpeza de texto e segmentacao semantica com spaCy...")
    from preprocessing.text_preprocessor import preprocess_and_chunk_dataset
    df_chunked = preprocess_and_chunk_dataset(os.path.join(root_dir, f"data/processed/{category}/dataset_processado.csv"), output_dir=os.path.join(root_dir, f"data/processed/{category}"))
    
    logging.info("Etapa 3/4: Geracao de embeddings e calculo de similaridade cosseno...")
    from embeddings.embedding_generator import process_embeddings_and_similarities
    df_sims, embs = process_embeddings_and_similarities(
        os.path.join(root_dir, f"data/processed/{category}/dataset_chunked.csv"), 
        output_dir=os.path.join(root_dir, f"data/processed/{category}"), 
        category=category
    )
    
    logging.info("Etapa 4/4: Treinamento dos classificadores supervisionados (HistGradientBoosting + MT-DNN PyTorch)...")
    from training.classifier_trainer import ModelTrainer
    trainer = ModelTrainer(
        os.path.join(root_dir, f"data/processed/{category}/dataset_with_similarities.csv"), 
        os.path.join(root_dir, f"data/processed/{category}/chunk_embeddings.npy"), 
        models_dir=os.path.join(root_dir, f"models/{category}")
    )
    results = trainer.train_and_evaluate()
    
    from training.neural_network_trainer import NeuralNetworkTrainer
    nn_trainer = NeuralNetworkTrainer(
        os.path.join(root_dir, f"data/processed/{category}/dataset_with_similarities.csv"), 
        os.path.join(root_dir, f"data/processed/{category}/chunk_embeddings.npy"), 
        models_dir=os.path.join(root_dir, f"models/{category}")
    )
    nn_results = nn_trainer.train_and_evaluate(epochs=100)
    
    logging.info("==================================================================")
    logging.info(f"PIPELINE {category.upper()} CONCLUIDO COM SUCESSO!")
    logging.info(f"HGB - Acuracia Derivada: {results['accuracy_derivada']*100:.2f}% | Acuracia Matriz: {results['accuracy_matriz']*100:.2f}%")
    logging.info(f"MT-DNN - Acuracia Derivada: {nn_results['accuracy_derivada']*100:.2f}% | Acuracia Matriz: {nn_results['accuracy_matriz']*100:.2f}%")
    logging.info("==================================================================")


def launch_flask_app():
    """Launches the Flask web server."""
    logging.info("Iniciando servidor Flask do Observatorio IA...")
    web_app_path = "web/app.py"
    
    try:
        subprocess.run([sys.executable, web_app_path], check=True)
    except KeyboardInterrupt:
        logging.info("Servidor Flask interrompido pelo usuario. Encerrando.")
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Observatório IA Pipeline")
    parser.add_argument("--category", type=str, default=None, help="Treinar uma categoria especifica (agrario, urbano, aguas, floresta)")
    parser.add_argument("--all", action="store_true", help="Iterar sobre todas as categorias")
    parser.add_argument("--force", action="store_true", help="Forcar o re-treinamento integral")
    parser.add_argument("--no-server", action="store_true", help="Nao iniciar o servidor Flask ao fim")
    args = parser.parse_args()
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(root_dir)
    
    # Categorias padrao suportadas
    valid_categories = ["agrario", "urbano", "aguas", "floresta"]
    
    categories_to_run = []
    if args.all:
        categories_to_run = valid_categories
    elif args.category:
        if args.category in valid_categories:
            categories_to_run = [args.category]
        else:
            logging.error(f"Categoria invalida. Escolha entre: {', '.join(valid_categories)}")
            sys.exit(1)
    else:
        categories_to_run = valid_categories
        
    for cat in categories_to_run:
        if args.force or not check_resources_exist(cat, root_dir):
            run_ml_pipeline(cat, root_dir)
        else:
            logging.info(f"Recursos para '{cat}' estao completos. Use --force para retreinar.")
            
    if not args.no_server:
        launch_flask_app()
