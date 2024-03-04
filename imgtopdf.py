import os
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from PIL import Image
def convert_images_to_pdf(folder_path, output_pdf):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    # Filter only PNG files
    image_paths = [os.path.join(folder_path, file) for file in files if file.lower().endswith('.png')]
    # Set custom page size
    custom_page_size = (22.04*72, 15.58*72)  # Convert inches to points (1 inch = 72 points)
    c = canvas.Canvas(output_pdf, pagesize=landscape(custom_page_size))
    for image_path in image_paths:
        img = Image.open(image_path)
        img_width, img_height = img.size
        # Reduce resolution to 150 dpi
        img = img.resize((int(img_width * 150 / 72), int(img_height * 150 / 72)), Image.LANCZOS)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        # Adjust image width and height to fit the page width
        if aspect_ratio > 1:
            img_width = custom_page_size[0] - 50
            img_height = img_width / aspect_ratio
        else:
            img_height = custom_page_size[1] - 50
            img_width = img_height * aspect_ratio
        c.setPageSize((custom_page_size[1], custom_page_size[0]))  # Flip width and height for landscape
        # Convert image to RGB mode before saving as JPEG
        img = img.convert("RGB")
        # Save the image as JPEG with higher compression
        img.save("temp.jpg", quality=60)  # Adjust quality as needed
        c.drawImage("temp.jpg", 0, 0, width=img_width, height=img_height)
        os.remove("temp.jpg")  # Delete temporary image file
        c.showPage()
    c.save()
    print("PDF generated successfully.")
# Folder path containing PNG images
folder_path = r"D:\lenova\Barcode\png_testing"
# Output PDF file
output_pdf = "output.pdf"
# Convert PNG images to PDF
convert_images_to_pdf(folder_path, output_pdf)