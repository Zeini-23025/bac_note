import requests
from bs4 import BeautifulSoup
import time
import re


def rechercher_resultat_bac(numero_candidat):
    """
    Recherche le résultat du bac pour un numéro de candidat donné
    """
    # URL avec le numéro du candidat
    base_url = 'https://www.mauribac.com/fr/bac-2024-uKolupoGL/numero/'
    url = f'{base_url}{numero_candidat}/'

    # Headers pour simuler un navigateur réel
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/91.0.4472.124 Safari/537.36'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                   'image/webp,*/*;q=0.8'),
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        print(f"Recherche du résultat pour le candidat n°{numero_candidat}...")

        # Faire la requête avec un timeout
        response = requests.get(url, headers=headers, timeout=10)
        # Lève une exception si le statut n'est pas 200
        response.raise_for_status()

        # Détecter l'encodage correct
        response.encoding = response.apparent_encoding or 'utf-8'

        # Parser le HTML
        soup = BeautifulSoup(response.content, 'html.parser',
                             from_encoding='utf-8')

        # Analyser les résultats avec la nouvelle fonction
        success = analyser_resultats_bac(soup, numero_candidat)

        # Si aucun résultat structuré n'est trouvé, afficher le contenu brut
        if not success:
            print("\n=== Contenu principal de la page ===")
            main_content = soup.find("main") or soup.find("body")
            if main_content:
                text = main_content.get_text(strip=True)
                # Filtrer les lignes vides et trop courtes
                lines = [line.strip() for line in text.split('\n')
                         if line.strip() and len(line.strip()) > 3]
                # Afficher les 20 premières lignes significatives
                print("Aperçu du contenu (première partie) :")
                for i, line in enumerate(lines[:15]):
                    ellipsis = '...' if len(line) > 80 else ''
                    print(f"{i+1:2d}. {line[:80]}{ellipsis}")

                if len(lines) > 15:
                    print(f"\n... et {len(lines) - 15} lignes supplémentaires")

        return True

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False


def analyser_resultats_bac(soup, numero_candidat):
    """
    Analyse les résultats du bac et les formate de manière lisible
    """
    print(f"\n=== RÉSULTATS POUR LE CANDIDAT N°{numero_candidat} ===")

    # Rechercher les informations principales
    info_candidat = extraire_info_candidat(soup)
    if info_candidat:
        afficher_info_candidat(info_candidat, numero_candidat)
        return True

    # Si pas d'informations structurées, chercher des patterns
    text_content = soup.get_text()
    patterns_found = chercher_patterns_bac(text_content, numero_candidat)

    if patterns_found:
        print("Informations trouvées dans le contenu :")
        
        # Organiser l'affichage par priorité avec emojis
        priorite_ordre = ['Admission', 'Moyenne générale', 'Série', 'Statut du candidat', 'Mention obtenue', 'Établissement', 'Académie']
        
        patterns_affiches = set()
        
        # Afficher en ordre de priorité
        for priorite in priorite_ordre:
            for pattern in patterns_found:
                if priorite in pattern and pattern not in patterns_affiches:
                    # Ajouter des emojis selon le type d'information
                    if 'Admission' in pattern:
                        if 'Session de rattrapage' in pattern:
                            emoji = "🔄"
                        elif 'Échec' in pattern:
                            emoji = "❌"
                        elif 'Admis' in pattern:
                            emoji = "✅"
                        else:
                            emoji = "❓"
                    elif 'Moyenne' in pattern:
                        emoji = "📊"
                    elif 'Série' in pattern:
                        emoji = "📚"
                    elif 'Statut du candidat' in pattern:
                        emoji = "🔍"
                    else:
                        emoji = "•"
                    
                    print(f"{emoji} {pattern}")
                    patterns_affiches.add(pattern)
        
        # Afficher les autres patterns non prioritaires
        for pattern in patterns_found:
            if pattern not in patterns_affiches:
                print(f"• {pattern}")
        
        return True

    print("Aucune information de résultat trouvée.")
    return False


def extraire_info_candidat(soup):
    """
    Extrait les informations structurées du candidat
    """
    info = {}

    # Rechercher différents sélecteurs
    selectors = [
        {"class": "result"},
        {"class": "resultat"},
        {"class": "candidat"},
        {"class": "student-info"},
        {"class": "bac-result"},
        {"class": "note"},
        {"class": "mention"}
    ]

    for selector in selectors:
        elements = soup.find_all(attrs=selector)
        for element in elements:
            text = element.get_text(strip=True)
            if text and len(text) > 5:
                info[f"element_{len(info)}"] = text

    return info if info else None


def chercher_patterns_bac(text, numero_candidat):
    """
    Cherche des patterns spécifiques liés aux résultats du bac avec logique améliorée
    """
    patterns_found = []

    # Nettoyer le texte pour une meilleure recherche
    text_clean = re.sub(r'\s+', ' ', text)

    # Extraction de la moyenne pour déterminer le statut
    moyenne_val = None
    moyenne_match = re.search(r'المعدل\s*(\d+\.?\d*)', text)
    if not moyenne_match:
        moyenne_match = re.search(r'moyenne?\s*[:\-]?\s*(\d+[.,]\d+)', text_clean, re.IGNORECASE)
    if moyenne_match:
        moyenne_val = float(moyenne_match.group(1).replace(',', '.'))
        patterns_found.append(f"Moyenne générale: {moyenne_val}")

    # Détection du statut d'admission avec logique améliorée
    statut_trouve = False
    
    # Recherche patterns explicites
    if re.search(r'ناجح|réussi|admis|decision.*admis', text, re.IGNORECASE):
        patterns_found.append("Admission: Admis")
        statut_trouve = True
    elif re.search(r'راسب|échec|refusé|decision.*refusé', text, re.IGNORECASE):
        patterns_found.append("Admission: Refusé")
        statut_trouve = True
    elif moyenne_val is not None and numero_candidat in text:
        # Logique basée sur la moyenne
        if moyenne_val >= 10.0:
            patterns_found.append("Admission: Admis (moyenne ≥10)")
        elif moyenne_val >= 8.0:
            patterns_found.append("Admission: Session de rattrapage (8 ≤ moyenne < 10)")
        else:
            patterns_found.append("Admission: Échec (moyenne <8)")
        statut_trouve = True

    # Détection de la série
    if 'العلوم الطبيعية' in text or 'sciences naturelles' in text.lower() or 'sn' in text.lower():
        patterns_found.append("Série: BAC - Sciences naturelles (SN)")
    elif 'الرياضيات' in text or 'sciences mathématiques' in text.lower() or 'sm' in text.lower():
        patterns_found.append("Série: BAC - Sciences mathématiques (SM)")
    elif 'الآداب' in text or 'lettres' in text.lower():
        patterns_found.append("Série: BAC - Lettres")

    # Patterns supplémentaires à rechercher
    additional_patterns = [
        (rf'{numero_candidat}.*?(?:admis|refusé|échec|réussi|mention)',
         'Statut du candidat'),
        (r'mention\s*[:\-]?\s*(\w+)', 'Mention obtenue'),
        (r'établissement\s*[:\-]?\s*([^|]+)', 'Établissement'),
        (r'académie\s*[:\-]?\s*([^|]+)', 'Académie'),
    ]

    for pattern, description in additional_patterns:
        matches = re.finditer(pattern, text_clean, re.IGNORECASE | re.UNICODE)
        for match in matches:
            if match.group(1) if len(match.groups()) > 0 else match.group(0):
                has_groups = len(match.groups()) > 0
                value = match.group(1) if has_groups else match.group(0)
                patterns_found.append(f"{description}: {value.strip()}")

    return patterns_found


def afficher_info_candidat(info, numero_candidat):
    """
    Affiche les informations du candidat de manière formatée améliorée
    """
    print(f"Candidat n°{numero_candidat} - Informations trouvées :")
    print("-" * 50)

    # Organiser l'affichage par priorité
    priorite_affichage = ['Admission', 'Moyenne générale', 'Série', 'Statut du candidat', 'Mention obtenue', 'Établissement', 'Académie']
    
    # Afficher en ordre de priorité
    info_affichees = set()
    for priorite in priorite_affichage:
        for key, value in info.items():
            if priorite in value and key not in info_affichees:
                # Nettoyer le texte
                value_clean = re.sub(r'\s+', ' ', value.strip())
                if len(value_clean) > 100:
                    value_clean = value_clean[:100] + "..."
                
                # Ajouter des emojis selon le type d'information
                if 'Admission' in value:
                    if 'Admis' in value:
                        emoji = "✅"
                    elif 'Session de rattrapage' in value:
                        emoji = "🔄"
                    else:
                        emoji = "❌"
                elif 'Moyenne' in value:
                    emoji = "📊"
                elif 'Série' in value:
                    emoji = "📚"
                else:
                    emoji = "•"
                
                print(f"{emoji} {value_clean}")
                info_affichees.add(key)
    
    # Afficher les autres informations non prioritaires
    for key, value in info.items():
        if key not in info_affichees:
            value_clean = re.sub(r'\s+', ' ', value.strip())
            if len(value_clean) > 100:
                value_clean = value_clean[:100] + "..."
            print(f"• {value_clean}")


def main():
    """
    Fonction principale
    """
    print("=== Recherche de résultats du BAC 2024 ===\n")

    while True:
        try:
            numero = input("Entrez le numéro du candidat "
                           "(ou 'quit' pour quitter) : ").strip()

            if numero.lower() in ['quit', 'exit', 'q']:
                print("Au revoir !")
                break

            if not numero.isdigit():
                print("Veuillez entrer un numéro valide (chiffres uniquement)")
                continue

            success = rechercher_resultat_bac(numero)

            if success:
                print(f"\nRecherche terminée pour le candidat {numero}")
            else:
                print(f"\nÉchec de la recherche pour le candidat {numero}")

            # Pause pour éviter de surcharger le serveur
            time.sleep(2)
            print("\n" + "="*50 + "\n")

        except KeyboardInterrupt:
            print("\n\nArrêt du programme...")
            break
        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
