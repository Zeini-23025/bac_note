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

### Script Simple
- ✅ Recherche rapide par numéro de candidat
- 📊 Affichage du statut (Admis/Échec)
- 📈 Extraction de la moyenne
- 📚 Identification de la série
- 👤 Affichage des informations du candidat
- 🌐 Support texte arabe et français

### Script Avancé
- 🔎 Analyse détaillée du contenu de la page
- 📋 Extraction d'informations structurées
- 🏫 Recherche d'établissement et académie
- 🏆 Détection des mentions
- 📝 Affichage formaté des résultats
- ⚡ Gestion avancée des erreurs

## 🛠️ Dépendances

- `requests` - Pour les requêtes HTTP
- `beautifulsoup4` - Pour l'analyse HTML
- `lxml` - Parser XML/HTML rapide

## 📋 Formats de résultats

### Informations extraites :
- **Statut** : Admis ✅ / Échec ❌
- **Moyenne** : Note générale
- **Série** : Sciences Naturelles (SN), Sciences Mathématiques (SM), Lettres
- **Nom** : Informations du candidat
- **Mention** : Mention obtenue (si applicable)

### Exemples d'affichage :

```
🔍 Résultats pour le candidat 123456:
==================================================
✅ STATUT: ADMIS/RÉUSSI
📊 MOYENNE: 12.50
📚 SÉRIE: Sciences Naturelles (SN)
👤 INFO: NOM DU CANDIDAT | Détails
```

## 🌍 Support linguistique

Le script reconnaît automatiquement :
- **Français** : admis, réussi, échec, refusé, moyenne, série
- **Arabe** : ناجح, راسب, المعدل, العلوم الطبيعية, الرياضيات, الآداب

## ⚠️ Notes importantes

1. **Respect du serveur** : Les scripts incluent des délais pour éviter de surcharger le site mauribac.com
2. **Encodage** : Support complet UTF-8 pour les caractères arabes
3. **Gestion d'erreurs** : Gestion robuste des erreurs de connexion et de parsing
4. **Timeout** : Timeout de 10 secondes pour les requêtes HTTP

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
