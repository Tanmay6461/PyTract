import streamlit as st
import requests
import pandas as pd

def fetch_markdown_content(markdown_url: str) -> str:
    """Helper function to fetch markdown content from an S3 URL."""
    try:
        response = requests.get(markdown_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Failed to fetch markdown from S3: {e}")
        return ""

def main():
    st.title("Web Scraper Frontend")

    # Select the scraping engine
    engine = st.selectbox("Select Scraping Engine", ("BeautifulSoup", "FireCrawl", "Opensource", "Docling"))

    # Initialize variables based on the selected engine
    if engine in ["BeautifulSoup", "FireCrawl"]:
        url_input = st.text_input("Enter URL to scrape")
    elif engine in ["Opensource","Docling"]:
        uploaded_file = st.file_uploader("Choose a file")

    # Scrape button to trigger scraping
    if st.button("Scrape"):
        if engine in ["BeautifulSoup", "FireCrawl"]:
            # For BeautifulSoup and FireCrawl, ensure URL is provided
            if not url_input:
                st.warning("Please enter a valid URL.")
            else:
                try:
                    scrape_api_url = "http://localhost:8000/scrape"  # Your scraper API URL
                    payload = {"url": url_input}
                    response = requests.post(scrape_api_url, json=payload)
                    response.raise_for_status()
                    result = response.json()

                    markdown_url = result.get("markdown_url")
                    if markdown_url:
                        # Fetch and display the markdown content
                        markdown_content = fetch_markdown_content(markdown_url)
                        if markdown_content:
                            st.markdown(markdown_content)
                    else:
                        st.error("No markdown_url returned from the API.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Request to backend failed: {e}")

        elif engine == "Opensource":
            # For Opensource, ensure a file is uploaded
            if not uploaded_file:
                st.warning("Please upload a valid file.")
            else:
                api_url = "http://127.0.0.1:8000/pdfToMd-text/"  # Your API URL for Opensource
                try:
                    response = requests.post(api_url, files={"file": uploaded_file})
                    response.raise_for_status()

                    # Parse the response JSON
                    response_data = response.json()
                    md_link = response_data.get("presigned_url")
                    images_link = response_data.get("image_urls")
                    tables_urls = response_data.get("table_url")

                    # Fetch and display markdown
                    if md_link:
                        markdown_response = requests.get(md_link)
                        if markdown_response.status_code == 200:
                            st.markdown(markdown_response.text, unsafe_allow_html=True)
                        else:
                            st.error("Error fetching markdown content from S3.")

                    # Display images if available
                    if images_link:
                        for img in images_link:
                            st.image(img)

                    # Display tables if available
                    if tables_urls:
                        for table in tables_urls:
                            table_response = requests.get(table)
                            if table_response.status_code == 200:
                                df = pd.read_csv(table)
                                st.dataframe(df)
                            else:
                                st.error(f"Failed to load table from {table}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error occurred: {e}")
        elif engine == "Docling":
            if not uploaded_file:
                st.warning("Please upload a valid file.")
            else:
                api_url = f"http://127.0.0.1:8000/pdfToMd_docling/"
                try:
                    response = requests.post(api_url,files={"file":uploaded_file})
                    if response.status_code == 200 :
                        markdown_response = response.text
                        if markdown_response:
                                st.markdown(markdown_response,unsafe_allow_html=True)
                        else :
                                st.error(f"Failed to process {requests.status_codes}")
                except requests.exceptions.RequestException as e :
                    st.error("Error occured")
        elif engine == "FireCrawl":
            # Placeholder for FireCrawl engine
            st.info("FireCrawl functionality will be implemented later.")

if __name__ == "__main__":
    main()
