import streamlit as st
from datetime import datetime

INDEKSLER = {
    2006: 1.083, 2007: 1.167, 2008: 1.208, 2009: 1.015,
    2010: 1.057, 2011: 1.079, 2012: 1.011, 2013: 1.024,
    2014: 1.014, 2015: 1.040, 2016: 1.124, 2017: 1.057,
    2018: 1.029, 2019: 1.166, 2020: 1.026, 2021: 1.028,
    2022: 1.067, 2023: 1.139, 2024: 1.088, 2025: 1.022,
    2026: 1.056
}
ILLIK_INDEKS_2026 = 1.093
BOLEN = 144
STAJ_BAZA_MEBLEG = 306

st.sidebar.title("Menyu")
secim = st.sidebar.radio("Seçin:", ["İrəli Hesablama", "Tərsinə Hesablama", "Haqqında", "Təlimat"])

if secim == "İrəli Hesablama":
    st.header("İrəli Hesablama")
    il = st.number_input("Staj (il)", 0.0)
    ay = st.number_input("Staj (ay)", 0.0)
    gun = st.number_input("Staj (gün)", 0.0)
    kapital = st.number_input("Kapital (AZN)", 0.0)
    dogum = st.text_input("Doğum tarixi (gg.aa.iiii)")

    if st.button("Hesabla"):
        try:
            dogum_dt = datetime.strptime(dogum, "%d.%m.%Y")
            pensiya_il = dogum_dt.year + 65
            staj_il_cemi = il + ay/12 + gun/365
            baza_2006 = (staj_il_cemi * STAJ_BAZA_MEBLEG) / BOLEN

            indeks_limit = min(pensiya_il, 2026)
            indeks_deyer = baza_2006
            for il_key in sorted(INDEKSLER.keys()):
                if il_key > indeks_limit:
                    break
                indeks_deyer *= INDEKSLER[il_key]

            kapital_ayliq = kapital / BOLEN
            esas_pensiya = indeks_deyer + kapital_ayliq

            if pensiya_il < 2026:
                yekun_2026 = esas_pensiya * ILLIK_INDEKS_2026
                indeks_text = f"2026 indeksləşməsi (9.3%): {yekun_2026:.2f} AZN"
            else:
                indeks_text = "2026 indeksləşməsi tətbiq olunmur."

            st.success(
                f"Doğum ili: {dogum_dt.year}\n"
                f"Pensiya ili: {pensiya_il}\n"
                f"2006-ya qədər staj: {staj_il_cemi:.2f} il\n\n"
                f"Staj dəyəri: {indeks_deyer:.2f} AZN\n"
                f"Kapital aylıq: {kapital_ayliq:.2f} AZN\n"
                f"Əsas pensiya: {esas_pensiya:.2f} AZN\n\n"
                f"{indeks_text}"
            )
        except Exception as e:
            st.error(f"Xəta: {e}")

elif secim == "Tərsinə Hesablama":
    st.header("Tərsinə Hesablama")
    pensiya = st.number_input("Hazır pensiya (AZN)", 0.0)
    kapital = st.number_input("Kapital (AZN)", 0.0)
    dogum = st.text_input("Doğum tarixi (gg.aa.iiii)")
    nine = st.checkbox("2026 üçün 9.3% tətbiq olunub")

    if st.button("Tərs Hesabla"):
        try:
            dogum_dt = datetime.strptime(dogum, "%d.%m.%Y")
            pensiya_il = dogum_dt.year + 65
            esas_pensiya = pensiya / ILLIK_INDEKS_2026 if nine else pensiya
            kapital_ayliq = kapital / BOLEN
            staj_deyeri = esas_pensiya - kapital_ayliq

            indeks_limit = min(pensiya_il, 2026)
            hasil = 1
            for il_key in sorted(INDEKSLER.keys()):
                if il_key > indeks_limit:
                    break
                hasil *= INDEKSLER[il_key]

            baza_2006 = staj_deyeri / hasil
            staj_il = baza_2006 * BOLEN / STAJ_BAZA_MEBLEG

            st.success(
                f"Doğum ili: {dogum_dt.year}\n"
                f"Pensiya ili: {pensiya_il}\n\n"
                f"Əsas pensiya: {esas_pensiya:.2f} AZN\n"
                f"Kapital aylıq: {kapital_ayliq:.2f} AZN\n"
                f"Staj dəyəri: {staj_deyeri:.2f} AZN\n\n"
                f"2006 baza: {baza_2006:.2f} AZN\n"
                f"2006-ya qədər staj: {staj_il:.2f} il"
            )
        except Exception as e:
            st.error(f"Xəta: {e}")

elif secim == "Haqqında":
    st.header("Haqqında")
    st.info("Pensiya Hesablama Sistemi\nVersiya: 1.0 (2026)\nHazırlayan: Akif Çərkəzoğlu\nWhatsApp: +7 985 444 07 37")

elif secim == "Təlimat":
    st.header("Təlimat")
    st.write("""
    Bu proqram pensiya hesablamalarını aparmaq üçün nəzərdə tutulub.

    **İrəli Hesablama:**
    - 2006-ya qədər stajı (il, ay, gün) daxil edin
    - Kapital məbləğini yazın
    - Doğum tarixini gg.aa.iiii formatında daxil edin
    - 'Hesabla' düyməsinə basın

    **Tərsinə Hesablama:**
    - Hazır pensiya məbləğini daxil edin
    - Kapitalı yazın
    - Doğum tarixini daxil edin
    - Əgər 2026 indeksləşməsi tətbiq olunubsa, işarələyin
    - 'Tərs Hesabla' düyməsinə basın
    """)
