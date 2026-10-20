from PIL import Image
import google.generativeai as genai
import streamlit as st

# Tytuł aplikacji
st.title("Rozliczacz Paragonów (Google Gemini - Darmowe)")

# Pole na klucz API z Google AI Studio
api_key = st.text_input("Wpisz swój klucz API z Google AI Studio", type="password")

# Pole do wgrania zdjęcia paragonu
uploaded_file = st.file_uploader(
    "Wgraj zdjęcie paragonu", type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
  # Wyświetlenie wgranego zdjęcia
  image = Image.open(uploaded_file)
  st.image(image, caption="Wgrany paragon", use_column_width=True)

  if st.button("Rozlicz paragon"):
    if not api_key:
      st.error("Najpierw wpisz klucz API!")
    else:
      with st.spinner("Analizuję paragon za pomocą Gemini..."):
        try:
          # Konfiguracja klucza Google AI
          genai.configure(api_key=api_key)

          # Użycie najnowszego, stabilnego modelu Gemini
          model = genai.GenerativeModel("gemini-2.5-flash")

          # Wygenerowanie odpowiedzi ze zdjęciem
          response = model.generate_content([
              image,
              (
                  "Przeanalizuj ten paragon, wypisz pozycje wraz z cenami i"
                  " pomóż je rozliczyć między osobami."
              ),
          ])

          # Wyświetlenie wyniku
          st.success("Gotowe!")
          st.write(response.text)

        except Exception as e:
          st.error(f"Wystąpił błąd: {e}")
