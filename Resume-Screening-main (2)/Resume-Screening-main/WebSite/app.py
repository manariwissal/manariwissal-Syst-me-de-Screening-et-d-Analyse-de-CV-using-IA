"""
Application Streamlit simplifiée pour extraire les informations clés d'un CV

Développé par l'équipe Explorateur de Savoir
© 2025 - Explorateur de Savoir
"""
import streamlit as st
import docx
import PyPDF2
from extractor import extract_all_info
from matcher import calculate_detailed_matching

# Configuration de la page
st.set_page_config(
    page_title="Extraction d'informations CV",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec design moderne
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header avec gradient */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        text-align: center;
        color: white;
    }
    
    .header-container h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .header-container p {
        font-size: 1.3rem;
        opacity: 0.95;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Upload section */
    .upload-section {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        border: 2px dashed #667eea;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #764ba2;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Info boxes avec design moderne */
    .info-box {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        background: white;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    .info-box:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .info-box h4 {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Badge pour le nom */
    .name-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        margin: 1rem 0;
    }
    
    /* Badges pour compétences */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem;
        box-shadow: 0 3px 10px rgba(245, 87, 108, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-badge:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
    }
    
    /* Expérience card */
    .exp-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .exp-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .exp-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .exp-company {
        color: #667eea;
        font-size: 1.1rem;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    .exp-date {
        color: #7f8c8d;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .exp-desc {
        color: #555;
        line-height: 1.6;
        margin-top: 0.5rem;
    }
    
    /* Education card */
    .edu-card {
        background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #00acc1;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .edu-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .edu-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .edu-school {
        color: #00acc1;
        font-size: 1.1rem;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: white;
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 500;
        color: #2c3e50;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(132, 250, 176, 0.3);
    }
    
    /* Matching score styles */
    .match-score-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        text-align: center;
    }
    
    .match-score-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 3rem;
        font-weight: 700;
        color: white;
        position: relative;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .match-score-high {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    .match-score-medium {
        background: linear-gradient(135deg, #fbc531 0%, #feca57 100%);
    }
    
    .match-score-low {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }
    
    .match-detail-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .match-detail-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .match-detail-value {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .progress-bar-container {
        background: #e0e0e0;
        border-radius: 10px;
        height: 30px;
        margin: 1rem 0;
        overflow: hidden;
        position: relative;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .progress-high {
        background: linear-gradient(90deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    .progress-medium {
        background: linear-gradient(90deg, #fbc531 0%, #feca57 100%);
    }
    
    .progress-low {
        background: linear-gradient(90deg, #f5576c 0%, #f093fb 100%);
    }
    
    .matched-skill {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-weight: 500;
    }
    
    .missing-skill {
        background: linear-gradient(135deg, #f5f7fa 0%, #e0e0e0 100%);
        color: #7f8c8d;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-weight: 500;
        border: 1px solid #ddd;
    }
    
    .job-keyword {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .job-description-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        border: 2px solid #667eea;
    }
    
    /* Footer personnalisé */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #7f8c8d;
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
    }
    
    .custom-footer strong {
        color: #667eea;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


def extract_text_from_pdf(file):
    """Extrait le texte d'un fichier PDF"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file):
    """Extrait le texte d'un fichier DOCX"""
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def extract_text_from_txt(file):
    """Extrait le texte d'un fichier TXT"""
    try:
        text = file.read().decode('utf-8')
    except UnicodeDecodeError:
        text = file.read().decode('latin-1')
    return text


def handle_file_upload(uploaded_file):
    """Gère l'upload et l'extraction du texte selon le type de fichier"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Type de fichier non supporté. Veuillez uploader un PDF, DOCX ou TXT.")


def main():
    # En-tête avec design moderne
    st.markdown("""
        <div class="header-container">
            <h1>📄 Extraction d'informations CV</h1>
            <p>Analysez automatiquement votre CV et extrayez les informations clés en quelques secondes</p>
            <p style='margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;'>Développé par l'équipe <strong>Explorateur de Savoir</strong></p>
        </div>
    """, unsafe_allow_html=True)

    # Section d'upload avec style amélioré
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📤 Télécharger votre CV")
        st.markdown("**Formats supportés :** PDF, DOCX, TXT")
        uploaded_file = st.file_uploader(
            "", 
            type=["pdf", "docx", "txt"], 
            key="file_uploader",
            help="Sélectionnez un fichier CV pour commencer l'analyse"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            # Afficher le nom du fichier
            st.markdown(f"""
                <div class="success-box">
                    ✅ Fichier chargé : <strong>{uploaded_file.name}</strong>
                </div>
            """, unsafe_allow_html=True)
            
            # Extraire le texte du fichier
            with st.spinner("🔄 Extraction du texte en cours..."):
                resume_text = handle_file_upload(uploaded_file)
            
            # Extraire les informations
            with st.spinner("🔍 Analyse du CV en cours..."):
                info = extract_all_info(resume_text)
            
            # Afficher les résultats avec design amélioré
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("""
                <h2 style='text-align: center; color: #2c3e50; margin: 2rem 0; font-size: 2.5rem;'>
                    📋 Informations extraites
                </h2>
            """, unsafe_allow_html=True)
            
            # Nom avec badge stylisé
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 👤 Nom")
            st.markdown(f'<div class="name-badge">{info["nom"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Compétences avec badges colorés
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 💼 Compétences")
            if info['competences'] and len(info['competences']) > 0 and info['competences'][0] != "Aucune compétence détectée":
                skills_html = ""
                for skill in info['competences']:
                    skills_html += f'<span class="skill-badge">{skill}</span>'
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #7f8c8d; font-style: italic;">Aucune compétence détectée</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Expériences avec cartes stylisées
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 💼 Expériences professionnelles")
            if info['experiences'] and len(info['experiences']) > 0 and info['experiences'][0].get('poste') != 'Aucune expérience détectée':
                for exp in info['experiences']:
                    exp_html = '<div class="exp-card">'
                    exp_html += f'<div class="exp-title">{exp["poste"]}</div>'
                    if exp.get('entreprise'):
                        exp_html += f'<div class="exp-company">🏢 {exp["entreprise"]}</div>'
                    if exp.get('dates'):
                        exp_html += f'<div class="exp-date">📅 {", ".join(exp["dates"])}</div>'
                    if exp.get('description'):
                        desc = exp['description'][:250] + "..." if len(exp['description']) > 250 else exp['description']
                        exp_html += f'<div class="exp-desc">{desc}</div>'
                    exp_html += '</div>'
                    st.markdown(exp_html, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #7f8c8d; font-style: italic;">Aucune expérience détectée</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Diplômes avec cartes stylisées
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 🎓 Diplômes et formations")
            if info['diplomes'] and len(info['diplomes']) > 0 and info['diplomes'][0].get('diplome') != 'Aucun diplôme détecté':
                for diplome in info['diplomes']:
                    edu_html = '<div class="edu-card">'
                    edu_html += f'<div class="edu-title">🎓 {diplome["diplome"]}</div>'
                    if diplome.get('etablissement'):
                        edu_html += f'<div class="edu-school">🏛️ {diplome["etablissement"]}</div>'
                    if diplome.get('annee'):
                        edu_html += f'<div class="exp-date">📅 {", ".join(diplome["annee"])}</div>'
                    edu_html += '</div>'
                    st.markdown(edu_html, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #7f8c8d; font-style: italic;">Aucun diplôme détecté</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Option pour voir le texte brut
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.expander("📝 Afficher le texte brut du CV", expanded=False):
                st.text_area("", resume_text, height=300, label_visibility="collapsed")
            
            # Section de matching avec la fiche de poste
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("""
                <h2 style='text-align: center; color: #2c3e50; margin: 2rem 0; font-size: 2.5rem;'>
                    🎯 Matching avec la fiche de poste
                </h2>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="job-description-box">
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>📋 Entrez la description du poste</h3>
                    <p style='color: #7f8c8d; margin-bottom: 1rem;'>
                        En tant que RH, collez ou tapez la description complète du poste à pourvoir. 
                        Le système calculera automatiquement le score de correspondance avec le CV.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Description du poste",
                height=200,
                placeholder="Exemple : Nous recherchons un développeur Python expérimenté avec des compétences en machine learning, Django, et bases de données SQL. Le candidat doit avoir au moins 3 ans d'expérience...",
                help="Entrez la description complète du poste à pourvoir"
            )
            
            if job_description and job_description.strip():
                # Calculer le matching
                with st.spinner("🔄 Calcul du matching en cours..."):
                    matching_results = calculate_detailed_matching(resume_text, info, job_description)
                
                # Afficher le score de matching principal
                match_percentage = matching_results['match_percentage']
                score_class = "match-score-high" if match_percentage >= 70 else "match-score-medium" if match_percentage >= 40 else "match-score-low"
                progress_class = "progress-high" if match_percentage >= 70 else "progress-medium" if match_percentage >= 40 else "progress-low"
                
                st.markdown(f"""
                    <div class="match-score-container">
                        <div class="match-score-circle {score_class}">
                            {match_percentage:.1f}%
                        </div>
                        <h3 style='color: #2c3e50; font-size: 1.8rem; margin-bottom: 1rem;'>
                            Score de correspondance
                        </h3>
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill {progress_class}" style="width: {match_percentage}%">
                                {match_percentage:.1f}%
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Détails du matching
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="match-detail-box">
                            <div class="match-detail-title">📊 Similarité globale</div>
                            <div class="match-detail-value">{matching_results['overall_similarity']*100:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="match-detail-box">
                            <div class="match-detail-title">💼 Compétences</div>
                            <div class="match-detail-value">{matching_results['skills_similarity']*100:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class="match-detail-box">
                            <div class="match-detail-title">🏢 Expériences</div>
                            <div class="match-detail-value">{matching_results['experience_similarity']*100:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Matching des compétences
                skills_match = matching_results['skills_match']
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("#### ✅ Compétences correspondantes")
                if skills_match['matched']:
                    matched_html = ""
                    for skill in skills_match['matched']:
                        matched_html += f'<span class="matched-skill">✓ {skill}</span>'
                    st.markdown(matched_html, unsafe_allow_html=True)
                    st.markdown(f"<p style='margin-top: 1rem; color: #2c3e50;'><strong>{skills_match['match_count']}/{skills_match['total_cv_skills']}</strong> compétences correspondent au poste</p>", unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #7f8c8d; font-style: italic;">Aucune compétence correspondante trouvée</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Compétences manquantes
                if skills_match['missing']:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("#### ⚠️ Compétences du CV non mentionnées dans le poste")
                    missing_html = ""
                    for skill in skills_match['missing']:
                        missing_html += f'<span class="missing-skill">{skill}</span>'
                    st.markdown(missing_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Mots-clés de la fiche de poste
                if matching_results['job_keywords']:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("#### 🔑 Mots-clés importants du poste")
                    keywords_html = ""
                    for keyword in matching_results['job_keywords']:
                        keywords_html += f'<span class="job-keyword">{keyword}</span>'
                    st.markdown(keywords_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement du fichier : {str(e)}")
            st.info("💡 Assurez-vous que le fichier est un CV valide au format PDF, DOCX ou TXT.")
    
    # Footer avec crédit de l'équipe
    st.markdown("""
        <div class="custom-footer">
            <p>© 2025 - <strong>Explorateur de Savoir</strong> | Tous droits réservés</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
