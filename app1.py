from PIL import Image
import google.generativeai as genai
import streamlit as st

# Tytuł aplikacji
st.title("Rozliczacz Paragonów (Kornel & Klaudia)")

# Automatyczne pobranie klucza z sekretów chmury Streamlit Cloud
api_key = st.secrets["GEMINI_API_KEY"]

# Pole do wgrania zdjęcia paragonu
uploaded_file = st.file_uploader(
    "Wgraj zdjęcie paragonu", type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
  # Załadowanie i wyświetlenie wgranego zdjęcia
  image = Image.open(uploaded_file)
  st.image(image, caption="Wgrany paragon", use_column_width=True)

  if st.button("Rozlicz paragon"):
    with st.spinner("Analizuję paragon i dzielę zakupy..."):
      try:
        # Konfiguracja klucza Google AI
        genai.configure(api_key=api_key)

        # Użycie modelu Gemini
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Instrukcja z podziałem na Wasze kategorie
        prompt = (
            "Przeanalizuj ten paragon i podziel pozycje na kategorie:\n1."
            " **Kornel** (mniej zdrowe rzeczy, np. chipsy, cola, energetyki,"
            " frytki, boczek, ketchup, majonez, sosy, ser cheddar, chleb"
            " tostowy, lody, barszcz, bułki, słodycze itp.)\n2. **Klaudia**"
            " (zdrowe rzeczy i osobiste, np. rzeczy do okularów, warzywa,"
            " owoce, mrożonki, nabiał, jogurty, mięso, ryby, jajka , kawa , herbaty , nici dentystyczne , mleko itp.)\n3."
            " **Wspólne** (chemia domowa, płyn do naczyń, płyn do prania, pasta"
            " do zębów, papier toaletowy itp.)\n4. **Do ustalenia / Niejasne"
            " pozycje** (tutaj wypisz wszystkie produkty z paragonu, co do"
            " których masz wątpliwości, do jakiej kategorii je przypisać"
            " albo których nazwy na paragonie są nieczytelne lub"
            " zagadkowe).\n\nNa koniec podaj podsumowanie kosztów dla"
            " Kornela i Klaudii (uwzględniając połowę kosztów wspólnych)."
        )

        # Wygenerowanie odpowiedzi ze zdjęciem
        response = model.generate_content([image, prompt])

        # Wyświetlenie wyniku
        st.success("Gotowe! Oto podział:")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"Wystąpił błąd: {e}")
