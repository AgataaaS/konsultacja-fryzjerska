Python
import streamlit as st

st.set_page_config(page_title="Cyfrowa Konsultacja Fryzjerska", page_icon="✂️")

st.title("✂️ Wirtualna Konsultacja Fryzjerska")
st.write("Witaj! Odpowiedz na kilka pytań i prześlij zdjęcie swoich włosów, abyśmy mogły dobrać idealną fryzurę i plan pielęgnacyjny.")

# Formularz konsultacyjny
with st.form("konsultacja_form"):
    
    st.subheader("1. Zmiana i stylizacja")
    poziom_zmiany = st.radio(
        "Jakiej zmiany dzisiaj potrzebujesz?",
        ["Duża zmiana (całkowita metamorfoza)", "Umiarkowana zmiana (odświeżenie stylu)", "Mała zmiana (podcięcie / lekka korekta)"]
    )
    
    st.subheader("2. Tekstura, objętość i ciężar włosów")
    tekstura = st.radio(
        "Jaka jest naturalna struktura Twoich włosów?",
        ["Proste", "Lekko się falują / wywijają", "Kręcone / mocny skręt"]
    )
    
    cel_skretu = st.radio(
        "Co chciałabyś osiągnąć z teksturą włosów?",
        [
            "Chcę wydobyć i podkreślić skręt / fale (więcej objętości i skrętu)",
            "Chcę je wygładzić / wyprostować (ułatwić stylizację na gładko)",
            "Podoba mi się obecny stan, chcę tylko dobrego cięcia"
        ]
    )

    objetosc = st.radio(
        "Jak oceniasz obecną objętość i ciężar swoich włosów?",
        [
            "Jestem zadowolona z obecnej objętości",
            "Chciałabym mieć optycznie więcej objętości (włosy są przyklapnięte/cienkie)",
            "Chciałabym mieć mniej objętości / mam poczucie, że są za ciężkie i grube"
        ]
    )

    st.subheader("3. Koloryzacja")
    zmiana_koloru = st.radio(
        "Czy jesteś otwarta na zmianę koloru?",
        ["Tak", "Nie"]
    )
    
    gotowosc_retusz = "Nie dotyczy"
    if zmiana_koloru == "Tak":
        gotowosc_retusz = st.radio(
            "Czy jesteś gotowa na regularne wizyty w salonie co miesiąc (odrosty/tonowanie)?",
            ["Tak, mogę przychodzić co miesiąc", "Nie, wolę coś niewymagającego częstych wizyt"]
        )

    st.subheader("4. Twoje obecne zdjęcie")
    st.write("Wgraj zdjęcie obecnych włosów (najlepiej w naturalnym świetle):")
    uploaded_file = st.file_uploader("Wybierz zdjęcie z telefonu lub komputera", type=["jpg", "jpeg", "png"])

    st.subheader("5. Kontakt do Ciebie")
    kontakt = st.text_input("Podaj swój numer telefonu lub nazwę na Instagramie, żebym mogła wysłać Ci indywidualną ocenę wykonalności:")

    submitted = st.form_submit_button("Wyślij konsultację do fryzjera")

# Obsługa po wysłaniu formularza
if submitted:
    st.divider()
    st.header("📋 Twoja wstępna analiza i scenariusz")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Twoje wgrane zdjęcie", width=300)
        st.info("📸 Dziękujemy za przesłanie zdjęcia! Przeanalizuję porowatość, gęstość oraz długość Twoich włosów i skontaktuję się z Tobą podanym kontaktem.")
    
    # Rekomendacje dotyczące cięcia, objętości i tekstury
    st.subheader("💡 Wskazówki dotyczące cięcia i objętości:")
    
    # Analiza objętości
    if "więcej objętości" in objetosc:
        st.markdown("""
        * **Objętość & Lekkość:** Zaproponujemy cięcie unoszące włosy u nasady (np. odpowiednie warstwowanie / cieniowanie) oraz lekkie kosmetyki bezciężarowe, które nie obciążają pasm.
        """)
    elif "mniej objętości" in objetosc:
        st.markdown("""
        * **Redukcja ciężaru:** Wykonamy techniczne odciążenie/spersonalizowane teksturowanie od wewnątrz, aby włosy układały się lżej i nie tworzyły „efektu trójkąta”.
        """)
    else:
        st.markdown("""
        * **Objętość:** Zachowamy obecną proporcję i ciężar, skupiając się jedynie na nadaniu czystej formy i linii.
        """)

    # Analiza skrętu
    if "podkreślić" in cel_skretu:
        st.markdown("""
        * **Tekstura:** Cięcie dopasowane do naturalnego układy skrętu (często cięcie na sucho lub dedykowane włosom falowanym), połączenie z wgniataniem stylizatora na mokro.
        """)
    elif "wygładzić" in cel_skretu:
        st.markdown("""
        * **Tekstura:** Postawimy na zwarta linię cięcia i domykające łuskę zabiegi pielęgnacyjne ułatwiające wygładzanie na szczotce.
        """)

    # Rekomendacje koloryzacyjne
    st.subheader("🎨 Scenariusz koloryzacji:")
    if zmiana_koloru == "Tak" and "Tak, mogę" in gotowosc_retusz:
        st.success("🟢 **Plan:** Pełna zmiana tonalna / jasny blond z regularnym planem tonowania co 4 tygodnie.")
    elif zmiana_koloru == "Tak" and "Nie, wolę" in gotowosc_retusz:
        st.warning("🟡 **Plan:** Techniki z miękkim odrostem (*Soft Balayage / AirTouch*), które odrastają naturalnie bez konieczności częstych poprawek.")
    else:
        st.info("🔵 **Plan:** Focus na naturze i pielęgnacji połysku (np. zabieg glossingowy).")
