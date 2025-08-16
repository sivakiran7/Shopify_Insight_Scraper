import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/fetch-insights"  # FastAPI backend

st.set_page_config(page_title="Shopify Insights Fetcher", layout="wide")

st.title("🛍️ Shopify Store Insights Fetcher")
st.write("Enter a Shopify store URL to fetch structured brand insights.")

# Input box
website_url = st.text_input("Shopify Store URL", placeholder="https://examplebrand.myshopify.com")

if st.button("Fetch Insights"):
    if not website_url:
        st.warning("⚠️ Please enter a valid Shopify store URL")
    else:
        with st.spinner("Fetching insights..."):
            try:
                response = requests.get(API_URL, params={"website_url": website_url}, timeout=30)
                if response.status_code == 200:
                    data = response.json()

                    st.success(f"✅ Insights fetched for: {data.get('brand_name', 'Unknown Brand')}")

                    # --- Brand Info ---
                    st.subheader("ℹ️ Brand Info")
                    st.write(data.get("about", "No About info available."))

                    # --- Hero Products ---
                    st.subheader("Home page Products")
                    for p in data.get("hero_products", []):
                        with st.expander(p["title"] if p["title"] else "Unnamed Product"):
                            st.write(p)

                    # --- Full Product Catalog ---
                    st.subheader("📦 Product Catalog")
                    for p in data.get("products", []):
                        st.markdown(f"- **{p['title']}** → [View]({p['url']}) | Price: {p['price']}")

                    # --- Policies ---
                    st.subheader("📜 Policies")
                    st.write("**Privacy Policy:**")
                    st.text_area("Privacy Policy", value=data.get("privacy_policy") or "Not Found", height=500)
                    st.write("**Return/Refund Policy:**")
                    st.text_area("Return/Refund Policy", value=data.get("return_refund_policy") or "Not Found", height=500)

                    # --- FAQs ---
                    st.subheader("❓ FAQs")
                    faqs = data.get("faqs", [])
                    if faqs:
                        for faq in faqs:
                            st.markdown(f"**Q:** {faq['question']}\n\n*A:* {faq['answer']}\n")
                    else:
                        st.write("No FAQs found.")

                    # --- Socials ---
                    st.subheader("📱 Social Media")
                    socials = data.get("social_handles", [])
                    if socials:
                        for s in socials:
                            st.markdown(f"- {s}")
                    else:
                        st.write("No social media links found.")

                    # --- Contact ---
                    st.subheader("📞 Contact Details")
                    contacts = data.get("contact_details", [])
                    if contacts:
                        for c in contacts:
                            st.markdown(f"- {c}")
                    else:
                        st.write("No contacts found.")

                    # --- Important Links ---
                    st.subheader("🔗 Important Links")
                    links = data.get("important_links", [])
                    if links:
                        for l in links:
                            st.markdown(f"- {l}")
                    else:
                        st.write("No important links found.")

                elif response.status_code == 401:
                    st.error("❌ Website not found or inaccessible.")
                else:
                    st.error(f"⚠️ Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Internal Error: {str(e)}")
