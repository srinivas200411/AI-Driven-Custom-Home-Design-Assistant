import streamlit as st
import google.generativeai as genai
import requests  # Importing requests to fetch images
import os  # For environment variables

# Configure the API key for the Gemini API
api_key = "AIzaSyCteWjKt80SY1yL0aZv7zQTMWJhE6y5JHI"
genai.configure(api_key=api_key)

# Pexels API Key (Replace with your own key from https://www.pexels.com/api/)
PEXELS_API_KEY = "P8w5PqSGzmM8dHr6D2ns0ldFBfUfp08pcoLDHyRllPecey7IqeyxtqNq"

# Configure the model generative settings
generative_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Function to generate home design ideas using Google generative AI API
def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generative_config,
    )
    
    context = f'Create a custom home design plan with the following details:\nStyle: {style}\nSize: {size}\nRooms: {rooms}'
    
    response = model.generate_content(context)
    
    # Print response for debugging
    print(response)
    
    if response.candidates:
        candidate = response.candidates[0]
        design_text = getattr(candidate, "content", "AI response format changed. Please check API documentation.")
    else:
        design_text = "No candidates found in the response."
    
    return design_text

# Function to fetch two images from Pexels based on the design style
def fetch_images_from_pexels(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=2"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "photos" in data and len(data["photos"]) >= 2:
            return [data["photos"][0]["src"]["large"], data["photos"][1]["src"]["large"]]  # Return two image URLs
        elif "photos" in data and len(data["photos"]) == 1:
            return [data["photos"][0]["src"]["large"]]  # Return only one if available
        else:
            return []
    except Exception as e:
        print("Error fetching images from Pexels:", str(e))
        return []

# Streamlit UI for taking user inputs
st.title("🏠 Custom Home Design Assistant")

# Textboxes for style, size, and number of rooms input
style = st.text_input("🎨 Enter the home design style (e.g., Modern, Rustic)")
size = st.text_input("📏 Enter the size of the home (e.g., 2000 sq ft)")
rooms = st.text_input("🛏️ Enter the number of rooms")

# Submit button
if st.button("🔍 Generate Design"):
    if style and size and rooms:
        design_idea = generate_design_idea(style, size, rooms)
        image_urls = fetch_images_from_pexels(f"{style} home design")
        
        st.markdown("### 🏡 Custom Home Design Idea")
        st.markdown(design_idea)
        
        if image_urls:
            for img_url in image_urls:
                st.image(img_url, caption="Design inspiration from Pexels")
        else:
            st.warning("No relevant images found on Pexels.")
    else:
        st.warning("Please fill in all the fields.")
