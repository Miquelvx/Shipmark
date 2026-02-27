import streamlit as st
from PIL import Image#, ImageGrab
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

# CSS
st.markdown(
    """
    <style>
    /* Styles CSS pour le titre d'une page */
    .page-title {
        text-align: center;
        font-weight: bold;
        font-size: xxx-large;
        color: #ffffff;
    }
    .dot {
    height: 25px;
    width: 25px;
    background-color: #bbb;
    border-radius: 50%;
    color : red;
    display: inline-block;
    }
    /* Styles CSS pour les conteneurs de texte */
    .txt-container-flower {
        background-color: #010713;
        color: #ffffff;
        border-radius: 25% 10% / 5% 20%;
        padding: 5%;
        margin: 3%;
        text-align: justify;
    }

    /* Solid border */
    hr.solid {
        border-top: 3px solid #ffffff;
    }
    h3 {
        color: #ffffff;
        backdrop-filter: blur(1px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------------------------
# permet d'afficher notre logo sur la sidebar
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

add_background('Background.png')
model = YOLO("Model.pt")
left, cent,last = st.columns(3)
with cent:
    st.image(add_logo(logo_path="logo_shipmark.png", width=200, height=200))
#my_logo = add_logo(logo_path="logo_shipmark.png", width=200, height=200)
#st.image(my_logo)
st.markdown("<h3 style='text-align: center;'>Testez notre algorithme d'identification des bateaux en téléchargeant une photo ci-dessous.</h3>" , unsafe_allow_html=True)
fichiers_images = st.file_uploader("Upload your image", type = ["jpg", "jpeg", "png"], label_visibility = 'hidden')
if fichiers_images is not None:
    col1, col2 = st.columns(2)
    # Adding image to the first column if image is uploaded
    with col1:
         if fichiers_images:
            # Opening the uploaded image
            image = Image.open(fichiers_images)
            # Adding the uploaded image to the page with a caption
            st.image(image,
                        use_column_width=True
                        )
            st.markdown("<h6 style='text-align: center;'>Image téléchargée</h1>", unsafe_allow_html=True)
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    with col2:
        st.image(res_plotted,
                use_column_width=True
                 )
        st.markdown("<h6 style='text-align: center;'>Bateau detecté</h1>", unsafe_allow_html=True)
        st.image("Legende.PNG")