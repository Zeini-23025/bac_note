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
        for pattern in patterns_found:
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
    Cherche des patterns spécifiques liés aux résultats du bac
    """
    patterns_found = []

    # Nettoyer le texte pour une meilleure recherche
    text_clean = re.sub(r'\s+', ' ', text)

    # Patterns à rechercher
    patterns = [
        (rf'{numero_candidat}.*?(?:admis|refusé|échec|réussi|mention)',
         'Statut du candidat'),
        (r'moyenne?\s*[:\-]?\s*(\d+[.,]\d+)', 'Moyenne générale'),
        (r'mention\s*[:\-]?\s*(\w+)', 'Mention obtenue'),
        (r'(?:admis|réussi|succès)', 'Admission'),
        (r'(?:refusé|échec|échoué)', 'Échec'),
        (r'série\s*[:\-]?\s*([A-Z]+)', 'Série du bac'),
        (r'établissement\s*[:\-]?\s*([^|]+)', 'Établissement'),
        (r'académie\s*[:\-]?\s*([^|]+)', 'Académie'),
    ]

    for pattern, description in patterns:
        matches = re.finditer(pattern, text_clean, re.IGNORECASE | re.UNICODE)
        for match in matches:
            if match.group(1) if len(match.groups()) > 0 else match.group(0):
                has_groups = len(match.groups()) > 0
                value = match.group(1) if has_groups else match.group(0)
                patterns_found.append(f"{description}: {value.strip()}")

    return patterns_found


def afficher_info_candidat(info, numero_candidat):
    """
    Affiche les informations du candidat de manière formatée
    """
    print(f"Candidat n°{numero_candidat} - Informations trouvées :")
    print("-" * 50)

    for key, value in info.items():
        # Nettoyer le texte
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
