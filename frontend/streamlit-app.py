import streamlit as st
import requests
import pandas as pd 

st.title('Welcome to the App!')


document_type_selectBox = st.sidebar.selectbox(
    'Select document type',('PDF','WebUrl')
)

add_selectBox =  st.sidebar.selectbox(
    'Select tool for conversion',
    ('OpenSource', 'Enterprise', 'Docling')
)

uploaded_file = st.file_uploader("Choose a file ")

if document_type_selectBox == 'PDF' and add_selectBox == 'OpenSource' and uploaded_file is not None:
    api_url = f"https://fastapi-service-741843712518.us-central1.run.app/pdfToMd-text/"
   
    try:
        response = requests.post(api_url,files={"file":uploaded_file})
        if response.status_code == 200 :
           
            # md_link = response.
            response_data = response.json()
            md_link = response_data.get("presigned_url")
            images_link = response_data.get("image_urls")
            tables_urls = response_data.get("table_url")

            # getting data from s3 link
            markdown_response = requests.get(md_link)

            if md_link:
                if markdown_response.status_code == 200:
                    md_data = markdown_response.text
                    st.markdown(md_data,unsafe_allow_html=True)
                else :
                    st.error("error: markdown")
            if images_link:
                for img in images_link:
                    st.image(img)
            if tables_urls:
                for table in tables_urls:
                  table_response = requests.get(table)
                  print(table_response)
                  df= pd.read_csv(table)
                  st.dataframe(df)
            
        else :
            st.error(f"Failed to process {requests.status_codes}")
    except requests.exceptions.RequestException as e :
        st.error("Error occured")

elif document_type_selectBox == 'PDF' and add_selectBox == 'Docling' and uploaded_file is not None:
    api_url = f"http://127.0.0.1:8000/pdfToMd_docling/"
    try:
        response = requests.post(api_url,files={"file":uploaded_file})
            # md_link = response.
        if response.status_code == 200 :
            # response_data =  response.text

            # getting data from s3 link
            markdown_response = response.text
        

            if markdown_response:
            #         md_data = markdown_response.text
                    st.markdown(markdown_response,unsafe_allow_html=True)
            else :
                    st.error("error: markdown")
            
        
        # st.error(f"Failed to process {requests.status_codes}")
    except requests.exceptions.RequestException as e :
        st.error("Error occured")

else :
    api_url = None



