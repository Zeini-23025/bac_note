#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour rechercher les résultats du BAC 2024 - Mauritanie
Usage: python bac_simple.py [numero_candidat]
"""

import requests
from bs4 import BeautifulSoup
import sys
import re


def rechercher_bac_simple(numero_candidat):
    """Version simplifiée pour recherche rapide"""
    url = f'https://www.mauribac.com/fr/bac-2024-uKolupoGL/numero/{numero_candidat}/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        text = soup.get_text()

        # Extraction des informations essentielles
        print(f"\n🔍 Résultats pour le candidat {numero_candidat}:")
        print("=" * 50)

        # Chercher les informations clés
        statut_trouve = False
        
        # Recherche plus robuste du statut d'admission
        if re.search(r'ناجح|réussi|admis|decision.*admis', text, re.IGNORECASE):
            print("✅ STATUT: ADMIS/RÉUSSI")
            statut_trouve = True
        elif re.search(r'راسب|échec|refusé|decision.*refusé', text, re.IGNORECASE):
            print("❌ STATUT: ÉCHEC")
            statut_trouve = True
        else:
            # Analyser la moyenne pour déduire le statut
            moyenne_match = re.search(r'المعدل\s*(\d+\.?\d*)', text)
            if not moyenne_match:
                moyenne_match = re.search(r'moyenne?\s*[:\-]?\s*(\d+[.,]\d+)', text, re.IGNORECASE)
            
            if moyenne_match and numero_candidat in text:
                moyenne_val = float(moyenne_match.group(1).replace(',', '.'))
                if moyenne_val >= 10.0:
                    print("✅ STATUT: ADMIS (basé sur moyenne ≥10)")
                elif moyenne_val >= 8.0:
                    print("🔄 STATUT: SESSION DE RATTRAPAGE (8 ≤ moyenne < 10)")
                else:
                    print("❌ STATUT: ÉCHEC (moyenne <8)")
                statut_trouve = True
            elif numero_candidat in text and ('bac' in text.lower() or 'decision' in text.lower()):
                print("🔍 STATUT: Candidat trouvé (statut à vérifier)")
                statut_trouve = True
        
        if not statut_trouve:
            print("❓ STATUT: Non déterminé")

        # Chercher la moyenne (plusieurs patterns)
        moyenne_match = re.search(r'المعدل\s*(\d+\.?\d*)', text)
        if not moyenne_match:
            moyenne_match = re.search(r'moyenne?\s*[:\-]?\s*(\d+[.,]\d+)', text, re.IGNORECASE)
        if moyenne_match:
            moyenne = moyenne_match.group(1).replace(',', '.')
            print(f"📊 MOYENNE: {moyenne}")

        # Chercher la série
        if 'العلوم الطبيعية' in text or 'sn' in text.lower():
            print("📚 SÉRIE: Sciences Naturelles (SN)")
        elif 'الرياضيات' in text or 'sm' in text.lower():
            print("📚 SÉRIE: Sciences Mathématiques (SM)")
        elif 'الآداب' in text or 'lettres' in text.lower():
            print("📚 SÉRIE: Lettres")

        # Afficher le nom si trouvé
        lines = text.split('\n')
        for line in lines:
            if numero_candidat in line and len(line.strip()) > 10:
                # Nettoyer la ligne pour extraire le nom
                clean_line = re.sub(r'[|]+', ' | ', line.strip())
                if len(clean_line) < 200:  # Éviter les lignes trop longues
                    print(f"👤 INFO: {clean_line}")
                break

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    if len(sys.argv) > 1:
        # Utilisation en ligne de commande
        numero = sys.argv[1]
        if numero.isdigit():
            rechercher_bac_simple(numero)
        else:
            print("❌ Veuillez fournir un numéro valide")
    else:
        # Mode interactif
        print("🎓 Recherche rapide - Résultats BAC 2024")
        numero = input("Numéro du candidat: ").strip()
        if numero.isdigit():
            rechercher_bac_simple(numero)
        else:
            print("❌ Numéro invalide")


if __name__ == "__main__":
    main()
