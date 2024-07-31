# Utiliser une image de base officielle de Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /API_Commandes

# Copier les fichiers de l'application dans le conteneur
COPY . /API_Commandes

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que l'application utilisera
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "API_Commandes.main:app", "--host", "0.0.0.0", "--port", "8000"]