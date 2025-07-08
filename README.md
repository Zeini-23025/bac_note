# 🎓 Recherche Résultats BAC 2024 - Mauritanie

## Description

Ce projet contient des scripts Python pour rechercher les résultats du Baccalauréat 2024 en Mauritanie via le site mauribac.com.

## 🔍 Fonctionnalités

### Script Simple (`bac_simple.py`)
- ✅ **Détection robuste du statut** : Patterns explicites + fallback basé sur la moyenne
- 📊 Affichage du statut (Admis/Échec/Session de rattrapage) en français et arabe
- 📚 Identification automatique de la série (SN, SM, Lettres)
- 📈 **Extraction intelligente de la moyenne** avec validation numérique
- 👤 Extraction et affichage des informations du candidat
- 🌐 Support complet du texte arabe et français
- ⚡ Interface simple : mode interactif ou ligne de commande
- 🎯 **Gestion des cas limites** : session de rattrapage (8 ≤ moyenne < 10)

### Script Avancé (`bac_avance.py`)
- 🔎 **Analyse approfondie** avec logique de détection avancée
- 📊 **Affichage enrichi avec emojis** et hiérarchisation des informations
- 📈 Affichage de la moyenne numérique précise (ex: 11.13)
- 📋 Recherche de patterns multiples dans le contenu (français/arabe)
- 🏆 **Détection intelligente des mentions** et informations complémentaires
- 🔄 Mode interactif continu avec possibilité de recherches multiples
- 📝 **Formatage structuré** des résultats avec séparateurs visuels
- ⚡ Gestion robuste des erreurs et timeout configuré
- 🕒 Pause automatique entre les requêtes (protection serveur)

### Script Traitement en Lot (`recherche_batch.py`) 🆕
- 📁 **Traitement automatique** de fichiers avec multiples matricules
- 🔄 **Extraction complète** : nom, matricule, statut, moyenne, série
- 📊 **Export enrichi** vers `resultats_batch.txt` avec format structuré
- 📈 **Résumé statistique détaillé** : admis, session, échec, erreurs
- 🎯 **Gestion avancée des statuts** : session de rattrapage incluse
- ⚡ **Traitement robuste** avec gestion d'erreurs individuelles
- 📋 **Format d'entrée flexible** : nom:matricule par ligne
- 🕒 **Horodatage automatique** des exports

## 📁 Structure du projet

```
bac_note/
├── bac_simple.py      # Script simple et rapide avec détection robuste
├── bac_avance.py      # Script avancé avec analyse détaillée et affichage enrichi
├── recherche_batch.py # Script de traitement en lot avec export automatique
├── test_complet.txt   # Fichier de test avec candidats d'exemple
├── resultats_batch.txt # Export automatique des résultats en lot
├── etu.txt           # Fichier d'exemple pour les matricules
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation complète
```

## 🚀 Installation

1. **Cloner ou télécharger le projet**

   ```git
   git clone https://github.com/Zeini-23025/bac_note.git
   ```
2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Utilisation

### Script Simple (`bac_simple.py`)

**Mode interactif :**
```bash
python bac_simple.py
```

**Ligne de commande :**
```bash
python bac_simple.py [numéro_candidat]
```

**Exemple :**
```bash
python bac_simple.py 123456
```

### Script Avancé (`bac_avance.py`)

**Mode interactif avec analyse détaillée :**
```bash
python bac_avance.py
```

### Script Traitement en Lot (`recherche_batch.py`)

**Traitement de fichiers avec matricules :**
```bash
python recherche_batch.py
```

Le script lit automatiquement le fichier `etu.txt` (ou tout fichier texte spécifié) contenant les matricules au format :
```
nom:matricule
nom2:matricule2
```

**Exemple de fichier d'entrée :**
```
memi:19736
mintous:19798
candidat_test:12345
```

**Résultats exportés automatiquement dans `resultats_batch.txt`**


## 🛠️ Dépendances

- `requests` - Pour les requêtes HTTP
- `beautifulsoup4` - Pour l'analyse HTML
- `lxml` - Parser XML/HTML rapide

## 📋 Formats de résultats

### Informations extraites :

**Script Simple :**
- **Statut** : Admis ✅ / Échec ❌ / Session de rattrapage 🔄 (reconnaissance arabe/français)
- **Série** : Sciences Naturelles (SN), Sciences Mathématiques (SM), Lettres
- **Moyenne** : Extraction automatique avec validation numérique
- **Info candidat** : Extraction automatique du nom et détails

**Script Avancé :**
- **Statut détaillé** : Avec contexte complet du résultat et emojis
- **Moyenne précise** : Valeur numérique exacte (ex: 11.13)
- **Admission** : Confirmation du statut d'admission avec logique avancée
- **Analyse patterns** : Recherche de multiples informations dans le contenu

**Script Traitement en Lot :**
- **Export structuré** : Nom, Matricule, Statut, Admission, Série, Moyenne
- **Résumé statistique** : Compteurs détaillés par statut
- **Horodatage** : Date et heure de traitement
- **Gestion d'erreurs** : Candidats non trouvés ou en erreur

### Exemples d'affichage :

**Script Simple (`bac_simple.py`) :**
```
🔍 Résultats pour le candidat 23025:
==================================================
✅ STATUT: ADMIS/RÉUSSI
📚 SÉRIE: Sciences Naturelles (SN)
📊 MOYENNE: 11.13
```

**Script Avancé (`bac_avance.py`) :**
```
🎓 === RÉSULTATS POUR LE CANDIDAT N°23025 === 🎓
📊 Informations extraites :
• 👤 Nom: candidat_admis
• 🎯 Statut: Admis
• 🏆 Admission: Admis
• 📚 Série: BAC - Sciences naturelles (SN)
• 📈 Moyenne: 11.13
==================================================
```

**Script Traitement en Lot (export `resultats_batch.txt`) :**
```
RÉSULTATS RECHERCHE BAC - TRAITEMENT EN LOT
==================================================
Date: 2025-07-08 20:04:19

Nom: candidat_admis
Matricule: 23025
Statut: Admis
Admission: Admis
Série: BAC - Sciences naturelles (SN)
Moyenne: 11.13
------------------------------

📊 RÉSUMÉ STATISTIQUE :
• Candidats traités: 4
• ✅ Admis: 1 (25.0%)
• 🔄 Session de rattrapage: 1 (25.0%)
• ❌ Échec: 2 (50.0%)
• 📈 Moyenne générale: 8.43
```

## 🌍 Support linguistique

Le système reconnaît automatiquement :
- **Français** : admis, réussi, échec, refusé, moyenne, série, session de rattrapage
- **Arabe** : ناجح, راسب, المعدل, العلوم الطبيعية, الرياضيات, الآداب

## 🎯 Logique de Détection Avancée

### Détection du Statut (Améliorations 2025) :
1. **Patterns explicites** : Recherche de mots-clés "Admis", "Échec", "Session"
2. **Fallback intelligent** basé sur la moyenne :
   - ≥ 10.00 : **Admis** ✅
   - 8.00 ≤ moyenne < 10.00 : **Session de rattrapage** 🔄
   - < 8.00 : **Échec** ❌
3. **Validation croisée** : Vérification de cohérence entre patterns et moyenne

### Extraction de la Moyenne :
- **Patterns multiples** : "Moyenne", "المعدل", formats numériques
- **Validation numérique** : Vérification de la plage [0-20]
- **Précision décimale** : Support des moyennes avec décimales (ex: 11.13)

### Identification de la Série :
- **Français** : Sciences naturelles (SN), Sciences mathématiques (SM), Lettres
- **Arabe** : العلوم الطبيعية, الرياضيات, الآداب
- **Normalisation** : Format uniforme BAC - [Série]

## ⚠️ Notes importantes

1. **Respect du serveur** : Pauses automatiques (2 secondes) entre les requêtes pour éviter de surcharger mauribac.com
2. **Encodage** : Support complet UTF-8 pour les caractères arabes avec détection automatique
3. **Gestion d'erreurs** : Timeout de 10 secondes et gestion robuste des erreurs de connexion
4. **Différences entre scripts** :
   - **Simple** : Affichage rapide avec détection robuste du statut
   - **Avancé** : Analyse détaillée avec affichage enrichi et emojis
   - **Batch** : Traitement en lot avec export automatique et statistiques
5. **Headers personnalisés** : Simulation de navigateur réel pour éviter les blocages
6. **Session de rattrapage** : Prise en charge complète des candidats en session (8-10)
7. **Export enrichi** : Format structuré avec horodatage et résumé statistique

## 🆕 Nouveautés Version 2025

### Améliorations Majeures :
- ✅ **Détection robuste** : Patterns explicites + fallback sur moyenne
- 🔄 **Session de rattrapage** : Gestion complète des cas 8 ≤ moyenne < 10
- 📊 **Traitement en lot** : Script `recherche_batch.py` pour fichiers multiples
- 📈 **Export enrichi** : Format structuré avec statistiques détaillées
- 🎨 **Affichage amélioré** : Emojis, hiérarchisation, formatage avancé
- 🛡️ **Robustesse** : Gestion des cas limites et erreurs individuelles

### Fichiers Ajoutés :
- `recherche_batch.py` : Traitement en lot automatisé
- `test_complet.txt` : Jeu de tests pour validation
- `resultats_batch.txt` : Export automatique des résultats

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Créer une Pull Request

## 📝 Licence

Ce projet est destiné à un usage éducatif et personnel. Respectez les conditions d'utilisation du site mauribac.com.

## 🐛 Résolution des problèmes

### Erreurs courantes :

**Erreur de connexion :**
```
❌ Erreur de connexion: [Details]
```
- Vérifiez votre connexion internet
- Le site mauribac.com peut être temporairement indisponible

**Numéro invalide :**
```
❌ Veuillez fournir un numéro valide
```
- Assurez-vous que le numéro ne contient que des chiffres
- Vérifiez que le numéro de candidat est correct

**Statut non déterminé :**
```
❓ STATUT: Non déterminé
```
- Le candidat n'a peut-être pas de résultats publiés
- Vérifiez le numéro de candidat
- Avec la nouvelle logique, utilise le fallback sur la moyenne si disponible

**Erreurs de traitement en lot :**
```
❌ Erreur lors du traitement de [matricule]: [détails]
```
- Vérifiez le format du fichier d'entrée (nom:matricule)
- Assurez-vous que les matricules sont valides
- Les erreurs individuelles n'interrompent pas le traitement global

### Validation du Système :

**Tests recommandés :**
1. **Test unitaire** : Vérifier avec `test_complet.txt`
   ```bash
   python recherche_batch.py
   ```
2. **Validation manuelle** : Comparer avec le site officiel
3. **Test de robustesse** : Matricules invalides ou inexistants

**Fichiers de test inclus :**
- `test_complet.txt` : Candidats avec différents statuts (admis, session, échec)
- Résultats attendus documentés dans `resultats_batch.txt`

## 📞 Support

Pour toute question ou problème, créez une issue dans le repository du projet.
