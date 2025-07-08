#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour rechercher les résultats BAC en lot à partir d'un fichier de matricules
Usage: python recherche_batch.py [fichier_matricules]
"""

import sys
import time
import os
from bac_avance import rechercher_resultat_bac


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
            # Utiliser la fonction du script avancé
            success = rechercher_resultat_bac(matricule)
            
            if success:
                resultats.append({
                    'nom': nom,
                    'matricule': matricule,
                    'statut': 'Trouvé'
                })
                print(f"✅ Résultat trouvé pour {nom}")
            else:
                resultats.append({
                    'nom': nom,
                    'matricule': matricule,
                    'statut': 'Non trouvé'
                })
                print(f"❌ Aucun résultat pour {nom}")
        
        except Exception as e:
            print(f"❌ Erreur pour {nom}: {e}")
            resultats.append({
                'nom': nom,
                'matricule': matricule,
                'statut': f'Erreur: {e}'
            })
        
        # Pause entre les requêtes pour respecter le serveur
        if i < len(matricules):
            print("⏳ Pause de 3 secondes...")
            time.sleep(3)
    
    return resultats


def afficher_resume(resultats):
    """
    Affiche un résumé des résultats
    """
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA RECHERCHE EN LOT")
    print("=" * 60)
    
    total = len(resultats)
    trouves = len([r for r in resultats if r['statut'] == 'Trouvé'])
    non_trouves = len([r for r in resultats if r['statut'] == 'Non trouvé'])
    erreurs = len([r for r in resultats if r['statut'].startswith('Erreur')])
    
    print(f"📈 Total candidats traités: {total}")
    print(f"✅ Résultats trouvés: {trouves}")
    print(f"❌ Non trouvés: {non_trouves}")
    print(f"⚠️  Erreurs: {erreurs}")
    
    if erreurs > 0:
        print("\n🔍 Détail des erreurs:")
        for r in resultats:
            if r['statut'].startswith('Erreur'):
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
