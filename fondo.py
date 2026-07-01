import os
from PIL import Image
from rembg import remove
import streamlit as st

def save_uploaded_file(uploaded_file):
    upload_dir = "upload"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def run_background_remover(input_image_file):
    input_image_path =  save_uploaded_file(input_image_file)
    output_image_path = input_image_path.replace('.', '_rmbg.').replace('jpg', 'png').replace('jpeg', 'png')
    try: 
        image = Image.open(input_image_path)
        output = remove(image)
        output.save(output_image_path, "PNG")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Antes")
            st.image(input_image_path, caption="Imagen original")
            with open(input_image_path, "rb") as image_file:
                st.download_button(
                    label="Descargar Imagen Original",
                    data=image_file,
                    file_name=os.path.basename(input_image_path),
                    mime="image/jpeg"
                )
        with col1:
            st.header("Después")
            st.image(output_image_path, caption="Imagen con fondo removido")
            with open(output_image_path, "rb") as image_file:
                st.download_button(
                    label="Descargar Imagen Procesada",
                    data=image_file,
                    file_name=os.path.basename(output_image_path),
                    mime="image/png"
                )
        st.success("Fondo removido exitosamente")
    except Exception as e:
        st.error(f"Ocurrio un error: {e}")

def main():
    st.title("Background Remover")
    uploaded_file = st.file_uploader("Elige un archivo de imagen", type=['jpeg', 'jpg', 'png'])
    if uploaded_file is not None:
        run_background_remover(uploaded_file)

if __name__ == "__main__" :
    main()