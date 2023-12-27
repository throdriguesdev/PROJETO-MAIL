import os
import smtplib
import msvcrt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import logging  # Adicionado: Importar o módulo logging
logging.basicConfig(filename='emails.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class EmailAssociation:
    def __init__(self):
        self.mapa_email_arquivo = {}
        self.corpo_email = None

    def associar_email_arquivo(self, email, arquivo):
        self.mapa_email_arquivo[email] = arquivo

    def obter_arquivo_por_email(self, email):
        return self.mapa_email_arquivo.get(email, None)

    def definir_corpo_email(self, corpo):
        self.corpo_email = corpo

    def obter_corpo_email(self):
        return self.corpo_email

def obter_credenciais_smtp():
    print("Digite suas credenciais SMTP:")
    remetente = input("E-mail (remetente): ")
    senha = obter_senha(permitir_visualizacao=False)
    return remetente, senha

def enviar_email(remetente, senha, destinatario, corpo_email, caminho_anexo):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    mensagem = MIMEMultipart()
    mensagem['Subject'] = 'Relatório de Despesas M-1'
    mensagem['From'] = remetente
    mensagem['To'] = destinatario

    parte_corpo = MIMEText(corpo_email, 'html')
    mensagem.attach(parte_corpo)

    if caminho_anexo:
        nome_anexo = os.path.basename(caminho_anexo)
        parte_anexo = adicionar_anexo(caminho_anexo, nome_anexo)
        mensagem.attach(parte_anexo)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as servidor_smtp:
            servidor_smtp.starttls()
            servidor_smtp.login(remetente, senha)
            servidor_smtp.sendmail(remetente, destinatario, mensagem.as_string())
            logging.info(f'E-mail enviado para {destinatario} com sucesso!')
        print(f'E-mail enviado para {destinatario} com sucesso!')
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def obter_senha(permitir_visualizacao=False):
    try:
        senha = getpass.getpass("Digite sua senha: ")
        if permitir_visualizacao:
            logging.info(f"Senha: {senha}")
        return senha
    except Exception as e:
        logging.error(f"Erro ao obter a senha: {e}")
        return ""
        
    logging.info("Digite sua senha: ")

    while True:
        chave = msvcrt.getch().decode("utf-8")

        if chave == "\r" or chave == "\n":
            break
        elif chave == "\x08":  # Backspace
            if senha:
                senha = senha[:-1]
                print("\b \b", end="", flush=True)
        elif chave == "\x03" and permitir_visualizacao:  # Ctrl+C para permitir visualização
            logging.info(f"Senha: {senha}")
        else:
            senha += chave
          

    print()
    return senha

def adicionar_anexo(caminho_anexo, nome_anexo):
    parte_anexo = MIMEBase('application', 'octet-stream')
    parte_anexo.set_payload(open(caminho_anexo, 'rb').read())
    encoders.encode_base64(parte_anexo)
    parte_anexo.add_header('Content-Disposition', f'attachment; filename={nome_anexo}')
    return parte_anexo

def ler_corpo_email():
    try:
        with open("corpo.html", "r", encoding="utf-8") as file:
            corpo_email = file.read()
        return corpo_email
    except Exception as e:
       logging.error(f"Erro ao ler corpo do e-mail: {e}")
    return ""

def consultar_emails_anexos_salvos(associacao_email):
    logging.info("\nE-mails e Anexos Salvos:")
    for email, arquivo in associacao_email.mapa_email_arquivo.items():
        logging.info(f"E-mail: {email}, Anexo: {arquivo}.xlsx" if arquivo else f"E-mail: {email}")

def associar_e_mapear_emails_arquivos():
    relacao_email_arquivo = [
        ('thiago.rodrigues@gmail.com', 'centro-de-custo'),
        ('thiago.rodrigues2@gmail.com,', 'centro-de-custo2'),
        ('thiago.rodrigues3@gmail.com,', 'centro-de-custo3'),
    ]

    associacao_email = EmailAssociation()
    for email, arquivo in relacao_email_arquivo:
        associacao_email.associar_email_arquivo(email, arquivo)
    
    return associacao_email

def main():
    while True:
        print("\nMenu:")
        print("1. Enviar E-mail")
        print("2. Consultar E-mails e Anexos Salvos")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email, senha = obter_credenciais_smtp()
            associacao_email = associar_e_mapear_emails_arquivos()
            corpo_email = ler_corpo_email()

            for destinatario, arquivo in associacao_email.mapa_email_arquivo.items():
                if arquivo:
                    caminho_anexo = os.path.join(os.path.dirname(__file__), f'{arquivo}.xlsx')
                    
                    if os.path.exists(caminho_anexo):
                        enviar_email(email, senha, destinatario, corpo_email, caminho_anexo)
                    else:
                        print(f"Arquivo {caminho_anexo} não encontrado.")
                else:
                    enviar_email(email, senha, destinatario, corpo_email, None)
        elif escolha == '2':
            associacao_email = associar_e_mapear_emails_arquivos()
            consultar_emails_anexos_salvos(associacao_email)
            print (associacao_email.mapa_email_arquivo)
        elif escolha == '3':
            break
        else:
            logging.error("Escolha inválida. Tente novamente.")
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
