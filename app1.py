from PIL import Image
import google.generativeai as genai
import streamlit as st

# Tytuł aplikacji
st.title("Rozliczacz Paragonów (Kornel & Klaudia)")

# Automatyczne pobranie klucza z sekretów Streamlita
api_key = st.secrets["GEMINI_API_KEY"]

# Pole do wgrania wielu zdjęć paragonu naraz (np. długa część 1 i część 2)
uploaded_files = st.file_uploader(
    "Wgraj zdjęcie / zdjęcia paragonu",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

# Pola na własne, bieżące instrukcje i wyjątki
custom_rules = st.text_area(
    "Dodatkowe zasady / wyjątki do tego paragonu (opcjonalnie)",
    placeholder=(
        "Np. Woda mineralna jest zawsze dla Klaudii. Sos czosnkowy jest"
        " wspólny."
    ),
)

if uploaded_files:
  images = []
  # Wyświetlenie wszystkich wgranych zdjęć
  for index, file in enumerate(uploaded_files):
    img = Image.open(file)
    images.append(img)
    st.image(
        img, caption=f"Część paragonu #{index + 1}", use_column_width=True
    )

  if st.button("Rozlicz paragon"):
    with st.spinner("Analizuję paragon i dzielę zakupy..."):
      try:
        # Konfiguracja klucza Google AI
        genai.configure(api_key=api_key)

        # Użycie modelu Gemini
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Bazowa instrukcja z Twoimi nowymi wytycznymi
        prompt = (
            "Przeanalizuj przesłane zdjęcia paragonu (może to być jeden długi"
            " paragon podzielony na kilka zdjęć/zrzutów ekranu) i połącz je w"
            " jedną całość.\n\nPodziel pozycje na kategorie:\n1. **Kornel**"
            " (mniej zdrowe rzeczy, np. chipsy, cola, energetyki, frytki,"
            " boczek, ketchup, majonez, sosy, ser cheddar, chleb tostowy, lody,"
            " barszcz, bułki, słodycze, żelki, gumy maoam, ser w plastrach itp.)\n2."
            " **Klaudia** (zdrowe rzeczy i osobiste, np. rzeczy do okularów,"
            " warzywa, owoce, mrożonki, nabiał, jogurty, mięso, ryby, jajka, kawa"
            " itp.)\n3. **Wspólne** (chemia domowa, płyn do naczyń, płyn do"
            " prania, pasta do zębów, papier toaletowy itp.)\n4. **Do ustalenia /"
            " Niejasne pozycje** (tutaj wypisz wszystkie produkty z paragonu, co"
            " do których masz wątpliwości, do jakiej kategorii je przypisać"
            " albo których nazwy na paragonie są nieczytelne lub"
            " zagadkowe).\n\n"
        )

        # Jeśli wpisano własne uwagi, doklejamy je do zapytania ze szczególnym priorytetem
        if custom_rules.strip():
          prompt += (
              "BARDZO WAŻNE - Uwzględnij poniższe dodatkowe zasady i wyjątki"
              f" podane przez użytkownika:\n{custom_rules}\n\n"
          )

        prompt += (
            "Na koniec podaj podsumowanie kosztów dla Kornela i Klaudii"
            " (uwzględniając połowę kosztów wspólnych)."
        )

        # Przekazujemy wszystkie zdjęcia i prompt do Gemini
        content_to_send = images + [prompt]
        response = model.generate_content(content_to_send)

        # Wyświetlenie wyniku
        st.success("Gotowe! Oto podział:")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"Wystąpił błąd: {e}")
