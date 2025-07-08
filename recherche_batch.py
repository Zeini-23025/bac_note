#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour rechercher les résultats BAC en lot à partir d'un fichier de matricules
Usage: python recherche_batch.py [fichier_matricules]
"""

import sys
import time
import os
import requests
from bs4 import BeautifulSoup
import re


def lire_matricules(fichier_path):
    """
    Lit les matricules depuis un fichier texte
    Format attendu: nom:matricule ou juste matricule
    """
    matricules = []
    
    try:
        with open(fichier_path, 'r', encoding='utf-8') as f:
            for ligne_num, ligne in enumerate(f, 1):
                ligne = ligne.strip()
                if not ligne or ligne.startswith('#'):
                    continue
                
                # Gérer les formats: "nom:matricule" ou juste "matricule"
                if ':' in ligne:
                    nom, matricule = ligne.split(':', 1)
                    matricule = matricule.strip()
                    nom = nom.strip()
                else:
                    matricule = ligne.strip()
                    nom = f"Candidat_{matricule}"
                
                # Vérifier que le matricule est valide
                if matricule.isdigit():
                    matricules.append((nom, matricule))
                else:
                    print(f"⚠️  Ligne {ligne_num}: Matricule invalide '{matricule}' ignoré")
    
    except FileNotFoundError:
        print(f"❌ Fichier '{fichier_path}' non trouvé")
        return []
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return []
    
    return matricules


def extraire_info_bac(numero_candidat):
    """
    Recherche et extrait les informations détaillées du BAC
    """
    url = f'https://www.mauribac.com/fr/bac-2024-uKolupoGL/numero/{numero_candidat}/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        text = soup.get_text()
        
        # Extraire les informations
        info = {
            'statut': 'Non déterminé',
            'admission': 'Non trouvé',
            'serie': 'Non spécifiée',
            'moyenne': 'Non disponible'
        }
        
        # Rechercher le statut et l'admission avec logique améliorée
        text_lower = text.lower()
        moyenne_val = None
        
        # D'abord extraire la moyenne pour la logique de fallback
        moyenne_match = re.search(r'المعدل\s*(\d+\.?\d*)', text)
        if not moyenne_match:
            moyenne_match = re.search(r'moyenne?\s*[:\-]?\s*(\d+[.,]\d+)', text, re.IGNORECASE)
        if moyenne_match:
            moyenne_val = float(moyenne_match.group(1).replace(',', '.'))
            info['moyenne'] = moyenne_match.group(1).replace(',', '.')
        
        # Détection du statut avec patterns et logique de moyenne
        if re.search(r'ناجح|réussi|admis|decision.*admis', text, re.IGNORECASE):
            info['statut'] = 'Admis'
            info['admission'] = 'Admis'
        elif re.search(r'راسب|échec|refusé|decision.*refusé', text, re.IGNORECASE):
            info['statut'] = 'Échec'
            info['admission'] = 'Refusé'
        elif moyenne_val is not None and numero_candidat in text:
            # Logique basée sur la moyenne
            if moyenne_val >= 10.0:
                info['statut'] = 'Admis (moyenne ≥10)'
                info['admission'] = 'Admis'
            elif moyenne_val >= 8.0:
                info['statut'] = 'Session de rattrapage (8 ≤ moyenne < 10)'
                info['admission'] = 'Session de rattrapage'
            else:
                info['statut'] = 'Échec (moyenne <8)'
                info['admission'] = 'Échec'
        elif numero_candidat in text and ('bac' in text_lower or 'decision' in text_lower):
            info['statut'] = 'Trouvé (statut à vérifier)'
            info['admission'] = 'À vérifier'
        
        # Rechercher la série
        if 'العلوم الطبيعية' in text or 'sciences naturelles' in text.lower() or 'sn' in text.lower():
            info['serie'] = 'BAC - Sciences naturelles (SN)'
        elif 'الرياضيات' in text or 'sciences mathématiques' in text.lower() or 'sm' in text.lower():
            info['serie'] = 'BAC - Sciences mathématiques (SM)'
        elif 'الآداب' in text or 'lettres' in text.lower():
            info['serie'] = 'BAC - Lettres'
        
        return True, info
        
    except requests.exceptions.RequestException:
        return False, {'statut': 'Erreur de connexion', 'admission': 'Erreur', 'serie': 'Erreur', 'moyenne': 'Erreur'}
    except Exception:
        return False, {'statut': 'Erreur inconnue', 'admission': 'Erreur', 'serie': 'Erreur', 'moyenne': 'Erreur'}


def rechercher_resultats_batch(matricules):
    """
    Recherche les résultats pour une liste de matricules
    """
    print(f"🎓 Recherche en lot - {len(matricules)} candidat(s) à traiter")
    print("=" * 60)
    
    resultats = []
    
    for i, (nom, matricule) in enumerate(matricules, 1):
        print(f"\n[{i}/{len(matricules)}] Traitement de {nom} (#{matricule})")
        print("-" * 50)
        
        try:
            # Utiliser la nouvelle fonction d'extraction
            success, info = extraire_info_bac(matricule)
            
            if success:
                resultats.append({
                    'nom': nom,
                    'matricule': matricule,
                    'statut': info['statut'],
                    'admission': info['admission'],
                    'serie': info['serie'],
                    'moyenne': info['moyenne']
                })
                print(f"✅ Résultat trouvé pour {nom}")
                print(f"   📊 Statut: {info['statut']}")
                print(f"   🎓 Admission: {info['admission']}")
                print(f"   📚 Série: {info['serie']}")
                print(f"   📈 Moyenne: {info['moyenne']}")
            else:
                resultats.append({
                    'nom': nom,
                    'matricule': matricule,
                    'statut': info['statut'],
                    'admission': 'Non trouvé',
                    'serie': 'Non spécifiée',
                    'moyenne': 'Non disponible'
                })
                print(f"❌ Aucun résultat pour {nom}: {info['statut']}")
        
        except Exception as e:
            print(f"❌ Erreur pour {nom}: {e}")
            resultats.append({
                'nom': nom,
                'matricule': matricule,
                'statut': f'Erreur: {e}',
                'admission': 'Erreur',
                'serie': 'Erreur',
                'moyenne': 'Erreur'
            })
        
        # Pause entre les requêtes pour respecter le serveur
        if i < len(matricules):
            print("⏳ Pause de 3 secondes...")
            time.sleep(3)
    
    return resultats


def afficher_resume(resultats):
    """
    Affiche un résumé des résultats avec support session de rattrapage
    """
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA RECHERCHE EN LOT")
    print("=" * 60)
    
    total = len(resultats)
    admis = len([r for r in resultats if r['admission'] == 'Admis'])
    refuses = len([r for r in resultats if r['admission'] in ['Refusé', 'Échec']])
    rattrapage = len([r for r in resultats if r['admission'] == 'Session de rattrapage'])
    non_trouves = len([r for r in resultats if r['admission'] == 'Non trouvé'])
    a_verifier = len([r for r in resultats if r['admission'] == 'À vérifier'])
    erreurs = len([r for r in resultats if r['admission'] == 'Erreur'])
    
    print(f"📈 Total candidats traités: {total}")
    print(f"✅ Admis: {admis}")
    print(f"🔄 Session de rattrapage: {rattrapage}")
    print(f"❌ Refusés/Échec: {refuses}")
    print(f"🔍 À vérifier: {a_verifier}")
    print(f"❓ Non trouvés: {non_trouves}")
    print(f"⚠️  Erreurs: {erreurs}")
    
    # Statistiques par série
    series = {}
    for r in resultats:
        if r['serie'] != 'Erreur' and r['serie'] != 'Non spécifiée':
            series[r['serie']] = series.get(r['serie'], 0) + 1
    
    if series:
        print("\n📚 Répartition par série:")
        for serie, count in series.items():
            print(f"  • {serie}: {count} candidat(s)")
    
    # Statistiques par moyenne
    moyennes_valides = []
    for r in resultats:
        if r['moyenne'] != 'Non disponible' and r['moyenne'] != 'Erreur':
            try:
                moyenne_val = float(r['moyenne'].replace(',', '.'))
                moyennes_valides.append(moyenne_val)
            except:
                pass
    
    if moyennes_valides:
        moyenne_generale = sum(moyennes_valides) / len(moyennes_valides)
        print(f"\n📊 Statistiques des moyennes:")
        print(f"  • Moyenne générale: {moyenne_generale:.2f}")
        print(f"  • Moyenne min: {min(moyennes_valides):.2f}")
        print(f"  • Moyenne max: {max(moyennes_valides):.2f}")
        print(f"  • Candidats avec moyenne: {len(moyennes_valides)}/{total}")
    
    if erreurs > 0:
        print("\n🔍 Détail des erreurs:")
        for r in resultats:
            if r['admission'] == 'Erreur':
                print(f"  • {r['nom']} (#{r['matricule']}): {r['statut']}")


def sauvegarder_resultats(resultats, fichier_sortie="resultats_batch.txt"):
    """
    Sauvegarde les résultats dans un fichier
    """
    try:
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            f.write("RÉSULTATS RECHERCHE BAC - TRAITEMENT EN LOT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for r in resultats:
                f.write(f"Nom: {r['nom']}\n")
                f.write(f"Matricule: {r['matricule']}\n")
                f.write(f"Statut: {r['statut']}\n")
                f.write(f"Admission: {r['admission']}\n")
                f.write(f"Série: {r['serie']}\n")
                f.write(f"Moyenne: {r['moyenne']}\n")
                f.write("-" * 30 + "\n")
        
        print(f"📁 Résultats sauvegardés dans: {fichier_sortie}")
    
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")


def main():
    """
    Fonction principale
    """
    # Déterminer le fichier à utiliser
    if len(sys.argv) > 1:
        fichier_matricules = sys.argv[1]
    else:
        fichier_matricules = "etu.txt"
    
    if not os.path.exists(fichier_matricules):
        print(f"❌ Fichier '{fichier_matricules}' non trouvé")
        print("Usage: python recherche_batch.py [fichier_matricules]")
        return
    
    print(f"📂 Lecture du fichier: {fichier_matricules}")
    
    # Lire les matricules
    matricules = lire_matricules(fichier_matricules)
    
    if not matricules:
        print("❌ Aucun matricule valide trouvé")
        return
    
    print(f"📋 {len(matricules)} matricule(s) trouvé(s):")
    for nom, matricule in matricules:
        print(f"  • {nom}: {matricule}")
    
    # Demander confirmation
    reponse = input(f"\n🤔 Continuer avec la recherche pour {len(matricules)} candidat(s)? (o/N): ")
    if reponse.lower() not in ['o', 'oui', 'y', 'yes']:
        print("🚫 Recherche annulée")
        return
    
    # Effectuer les recherches
    resultats = rechercher_resultats_batch(matricules)
    
    # Afficher le résumé
    afficher_resume(resultats)
    
    # Sauvegarder les résultats
    sauvegarder_resultats(resultats)
    
    print("\n🎯 Traitement terminé!")


if __name__ == "__main__":
    main()
