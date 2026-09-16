import streamlit as st
import replicate
import os

st.set_page_config(page_title="Cyfrowa Konsultacja Fryzjerska AI", page_icon="✂️")

st.title("✂️ Wirtualna Metamorfoza Fryzjerska AI")
st.write("Witaj! Prześlij swoje zdjęcie i odpowiedz na pytania, aby sztuczna inteligencja wygenerowała Twoją nową fryzurę!")

# --- BAZA WZORCÓW I INSPIRACJI DLA AI ---
BAZA_STYLE = [
    {
        "nazwa": "Klasyczny Bob z prostą linią",
        "tekstura": "Proste",
        "prompt_ai": "straight sleek bob haircut, short hair, natural hairline, realistic hair texture, professional salon styling",
        "zdjecie_referencyjne": "bob.jpg"
    },
    {
        "nazwa": "Soft Waves - Miękkie Fale",
        "tekstura": "Lekko się falują / wywijają",
        "prompt_ai": "medium length wavy hair, soft beach waves haircut, volume at roots, natural hair flow",
        "zdjecie_referencyjne": "waves.jpg"
    },
    {
        "nazwa": "Curly Shag / Zdefiniowany Skręt",
        "tekstura": "Kręcone / mocny skręt",
        "prompt_ai": "short curly shag haircut, defined natural curls, volumetric curly hair, layered curls",
        "zdjecie_referencyjne": "pixie.jpg"
    }
]

# Formularz
with st.form("konsultacja_form"):
    st.subheader("1. Tekstura i oczekiwania")
    tekstura = st.radio(
        "Jaka jest Twoja naturalna struktura włosów?",
        ["Proste", "Lekko się falują / wywijają", "Kręcone / mocny skręt"]
    )
    
    cel_skretu = st.radio(
        "Preferujesz fryzurę zgodną z Twoim skrętem?",
        [
            "Tak, chcę fryzurę dopasowaną do mojego skrętu",
            "Chcę zobaczyć wygładzoną / wyprostowaną wersję"
        ]
    )

    st.subheader("2. Twoje zdjęcie twarzy")
    st.write("Wgraj wyraźne zdjęcie twarzy z dobrze widoczną linią włosów:")
    uploaded_file = st.file_uploader("Wybierz zdjęcie z telefonu lub komputera", type=["jpg", "jpeg", "png"])

    st.subheader("3. Kontakt")
    kontakt = st.text_input("Podaj numer telefonu lub Instagram:")

    submitted = st.form_submit_button("🎨 Wygeneruj moją metamorfozę AI")

# GENEROWANIE PRZEZ AI
if submitted:
    if uploaded_file is None:
        st.error("Proszę najpierw wgrać zdjęcie twarzy!")
    else:
        st.divider()
        st.header("✨ Twój Wynik Metamorfozy AI")
        
        col_orig, col_ai = st.columns(2)
        with col_orig:
            st.image(uploaded_file, caption="Twoje obecne zdjęcie", use_container_width=True)
            
        # Wybór odpowiedniego stylu z bazy na podstawie filtra
        wybrana_fryzura = BAZA_STYLE[0] # Domyślna
        for style in BAZA_STYLE:
            if style["tekstura"] == tekstura:
                wybrana_fryzura = style
                break

        with col_ai:
            with st.spinner("AI analizuje Twoją twarz i nakłada nową fryzurę... To może zająć około 15-30 sekund."):
                try:
                    # Pobranie tokenu API ze Streamlit Secrets
                    api_token = st.secrets.get("REPLICATE_API_TOKEN") or os.environ.get("REPLICATE_API_TOKEN")
                    
                    if not api_token:
                        st.error("Brak skonfigurowanego klucza REPLICATE_API_TOKEN w Secrets Streamlit.")
                    else:
                        # Wywołanie generowania
                        output = replicate.run(
                            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                            input={
                                "image": uploaded_file,
                                "prompt": f"photo of the person in the image with {wybrana_fryzura['prompt_ai']}, same face, realistic salon lighting, 8k quality",
                                "negative_prompt": "long hair, curly if straight selected, distorted face, extra limbs, unrealistic texture",
                                "prompt_strength": 0.65
                            }
                        )
                        
                        if output:
                            st.image(output[0], caption=f"Rekomendacja: {wybrana_fryzura['nazwa']}", use_container_width=True)
                            st.success("Gotowe! Oto jak możesz wyglądać w nowej odsłonie.")
                        else:
                            st.warning("Nie udało się wygenerować obrazu. Spróbuj ponownie.")

                except Exception as e:
                    st.error(f"Wystąpił błąd podczas generowania AI: {str(e)}")
