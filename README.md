# 🎓 Recherche Résultats BAC 2024 - Mauritanie

## Description

Ce projet contient des scripts Python pour rechercher et afficher les résultats du Baccalauréat 2024 en Mauritanie via le site mauribac.com.

## 📁 Structure du projet

```
bac_note/
├── bac_simple.py      # Script simple et rapide
├── bac_avance.py      # Script avancé avec analyse détaillée
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation
```

## 🚀 Installation

1. **Cloner ou télécharger le projet**
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

## 🔍 Fonctionnalités

### Script Simple (`bac_simple.py`)
- ✅ Recherche rapide par numéro de candidat
- 📊 Affichage du statut (Admis/Échec) en français et arabe
- 📚 Identification automatique de la série (SN, SM, Lettres)
- 👤 Extraction et affichage des informations du candidat
- 🌐 Support complet du texte arabe et français
- ⚡ Interface simple : mode interactif ou ligne de commande
- 🎯 Affichage concis et formaté des résultats essentiels

### Script Avancé (`bac_avance.py`)
- 🔎 Analyse approfondie et extraction détaillée des données
- 📊 Affichage de la moyenne numérique précise (ex: 11.13)
- 📋 Recherche de patterns multiples dans le contenu
- 🏆 Détection des mentions et informations complémentaires
- � Mode interactif continu avec possibilité de recherches multiples
- 📝 Formatage structuré des résultats avec séparateurs visuels
- ⚡ Gestion robuste des erreurs et timeout configuré
- 🕒 Pause automatique entre les requêtes (protection serveur)

## 🛠️ Dépendances

- `requests` - Pour les requêtes HTTP
- `beautifulsoup4` - Pour l'analyse HTML
- `lxml` - Parser XML/HTML rapide

## 📋 Formats de résultats

### Informations extraites :

**Script Simple :**
- **Statut** : Admis ✅ / Échec ❌ (reconnaissance arabe/français)
- **Série** : Sciences Naturelles (SN), Sciences Mathématiques (SM), Lettres
- **Info candidat** : Extraction automatique du nom et détails

**Script Avancé :**
- **Statut détaillé** : Avec contexte complet du résultat
- **Moyenne précise** : Valeur numérique exacte (ex: 11.13)
- **Admission** : Confirmation du statut d'admission
- **Analyse patterns** : Recherche de multiples informations dans le contenu

### Exemples d'affichage :

**Script Simple (`bac_simple.py`) :**
```
🔍 Résultats pour le candidat 23025:
==================================================
✅ STATUT: ADMIS/RÉUSSI
 SÉRIE: Sciences Naturelles (SN)
```

**Script Avancé (`bac_avance.py`) :**
```
=== RÉSULTATS POUR LE CANDIDAT N°23025 ===
Informations trouvées dans le contenu :
• Statut du candidat: 23025 | BAC - Sciences naturelles (sn) Decision 🎉 Admis
• Moyenne générale: 11.13
• Admission: Admis
```

## 🌍 Support linguistique

Le script reconnaît automatiquement :
- **Français** : admis, réussi, échec, refusé, moyenne, série
- **Arabe** : ناجح, راسب, المعدل, العلوم الطبيعية, الرياضيات, الآداب

## ⚠️ Notes importantes

1. **Respect du serveur** : Le script avancé inclut des pauses automatiques (2 secondes) entre les requêtes pour éviter de surcharger mauribac.com
2. **Encodage** : Support complet UTF-8 pour les caractères arabes avec détection automatique
3. **Gestion d'erreurs** : Timeout de 10 secondes et gestion robuste des erreurs de connexion
4. **Différences entre scripts** :
   - **Simple** : Affichage rapide des informations essentielles
   - **Avancé** : Analyse détaillée avec moyennes précises et recherche continue
5. **Headers personnalisés** : Simulation de navigateur réel pour éviter les blocages

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

## 📞 Support

Pour toute question ou problème, créez une issue dans le repository du projet.
