import streamlit as st
from huggingface_hub import InferenceClient
import os
from PIL import Image
import io

st.set_page_config(page_title="Cyfrowa Konsultacja Fryzjerska AI", page_icon="✂️")

st.title("✂️ Wirtualna Metamorfoza Fryzjerska AI")
st.write("Witaj! Prześlij swoje zdjęcie i odpowiedz na pytania, aby sztuczna inteligencja wygenerowała Twoją nową fryzurę!")

# --- BAZA WZORCÓW I INSPIRACJI DLA AI ---
BAZA_STYLE = [
    {
        "nazwa": "Klasyczny Bob z prostą linią",
        "tekstura": "Proste",
        "prompt_ai": "photo of a person with a short sleek bob haircut, straight hair, professional salon hair style, realistic lighting",
    },
    {
        "nazwa": "Soft Waves - Miękkie Fale",
        "tekstura": "Lekko się falują / wywijają",
        "prompt_ai": "photo of a person with medium length soft wavy hair, beach waves haircut, natural volume, professional styling",
    },
    {
        "nazwa": "Curly Shag / Zdefiniowany Skręt",
        "tekstura": "Kręcone / mocny skręt",
        "prompt_ai": "photo of a person with short curly shag haircut, defined natural curls, volumetric curly hair",
    }
]

# Formularz
with st.form("konsultacja_form"):
    st.subheader("1. Tekstura i oczekiwania")
    tekstura = st.radio(
        "Jaka jest Twoja naturalna struktura włosów?",
        ["Proste", "Lekko się falują / wywijają", "Kręcone / mocny skręt"]
    )

    st.subheader("2. Twoje zdjęcie twarzy")
    uploaded_file = st.file_uploader("Wgraj zdjęcie twarzy", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("🎨 Wygeneruj moją metamorfozę AI")

if submitted:
    if uploaded_file is None:
        st.error("Proszę najpierw wgrać zdjęcie twarzy!")
    else:
        st.divider()
        st.header("✨ Wynik Metamorfozy AI")
        
        col_orig, col_ai = st.columns(2)
        with col_orig:
            st.image(uploaded_file, caption="Twoje obecne zdjęcie", use_container_width=True)
            
        wybrana_fryzura = BAZA_STYLE[0]
        for style in BAZA_STYLE:
            if style["tekstura"] == tekstura:
                wybrana_fryzura = style
                break

        with col_ai:
            with st.spinner("AI przetwarza propozycję fryzury... To może zająć chwilę."):
                try:
                    token = st.secrets.get("HF_TOKEN") or os.environ.get("HF_TOKEN")
                    
                    if not token:
                        st.error("Brak skonfigurowanego klucza HF_TOKEN w Secrets Streamlit.")
                    else:
                        client = InferenceClient(api_key=token)
                        
                        # Generowanie propozycji stilistycznej za pomocą darmowego modelu Stable Diffusion
                        image = client.text_to_image(
                            prompt=wybrana_fryzura["prompt_ai"],
                            model="black-forest-labs/FLUX.1-schnell"
                        )
                        
                        st.image(image, caption=f"Inspiracja AI dla Ciebie: {wybrana_fryzura['nazwa']}", use_container_width=True)
                        st.success("Oto wygenerowana propozycja fryzury!")

                except Exception as e:
                    st.error(f"Wystąpił błąd podczas generowania: {str(e)}")

                except Exception as e:
                    st.error(f"Wystąpił błąd podczas generowania AI: {str(e)}")
