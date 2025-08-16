import streamlit as st # for ui application
import requests

API_URL = "http://127.0.0.1:8000/fetch-insights"  # string constant (a variable) that stores the URL of your API endpoint.

st.set_page_config(page_title="Shopify Insights Fetcher", layout="wide")

st.title("🛍️ Shopify Store Insights Fetcher")
st.write("Enter a Shopify store URL to fetch structured brand insights.")

# creating an input log for website url
website_url = st.text_input("Shopify Store URL", placeholder="https://examplebrand.myshopify.com")

# fetching button for data extraction
if st.button("Fetch Insights"):
    if not website_url:
        st.warning("⚠️ Please enter a valid Shopify store URL")
    else:
        with st.spinner("Fetching insights..."):
            try:
                response = requests.get(API_URL, params={"website_url": website_url}, timeout=30) # providing a time out after time is extended
                if response.status_code == 200:
                    data = response.json()

                    st.success(f"✅ Insights fetched for: {data.get('brand_name', 'Unknown Brand')}") # getting the data response from json

                    # Brand Info 
                    st.subheader("ℹ️ Brand Info")
                    st.write(data.get("about", "No About info available."))  # writing a brand info form json

                    #  Hero Products 
                    st.subheader("Home page Products")
                    for p in data.get("hero_products", []):
                        with st.expander(p["title"] if p["title"] else "Unnamed Product"):
                            st.write(p)

                    # Full Product Catalog 
                    st.subheader("📦 Product Catalog")
                    for p in data.get("products", []):
                        st.markdown(f"- **{p['title']}** → [View]({p['url']}) | Price: {p['price']}") # providing the products url and price tag

                    #  Policies 
                    st.subheader("📜 Policies")
                    st.write("**Privacy Policy:**")
                    st.text_area("Privacy Policy", value=data.get("privacy_policy") or "Not Found", height=500) # viewing the data policy in an scroll log
                    st.write("**Return/Refund Policy:**")
                    st.text_area("Return/Refund Policy", value=data.get("return_refund_policy") or "Not Found", height=500)

                    # FAQs 
                    st.subheader("❓ FAQs")
                    faqs = data.get("faqs", [])
                    if faqs:
                        for faq in faqs:
                            st.markdown(f"**Q:** {faq['question']}\n\n*A:* {faq['answer']}\n") # provide faqs if not print no faqs
                    else:
                        st.write("No FAQs found.")

                    # Socials
                    st.subheader("📱 Social Media")
                    socials = data.get("social_handles", [])  # adding the social media handles from json
                    if socials:
                        for s in socials:
                            st.markdown(f"- {s}")
                    else:
                        st.write("No social media links found.")

                    # Contact
                    st.subheader("📞 Contact Details")
                    contacts = data.get("contact_details", [])  # providing the contacts 
                    if contacts:
                        for c in contacts:
                            st.markdown(f"- {c}")
                    else:
                        st.write("No contacts found.")

                    # Important Links
                    st.subheader("🔗 Important Links")
                    links = data.get("important_links", [])
                    if links:
                        for l in links:
                            st.markdown(f"- {l}")
                    else:
                        st.write("No important links found.")

                elif response.status_code == 401:
                    st.error("❌ Website not found or inaccessible.") # if the status is 401 print website not found
                else:
                    st.error(f"⚠️ Error {response.status_code}: {response.text}")    # return a error with the response code and text

            except Exception as e:
                st.error(f"⚠️ Internal Error: {str(e)}")   # rise an exception on internal error
