from PIL import Image
import google.generativeai as genai
import streamlit as st

# Tytuł aplikacji
st.title("Rozliczacz Paragonów (Kornel & Klaudia)")

# Automatyczne pobranie klucza z sekretów Streamlita
api_key = st.secrets["GEMINI_API_KEY"]

# Inicjalizacja historii konwersacji w pamięci podręcznej (st.session_state)
if "chat" not in st.session_state:
  st.session_state.chat = None
if "result" not in st.session_state:
  st.session_state.result = None

# Pole do wgrania wielu zdjęć paragonu naraz
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
  for index, file in enumerate(uploaded_files):
    img = Image.open(file)
    images.append(img)
    st.image(
        img, caption=f"Część paragonu #{index + 1}", use_column_width=True
    )

  if st.button("Rozlicz paragon"):
    with st.spinner("Analizuję paragon i dzielę zakupy..."):
      try:
        genai.configure(api_key=api_key)

        # Uruchamiamy model w trybie czatu, żeby mógł pamiętać poprzednie odpowiedzi
        model = genai.GenerativeModel("gemini-3.8-flash")
        st.session_state.chat = model.start_chat(history=[])

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

        if custom_rules.strip():
          prompt += (
              "BARDZO WAŻNE - Uwzględnij poniższe dodatkowe zasady i wyjątki"
              f" podane przez użytkownika:\n{custom_rules}\n\n"
          )

        prompt += (
            "Na koniec podaj podsumowanie kosztów dla Kornela i Klaudii"
            " (uwzględniając połowę kosztów wspólnych)."
        )

        # Wyślij zdjęcia i prompt w konwersacji
        content_to_send = images + [prompt]
        response = st.session_state.chat.send_message(content_to_send)
        st.session_state.result = response.text

      except Exception as e:
        st.error(f"Wystąpił błąd: {e}")

# Wyświetlanie wyniku i pole do poprawek
if st.session_state.result:
  st.success("Gotowe! Oto podział:")
  st.markdown(st.session_state.result)

  st.divider()
  st.subheader("✏️ Coś się nie zgadza? Popraw rozliczenie")

  correction = st.text_input(
      "Wpisz uwagę do powyższego rozliczenia:",
      placeholder=(
          "Np. Przenieś ser w plastrach do Klaudii, a kawa miała być pół na"
          " pół."
      ),
  )

  if st.button("Zastosuj poprawkę"):
    if correction.strip():
      with st.spinner("Aktualizuję podział..."):
        try:
          # Przesyłamy samą uwagę do otwartej konwersacji
          response = st.session_state.chat.send_message(
              f"Wprowadź następującą poprawkę do poprzedniego rozliczenia:"
              f" {correction}. Przedstaw od nowa pełny, zaktualizowany podział"
              " i podsumowanie kosztów."
          )
          st.session_state.result = response.text
          st.rerun()  # Odświeżenie widoku z nowym wynikiem
        except Exception as e:
          st.error(f"Wystąpił błąd podczas poprawiania: {e}")
