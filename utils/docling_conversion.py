from pathlib import Path
from docling.datamodel.base_models import FigureElement, InputFormat, Table
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from utils.aws import s3
from io import BytesIO
import os 

def pdf_to_md_docling(pdf_path):
    input_doc_path = Path(pdf_path)
    # output_dir = Path("docling_conversion")
    s3_client = s3.get_s3client()
    bucket_name = os.getenv('BUCKET_NAME')

    IMAGE_RESOLUTION_SCALE = 2.0

    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    conv_res = doc_converter.convert(input_doc_path)
    # output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_res.input.file.stem
    
    temp_md_path = Path(f"temp_{doc_filename}_with_image_refs.md")

    try :
        conv_res.document.save_as_markdown(temp_md_path, image_mode=ImageRefMode.REFERENCED )
        # Save markdown with externally referenced pictures
        # md_filename = output_dir / f"{doc_filename}-with-image-refs.md"
        # md_data = BytesIO(md_filename.encode('utf-8'))
        with open(temp_md_path, "rb") as file:
            s3_key = f"docling_Conversion/{doc_filename}-converted.md"   
        # conv_res.document.save_as_markdown(md_filename, image_mode=ImageRefMode.REFERENCED)

            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key
            )

        public_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    
    except Exception as e :
        print(e)
    
    return public_url 
