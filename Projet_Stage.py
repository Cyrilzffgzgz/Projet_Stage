from datetime import datetime
from collections import defaultdict

server_numeros = []
logs_par_process = {}
info_count_per_minutes = defaultdict(int)
warn_count_per_minutes = defaultdict(int)
error_count_per_minutes = defaultdict(int)

# Compteurs globaux pour les types de messages
total_info_count = 0
total_warn_count = 0
total_error_count = 0

# Lire les dates d'entrée de l'utilisateur
date_format = "%Y-%m-%d %H:%M:%S"
while True:
    try:
        date_debut = input("Entrez la date de début (format YYYY-MM-DD HH:MM:SS): ")
        date_debut = datetime.strptime(date_debut, date_format)
        break
    except ValueError:
        print("Format de date invalide. Veuillez réessayer.")

while True:
    try:
        date_fin = input("Entrez la date de fin (format YYYY-MM-DD HH:MM:SS): ")
        date_fin = datetime.strptime(date_fin, date_format)
        break
    except ValueError:
        print("Format de date invalide. Veuillez réessayer.")

# Lire et traiter les logs
with open('C:\\Users\\w191984\\OneDrive - Worldline SA\\Documents\\Stage_2024\\log_final.txt', 'r') as f:
    n = 0
    for log in f:
        n += 1
        position_length = log.find("Length")
        position_INFO = log.find("INFO")
        position_WARN = log.find("WARN")
        position_ERROR = log.find("ERROR")
        
        if 'Length' in log:
            serv = log.split(" ")
            heure_split = log.split(".")
            heure_split2 = log.split("-")
            heure = heure_split[0]
            local = serv[2]
            numero_serv = serv[5]
            info1 = serv[23]
            info = log[position_INFO:position_length].strip() if position_INFO != -1 else ""
            
            if 'T' in heure:
                heure = heure.replace('T', " ")
            
            # Convertir l'heure en objet datetime
            try:
                log_datetime = datetime.strptime(heure, date_format)
            except ValueError:
                print(f"Format de date invalide dans le log: {log}")
                continue
            
            # Vérifier si le log se trouve entre les deux dates
            if date_debut <= log_datetime <= date_fin:
                warn = log[position_WARN:].strip() 
                error = log[position_ERROR:].strip() 
                if warn or error:
                    log_entree = f"{n} ==> {info, error, warn}"
                    if numero_serv not in logs_par_process:
                        logs_par_process[numero_serv] = []
                        server_numeros.append(numero_serv)
                    logs_par_process[numero_serv].append((heure, local, numero_serv, info, warn, error))
                
                    # Afficher les lignes avec WARN ou ERROR
                    if warn:
                        print(f"Ligne {n} (WARN): {log.strip()}")
                        print("Message de warning détecté.")
                    if error:
                        print(f"Ligne {n} (ERROR): {log.strip()}")
                        print("Message d'erreur détecté.")
                
                # Compter les infos par minute
                if "INFO" in log:
                    minute_key = log_datetime.replace(second=0, microsecond=0)
                    info_count_per_minutes[(minute_key, info)] += 1
                    total_info_count += 1  # Incrémenter le compteur global d'infos
                
                if "WARN" in log:
                    minute_key = log_datetime.replace(second=0, microsecond=0)
                    warn_count_per_minutes[(minute_key, warn)] += 1
                    total_warn_count += 1  # Incrémenter le compteur global de warns
                
                if "ERROR" in log:
                     minute_key = log_datetime.replace(second=0, microsecond=0)
                     if ":" in log[position_ERROR:]:
                        error = log[position_ERROR:log.find(":", position_ERROR)].strip()
                     else:
                        error = log[position_ERROR:].strip()
                     error_count_per_minutes[(minute_key, error)] += 1
                     total_error_count += 1  # Incrémenter le compteur global d'erreurs
# Affichage du nombre d'infos identiques par minute
print("\nNombre d'infos identiques par minute:")
for (minute, info), count in info_count_per_minutes.items():
    print(f"{minute} - {info}: {count} fois")

print("\nNombre de warns identiques par minute:")
for (minute, warn), count in warn_count_per_minutes.items():
    print(f"{minute} - {warn}: {count} fois")

print("\nNombre d'erreurs identiques par minute:")
for (minute, error), count in error_count_per_minutes.items():
    print(f"{minute} - {error}: {count} fois")

# Affichage des compteurs globaux
print("\nNombre total d'infos:", total_info_count)
print("Nombre total de warns:", total_warn_count)
print("Nombre total d'erreurs:", total_error_count)