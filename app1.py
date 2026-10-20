import streamlit as st
from openai import OpenAI
import base64

st.title("🧾 Rozliczacz Paragonów")

api_key = st.text_input("Klucz OpenAI API", type="password")
uploaded_file = st.file_uploader("Wgraj zdjęcie paragonu", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    st.image(uploaded_file, caption="Wgrany paragon", use_container_width=True)
    
    if st.button("Rozlicz paragon"):
        with st.spinner("Analizowanie..."):
            client = OpenAI(api_key=api_key)
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            
            prompt_instrukcja = """
            Jesteś asystentem do rozliczania paragonów między parą.
            Zasady:
            - Produkty Twoje: energetyki, białko, słodycze.
            - Produkty Jej: kosmetyki, produkty owsiane.
            - Reszta: Wspólne (dzielone 50/50).
            Przeanalizuj paragon, przypisz produkty, wylicz ile dziewczyna musi Ci oddać.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_instrukcja},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Rozlicz ten paragon:"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            
            st.markdown("### Wynik rozliczenia:")
            st.write(response.choices[0].message.content)
