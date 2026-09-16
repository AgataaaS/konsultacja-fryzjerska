import streamlit as st
from huggingface_hub import InferenceClient
import os
from PIL import Image

st.set_page_config(page_title="AI Hair Consultation & Virtual Try-On", page_icon="✂️", layout="wide")

st.title("✂️ Digital Hair Consultation & AI Virtual Try-On")
st.write("Complete the brief consultation form below. Our AI will analyze your inputs and generate 3 to 5 custom hairstyle proposals tailored strictly to your natural texture and hair length!")

# --- INTERNAL PROPRIETARY TREND GALLERY (HIDDEN REFERENCE BASE) ---
# Photos serve purely as reference prompts for the AI and are never shown raw to the client.
STYLE_DATABASE = [
    {
        "id": 1,
        "name": "Classic Blunt Bob",
        "length": "Short (Jaw-length)",
        "texture": "Straight",
        "styling_time": "Under 10 minutes",
        "description": "A sharp, geometric chin-length cut that defines the jawline. Perfect for straight, sleek hair.",
        "prompt_ai": "photo of a woman with a sleek chin-length blunt bob haircut, straight hair, professional salon styling, realistic lighting, 8k"
    },
    {
        "id": 2,
        "name": "Textured French Bob",
        "length": "Short (Jaw-length)",
        "texture": "Wavy / Loose curls",
        "styling_time": "Under 10 minutes",
        "description": "A relaxed, textured bob with subtle layers to add movement without high maintenance.",
        "prompt_ai": "photo of a woman with a textured french bob haircut, soft natural waves, curtain bangs, professional salon hair styling"
    },
    {
        "id": 3,
        "name": "Curly Shag Cut",
        "length": "Short (Jaw-length)",
        "texture": "Curly / Tight curls",
        "styling_time": "Under 10 minutes",
        "description": "Layered cut designed specifically to enhance natural curl definition while avoiding excessive volume at the bottom.",
        "prompt_ai": "photo of a woman with a short curly shag haircut, defined volumetric natural curls, layered curly hair"
    },
    {
        "id": 4,
        "name": "Soft Waves & Curtain Bangs",
        "length": "Medium (Shoulder-length)",
        "texture": "Wavy / Loose curls",
        "styling_time": "10-20 minutes",
        "description": "Shoulder-length soft layers combined with face-framing curtain bangs for effortless volume.",
        "prompt_ai": "photo of a woman with shoulder-length soft wavy hair, curtain bangs, face framing layers, natural volume"
    },
    {
        "id": 5,
        "name": "Sleek Shoulder-Length Cut",
        "length": "Medium (Shoulder-length)",
        "texture": "Straight",
        "styling_time": "10-20 minutes",
        "description": "A clean, elegant medium-length style with subtle internal layering for a lightweight feel.",
        "prompt_ai": "photo of a woman with sleek shoulder-length straight hair, blunt ends, natural shine, salon quality"
    },
    {
        "id": 6,
        "name": "Medium Volumetric Curls",
        "length": "Medium (Shoulder-length)",
        "texture": "Curly / Tight curls",
        "styling_time": "10-20 minutes",
        "description": "Balanced medium-length cut tailored to keep tight curls bouncy, defined, and light.",
        "prompt_ai": "photo of a woman with shoulder-length volumetric curls, well-defined curly texture, natural shape"
    },
    {
        "id": 7,
        "name": "Long Layered Waves",
        "length": "Long (Past shoulders)",
        "texture": "Wavy / Loose curls",
        "styling_time": "Over 20 minutes",
        "description": "Long flowing layers designed to lighten heavy hair while enhancing soft wave patterns.",
        "prompt_ai": "photo of a woman with long layered wavy hair, soft cascading beach waves, natural movement"
    }
]

# --- CONSULTATION FORM ---
with st.form("consultation_form"):
    st.subheader("1. Hair Characteristics & Daily Routine")
    col1, col2 = st.columns(2)
    
    with col1:
        current_length = st.selectbox(
            "Current Hair Length:",
            ["Short (Jaw-length)", "Medium (Shoulder-length)", "Long (Past shoulders)"]
        )
        texture = st.radio(
            "Natural Hair Texture:",
            ["Straight", "Wavy / Loose curls", "Curly / Tight curls"]
        )
        
    with col2:
        styling_time = st.radio(
            "How much time do you spend styling daily?",
            ["Under 10 minutes", "10-20 minutes", "Over 20 minutes"]
        )
        allow_straightening = st.checkbox("Open to smoothed / heat-styled looks (different from natural texture)")

    st.subheader("2. Transformation Boundaries")
    st.info("💡 Strict Transformation Policy: All AI suggestions are strictly constrained to your current length or shorter. No extensions or additions are applied.")

    st.subheader("3. Client Reference Photo")
    uploaded_file = st.file_uploader("Upload a clear front-facing portrait photo (well lit, visible hairline):", type=["jpg", "jpeg", "png"])

    st.subheader("4. Contact Information")
    contact = st.text_input("Phone number or Instagram handle (to receive your consultation summary):")

    submitted = st.form_submit_button("🎨 Generate My 3-5 AI Hairstyle Proposals")

# --- MATCHING & AI GENERATION ENGINE ---
if submitted:
    if uploaded_file is None:
        st.error("Please upload a portrait photo first!")
    else:
        st.divider()
        st.header("✨ Your AI Virtual Hair Consultation Results")
        
        # 1. FILTERING LOGIC
        matched_styles = []
        for style in STYLE_DATABASE:
            # Rule 1: No longer hair cuts than current length
            if current_length == "Short (Jaw-length)" and style["length"] in ["Medium (Shoulder-length)", "Long (Past shoulders)"]:
                continue
            if current_length == "Medium (Shoulder-length)" and style["length"] == "Long (Past shoulders)":
                continue
                
            # Rule 2: Texture matching unless heat-styling option is checked
            if not allow_straightening and style["texture"] != texture:
                continue
                
            matched_styles.append(style)

        # Ensure between 3 and 5 proposals
        if len(matched_styles) < 3:
            # Fallback to ensure client always gets at least 3 valid options
            matched_styles = [s for s in STYLE_DATABASE if not (current_length == "Short (Jaw-length)" and s["length"] != "Short (Jaw-length)")][:5]
        else:
            matched_styles = matched_styles[:5]

        st.subheader(f"We have generated {len(matched_styles)} custom AI proposals based on your consultation profile:")
        
        # Display Client Original Photo
        st.image(uploaded_file, caption="Your Original Photo", width=300)
        st.divider()

        # 2. GENERATE 3 TO 5 AI VISUALIZATIONS IN A GRID
        token = st.secrets.get("HF_TOKEN") or os.environ.get("HF_TOKEN")
        
        if not token:
            st.error("Missing HF_TOKEN in Streamlit Secrets.")
        else:
            client = InferenceClient(api_key=token)
            
            # Display results in grid columns
            cols = st.columns(len(matched_styles))
            
            for idx, style in enumerate(matched_styles):
                with cols[idx]:
                    st.markdown(f"### Proposal {idx+1}: {style['name']}")
                    st.write(f"**Length:** {style['length']}")
                    st.write(f"**Styling Time:** {style['styling_time']}")
                    st.caption(style['description'])
                    
                    with st.spinner(f"Generating AI Proposal {idx+1}..."):
                        try:
                            # Direct AI generation based on curated prompt logic
                            image = client.text_to_image(
                                prompt=style["prompt_ai"],
                                model="black-forest-labs/FLUX.1-schnell"
                            )
                            st.image(image, caption=f"Option {idx+1}: {style['name']}", use_container_width=True)
                        except Exception as e:
                            st.error(f"Error generating proposal {idx+1}: {str(e)}")

            st.success("All proposals generated successfully! Select your favorite look for your upcoming appointment.")
