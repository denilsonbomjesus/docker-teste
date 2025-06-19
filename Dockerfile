# Usa uma imagem base oficial do Python
# 'alpine' é uma distribuição Linux leve, ideal para imagens Docker menores
FROM python:3.9-alpine

# Define o diretório de trabalho dentro do container
# Todos os comandos subsequentes serão executados nesse diretório indicado
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
# O cache do Docker funciona melhor se copiarmos apenas o que é necessário antes de instalar as dependências
COPY app/requirements.txt ./

# Instala as dependências Python listadas em requirements.txt
# --no-cache-dir: Não armazena os arquivos de cache baixados, economizando espaço na imagem
# -r: Lê os pacotes de um arquivo
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código da aplicação (o diretório 'app' completo) para o container
COPY app/ .

# Comando padrão para executar quando o container for iniciado
# python -u: Garante que a saída do Python não seja armazenada em buffer, exibindo-a imediatamente nos logs
CMD ["python", "-u", "main.py"]