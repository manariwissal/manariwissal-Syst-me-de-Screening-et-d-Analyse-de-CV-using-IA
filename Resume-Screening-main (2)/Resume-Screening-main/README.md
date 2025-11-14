# 📄 Extraction d'informations CV — Version simplifiée

**Développé par l'équipe Explorateur de Savoir**

## 🎯 À propos du projet

Ce projet simplifié permet d'extraire automatiquement les informations clés d'un CV :
- **Nom** du candidat
- **Compétences** techniques et professionnelles
- **Expériences** professionnelles (poste, entreprise, dates)
- **Diplômes** et formations

L'application combine :
- **Traitement de texte** (expressions régulières, patterns) pour l'extraction d'informations
- **Intelligence Artificielle (IA)** avec TF-IDF et similarité cosinus pour le matching CV/fiche de poste

![Output](image/Output.gif)

---

## ✨ Fonctionnalités

*  **Extraction automatique** des informations clés d'un CV (nom, compétences, expériences, diplômes)
*  **Matching intelligent** entre CV et fiche de poste avec IA (TF-IDF + similarité cosinus)
*  **Score de correspondance** calculé automatiquement avec analyse détaillée
*  **Support multi-formats** : PDF, DOCX, TXT
*  **Interface simple** et intuitive avec Streamlit
*  **Techniques d'IA** pour la comparaison sémantique des textes

---

## ⚙️ Technologies utilisées

| Technologie | Usage |
| ----------- | ----- |
| **Python** | Logique principale et traitement de texte |
| **Streamlit** | Interface utilisateur interactive |
| **python-docx** | Extraction de texte depuis fichiers Word |
| **PyPDF2** | Extraction de texte depuis fichiers PDF |
| **Regex** | Extraction d'informations via patterns |
| **scikit-learn** | TF-IDF et similarité cosinus pour le matching IA |
| **TF-IDF** | Vectorisation des textes pour comparaison intelligente |
| **Similarité cosinus** | Calcul de correspondance entre CV et fiche de poste |

---

## 📁 Structure du projet

```
Resume-Screening/
├── DataSet/              # Dataset d'exemple (optionnel)
├── Model/                # Anciens modèles ML (optionnel)
├── WebSite/              # Application Streamlit
│   ├── app.py           # Application principale
│   ├── extractor.py     # Module d'extraction d'informations
│   └── requirements.txt # Dépendances
└── README.md
```

---

## 🚀 Installation et utilisation

### Prérequis
- Python 3.7 ou supérieur
- pip

### Installation

```bash
# Étape 1 : Naviguer vers le dossier
cd Resume-Screening

# Étape 2 : Installer les dépendances
pip install -r WebSite/requirements.txt

# Étape 3 : Lancer l'application
streamlit run WebSite/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

---

## 📝 Utilisation

1. Ouvrez l'application dans votre navigateur
2. Cliquez sur "Browse files" et sélectionnez un CV (PDF, DOCX ou TXT)
3. Les informations extraites s'affichent automatiquement :
   - Nom du candidat
   - Liste des compétences
   - Expériences professionnelles avec détails
   - Diplômes et formations
4. **En tant que RH** : Entrez la description du poste à pourvoir
5. Le système calcule automatiquement le **score de matching** avec l'IA :
   - Similarité globale (TF-IDF)
   - Similarité des compétences
   - Similarité des expériences
   - Compétences correspondantes et manquantes
   - Mots-clés importants du poste

---

## 🔧 Personnalisation

Le module `extractor.py` contient les fonctions d'extraction. Vous pouvez facilement :
- Ajouter de nouveaux patterns pour détecter des informations
- Améliorer la détection des compétences
- Ajuster les expressions régulières selon vos besoins

---

## 📄 Licence

[MIT License](License)

**© 2025 - Équipe Explorateur de Savoir**

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Améliorer les algorithmes d'extraction
- Ajouter le support de nouveaux formats
- Améliorer l'interface utilisateur
- Corriger les bugs

---

## 🤖 Aspect Intelligence Artificielle

Le projet utilise des **techniques d'IA et de NLP** pour le matching :

### 📍 Localisation de l'IA dans le code

**Fichier : `WebSite/matcher.py`**

1. **TF-IDF (Term Frequency-Inverse Document Frequency)** - Lignes 77, 136
   - Vectorisation des textes pour représenter leur contenu sémantique
   - Permet de comparer la similarité entre CV et fiche de poste

2. **Similarité cosinus** - Ligne 84
   - Calcul de la similarité entre deux vecteurs TF-IDF
   - Score entre 0 et 1 indiquant le degré de correspondance

3. **Extraction de mots-clés** - Lignes 126-155
   - Identification automatique des termes les plus importants dans la fiche de poste
   - Utilise les scores TF-IDF pour classer les mots-clés

4. **Matching intelligent** - Fonction `calculate_detailed_matching()`
   - Combine plusieurs métriques pour un score global
   - Analyse séparée des compétences et expériences

### 🧠 Comment ça fonctionne ?

1. **Vectorisation** : Les textes (CV et fiche de poste) sont convertis en vecteurs numériques via TF-IDF
2. **Comparaison** : La similarité cosinus calcule l'angle entre ces vecteurs
3. **Score** : Un score de 0 à 100% indique le niveau de correspondance

---

## 💡 Améliorations futures possibles

*  Extraction d'informations supplémentaires (email, téléphone, adresse)
*  Support de plus de formats (ODT, RTF)
*  Export des données extraites (JSON, CSV)
*  Utilisation d'embeddings (Word2Vec, BERT) pour une meilleure compréhension sémantique
*  Machine Learning pour améliorer la précision du matching
