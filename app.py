
import streamlit as st
import random

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Closet",
    page_icon="👗",
    layout="wide"
)

# -----------------------------
# INITIALIZE SESSION DATA
# -----------------------------

if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = []


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("My Closet 👗")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "My Wardrobe", "Outfit Generator"]
)


# -----------------------------
# HOME PAGE
# -----------------------------

if page == "Home":

    st.title("Welcome to My Closet!")
    st.subheader("Your personal digital wardrobe.")

    st.write(
        "Organize your clothing and discover new outfit combinations."
    )

    st.divider()

    st.subheader("Today's Weather")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperature", "-- °C")

    with col2:
        st.metric("Conditions", "Not connected")

    with col3:
        st.metric("Location", "Not connected")

    st.info("Weather information will be connected later.")

    st.divider()

    st.subheader("Get Started")

    st.write("Upload clothing to your wardrobe or generate an outfit!")

    if st.button("Go to My Wardrobe"):
        st.session_state.page = "My Wardrobe"


# -----------------------------
# MY WARDROBE PAGE
# -----------------------------

elif page == "My Wardrobe":

    st.title("My Wardrobe")
    st.write("Upload and organize your clothing items.")

    st.divider()

    # Clothing upload section

    st.subheader("Add a Clothing Item")

    uploaded_file = st.file_uploader(
        "Upload an image of your clothing",
        type=["png", "jpg", "jpeg"]
    )

    category = st.selectbox(
        "Select clothing category",
        ["Top", "Bottom", "Shoes", "Outerwear", "Dress", "Accessory"]
    )

    if uploaded_file is not None:

        st.image(uploaded_file, width=200)

        if st.button("Add to Wardrobe"):

            clothing_item = {
                "name": uploaded_file.name,
                "category": category,
                "image": uploaded_file.getvalue()
            }

            st.session_state.wardrobe.append(clothing_item)

            st.success("Clothing item added!")

    st.divider()

    # Display wardrobe

    st.subheader("My Clothing Collection")

    filter_category = st.selectbox(
        "Filter by category",
        ["All", "Top", "Bottom", "Shoes",
         "Outerwear", "Dress", "Accessory"]
    )

    if len(st.session_state.wardrobe) == 0:

        st.info("Your wardrobe is empty. Upload your first item!")

    else:

        clothing_to_display = st.session_state.wardrobe

        if filter_category != "All":
            clothing_to_display = [
                item for item in clothing_to_display
                if item["category"] == filter_category
            ]

        cols = st.columns(3)

        for index, item in enumerate(clothing_to_display):

            with cols[index % 3]:

                st.image(item["image"], width=180)
                st.write(item["name"])
                st.caption(item["category"])


# -----------------------------
# OUTFIT GENERATOR PAGE
# -----------------------------

elif page == "Outfit Generator":

    st.title("Outfit Generator")

    st.write("Discover a new outfit using your wardrobe!")

    st.divider()

    st.subheader("Choose Your Preferences")

    style = st.selectbox(
        "What style are you going for?",
        ["Any", "Casual", "Formal", "Sporty", "Comfy"]
    )

    occasion = st.selectbox(
        "What is the occasion?",
        ["Everyday", "School", "Work", "Going Out"]
    )

    if st.button("Generate Outfit"):

        wardrobe = st.session_state.wardrobe

        tops = [
            item for item in wardrobe
            if item["category"] == "Top"
        ]

        bottoms = [
            item for item in wardrobe
            if item["category"] == "Bottom"
        ]

        if tops and bottoms:

            selected_top = random.choice(tops)
            selected_bottom = random.choice(bottoms)

            st.subheader("Your Outfit!")

            col1, col2 = st.columns(2)

            with col1:
                st.image(selected_top["image"], width=200)
                st.write(selected_top["name"])

            with col2:
                st.image(selected_bottom["image"], width=200)
                st.write(selected_bottom["name"])

            st.success("Outfit generated successfully!")

        else:

            st.warning(
                "Please add at least one top and one bottom "
                "to your wardrobe first."
            )

    st.caption("More outfit customization coming soon!")
