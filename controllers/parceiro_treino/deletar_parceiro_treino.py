from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from models.parceiro_treino.parceiro_treino import ParceiroTreino
from database import engine  # Seu arquivo de configuração do SQLAlchemy
def deletar_parceiros_treino_antigos(db: Session):
    """
    Deleta parceiros de treino com mais de 7 dias.
    """
    # Define o limite de 7 dias
    data_limite = datetime.now(timezone.utc) - timedelta(days=7)

    try:
        # Executa a deleção
        parceiros_deletados = db.query(ParceiroTreino).filter(
            ParceiroTreino.datetime_registro < data_limite
        ).delete(synchronize_session=False)
        
        db.commit()
        print(f"{parceiros_deletados} registros deletados com sucesso.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar parceiros de treino antigos: {str(e)}")
# Cria a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def agendar_delecao_parceiros():
    # Inicia o agendador
    scheduler = BackgroundScheduler()
    
    # Agendar a função para rodar diariamente
    scheduler.add_job(
        func=lambda: deletar_parceiros_com_sessao(), 
        trigger="interval", 
        days=1,  # Roda uma vez por dia
        id="delete_old_parceiros",
        replace_existing=True
    )
    
    scheduler.start()

def deletar_parceiros_com_sessao():
    # Cria uma nova sessão
    db = SessionLocal()
    try:
        deletar_parceiros_treino_antigos(db)
    finally:
        db.close()

# Iniciar o agendador no sistema
if __name__ == "__main__":
    agendar_delecao_parceiros()
    while True:
        pass  # Mantém o script rodando
