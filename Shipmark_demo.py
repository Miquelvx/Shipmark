import os
os.system("pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless")
os.system("pip install opencv-python-headless")

## ======== Importation des librairies ======== ##
import streamlit as st
from PIL import Image, ImageOps
from zipfile import ZipFile
from ultralytics import YOLO
import base64
import os
import random

hide_menu = """
<style>
#MainMenu{
    visibility:hidden;
    }
footer{
    visibility:hidden;
}
footer:after{
    content : 'Copyright @2024: Shipmark';
    display:block;
    position:relative;
    color:white;
    visibility: visible;
    padding:5px;
    top:2px;
}
header{
    visibility:hidden;
}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

## ======== CSS ======== ##
st.markdown(
    """
    <style>
    /* --- GENERAL --- */
    h3, h5, h6 {
        color: #E2E8F0; /* Lighter gray for better readability */
        text-shadow: 1px 1px 3px black;
    }

    p {
        color: #ffffff;
    }

    /* --- CONTAINERS --- */
    .block-container {
        background-color: rgba(15, 23, 42, 0.85); /* Slate 900 with transparency */
        border: 1px solid #475569; /* Slate 600 */
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0 2rem 0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }

    /* --- WIDGETS --- */

    /* Buttons */
    .stButton > button, .stLinkButton > a {
        border-radius: 8px;
        border: 1px solid #3399FF;
        background-color: transparent;
        color: #3399FF;
        transition: all 0.2s ease-in-out;
        font-weight: 600;
        text-decoration: none;
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background-color: #3399FF;
        color: white;
        border-color: #3399FF;
        transform: scale(1.02);
    }    .stButton > button:active, .stLinkButton > a:active {
        background-color: #0077E6 !important;
        border-color: #0077E6 !important;
        color: white;
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #475569;
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        padding: 1rem;
    }
    .stFileUploader label {
        color: #E2E8F0;
        font-size: 1.1rem;
    }
    .stFileUploader [data-testid="stFileUploadDropzone"] p {
        color: #94A3B8; /* Slate 400 */
    }

    </style>
    """,
    unsafe_allow_html=True
)

## ======== Définition des foncitons ======== ##
@st.cache_resource
def add_logo(logo_path, width, height):
    #Lire et retourner l'image
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def add_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_background('./img_app/Background.png')

## ======== Importation du model YOLO ======== ##
model = YOLO("Model_Shipmark.pt")

## ======== Logo Shipmark ======== ##
with open("./img_app/logo_shipmark.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{logo_base64}" width="200" height="200"></div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; padding: 0 0 2rem 0; color: #ffffff;'>Testez notre algorithme d'identification de bateaux.</h3>" , unsafe_allow_html=True)

## ======== Text Projet ======== ##
col_text, col_img = st.columns([3, 1], gap="large")

with col_text:
    st.markdown("""
        <p style='text-align: justify; margin-bottom: 0;'>
            Initié par Airbus, Shipmark est un projet de groupe développant une technologie de surveillance maritime basée sur un algorithme de détection de bateaux et de points de repère. 
            Son objectif ? Disposer d'un outil pour identifier/prévenir la pêche illégale, les dégazages ou déballastages en mer dans les zones maritimes. 
            <br> <br> 
            Projet sélectionné pour la finale des projets de fin d'études (Engineering Project Awards 2024).
        </p>
        """, unsafe_allow_html=True)

## ======== Affiche Shipmark ======== ##
with col_img:
    st.image("./img_app/Affiche_Shipmark.png", 
             caption="Affiche du projet Shipmark", 
             use_column_width=True)
    
## ======== Bouton Dashboard CometML ======== ##
st.write("")
col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    st.link_button("📈 Voir le Dashboard Comet", "https://www.comet.com/miquelvx/shipmark-entrainement/view/8r3SrgJj76S1pXVBHekpc4av8/panels", use_container_width=True)
st.markdown("---")


## ======== Fonction et Initialisation ======== ##
@st.cache_data
def get_random_demo_images(n=5, rerun_trigger=0): # Ajout d'un trigger pour le cache
    folder_path = "test_demo"
    if not os.path.exists(folder_path):
        return []
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return []
    return random.sample(files, min(len(files), n))

if 'selected_demo' not in st.session_state:
    st.session_state.selected_demo = None
if 'rerun_trigger' not in st.session_state:
    st.session_state.rerun_trigger = 0
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

def reset_demo_selection():
    st.session_state.selected_demo = None

## ======== Sélection d'images ======== ##
with st.container():
    st.markdown("<h5 style='color: #ffffff;'>1. Téléchargez votre propre image. (image satellite obligatoire)</h5>", unsafe_allow_html=True)
    fichiers_images = st.file_uploader("Déposez une image ici ou cliquez pour parcourir.", type=["jpg", "jpeg", "png"], label_visibility='collapsed', key=f"uploader_{st.session_state.uploader_key}", on_change=reset_demo_selection)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    head1, head2 = st.columns([0.7, 0.3])
    with head1:
        st.markdown("<h5 style='color: #ffffff;'>2. Ou choisissez une image de notre sélection</h5>", unsafe_allow_html=True)
    with head2:
        if st.button("🔄 Changer la sélection"):
            st.session_state.rerun_trigger += 1
            st.rerun()

    st.write("")

    demo_images = get_random_demo_images(5, rerun_trigger=st.session_state.rerun_trigger)
    if demo_images:
        cols = st.columns(5)
        for idx, img_name in enumerate(demo_images):
            img_path = os.path.join("test_demo", img_name)
            with cols[idx]:
                container = st.container()
                try:
                    img_display = Image.open(img_path)
                    
                    is_selected = (st.session_state.selected_demo == img_path)
                    
                    if is_selected:
                        img_to_show = ImageOps.expand(img_display, border=10, fill='#3399FF')
                    else:
                        img_to_show = img_display

                    container.image(img_to_show, use_column_width=True)
                    
                    if container.button("Sélectionner", key=f"demo_{idx}", use_container_width=True):
                        st.session_state.selected_demo = img_path if not is_selected else None
                        st.session_state.uploader_key += 1
                        st.rerun()
                except Exception as e:
                    st.error(f"Erreur image: {img_name}")
    st.markdown('</div>', unsafe_allow_html=True)


## ======== Affichage des images ======== ##
image_source = fichiers_images or st.session_state.selected_demo

if image_source is not None:
    st.markdown("---")
    if st.button("❌ Effacer la sélection et analyser une autre image"):
        st.session_state.selected_demo = None
        st.session_state.uploader_key += 1
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        image = Image.open(image_source)
        st.image(image, use_column_width=True)
        st.markdown("<h6 style='text-align: center; color: #ffffff'>Image analysée</h6>", unsafe_allow_html=True)
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    with col2:
        st.image(res_plotted,
                use_column_width=True
                 )
        st.markdown("<h6 style='text-align: center; color: #ffffff'>Image traitée</h1>", unsafe_allow_html=True)

    ## ======== Légende et Pourcentage ======== ## 
    col1, col2, col3 = st.columns([0.2, 1, 0.2])
    with col2: 
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                conf = box.conf.item() * 100
                st.markdown(f"<p style='text-align: center; color: #E2E8F0;'>Détection à {conf:.1f}% d'un bateau</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; color: #E2E8F0;'>Aucun bateau détecté</p>", unsafe_allow_html=True)

        st.markdown("""
            <div style="margin-top: 15px; font-size: 0.8rem; color: #E2E8F0; display: flex; flex-direction: column; align-items: center;">
                <div style="display:flex; align-items:center; margin-bottom:10px;">
                    <span style="display:inline-block; width:12px; height:12px; background-color:blue; border:1px solid white; margin-right:10px;"></span> Bateau
                </div>
                <div style="display:flex; flex-direction: row; gap: 30px;">
                    <div style="display:flex; align-items:center;">
                        <span style="display:inline-block; width:10px; height:10px; background-color:red; border-radius:50%; margin-right:5px;"></span> Proue
                    </div>
                    <div style="display:flex; align-items:center;">
                        <span style="display:inline-block; width:10px; height:10px; background-color:yellow; border-radius:50%; margin-right:5px;"></span> Poupe babord
                    </div>
                    <div style="display:flex; align-items:center;">
                        <span style="display:inline-block; width:10px; height:10px; background-color:white; border-radius:50%; margin-right:5px;"></span> Poupe tribord
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

## ======== Footer ======== ##
st.markdown(
    """
    <div style='text-align: center; margin-top: 50px; padding-bottom: 20px; color: #94A3B8;'>
        <hr style='border-color: #475569; margin-bottom: 20px;'>
        <p style='margin: 0 0 0.5rem;'>© 2024 Shipmark </p>
        <p style='margin: 0 7rem;'> Développé par Anne-Julie Hottin - Maël Gueguen - Nicolas Rousselot Théo Masson - Cédric Song - Mike Leveleux. 
    </div>
    """,
    unsafe_allow_html=True
)
