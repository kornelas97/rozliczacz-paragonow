import os
import streamlit as st
from openai import OpenAI

# Tytuł aplikacji
st.title("Rozliczacz Paragonów (Wersja Darmowa - OpenRouter)")

# Pole na klucz API do OpenRouter
api_key = st.text_input("Wpisz swój klucz API OpenRouter", type="password")

# Pole do wgrania zdjęcia paragonu
uploaded_file = st.file_uploader(
    "Wgraj zdjęcie paragonu", type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
  # Wyświetlenie wgranego zdjęcia
  st.image(uploaded_file, caption="Wgrany paragon", use_column_width=True)

  if st.button("Rozlicz paragon"):
    if not api_key:
      st.error("Najpierw wpisz klucz API OpenRouter!")
    else:
      with st.spinner("Analizuję paragon za pomocą darmowego AI..."):
        try:
          # Inicjalizacja klienta OpenAI ze skierowaniem na OpenRouter
          client = OpenAI(
              base_url="https://openrouter.ai/api/v1", api_key=api_key
          )

          # Odczytanie bytes pliku graficznego
          image_bytes = uploaded_file.getvalue()
          import base64

          base64_image = base64.b64encode(image_bytes).decode("utf-8")

          # Wywołanie darmowego modelu wizyjnego przez OpenRouter
          response = client.chat.completions.create(
              model="google/gemini-2.0-flash-lite-preview:free",  # Darmowy model wizyjny
              messages=[
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "text",
                              "text": (
                                  "Przeanalizuj ten paragon, wypisz pozycje"
                                  " wraz z cenami i pomóż je rozliczyć."
                              ),
                          },
                          {
                              "type": "image_url",
                              "image_url": {
                                  "url": f"data:image/jpeg;base64,{base64_image}"
                              },
                          },
                      ],
                  }
              ],
          )

          # Wyświetlenie wyniku
          st.success("Gotowe!")
          st.write(response.choices[0].message.content)

        except Exception as e:
          st.error(st.error(f"Wystąpił błąd: {e}"))
