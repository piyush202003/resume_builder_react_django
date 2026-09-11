import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY")
)

IMAGEKIT_URL_ENDPOINT = os.environ.get("IMAGEKIT_URL_ENDPOINT")

def upload_resume_image(file, resume_id, remove_background):
    transformation = "w-300,h-300,fo-face,z-0.75"
    if remove_background:
        transformation += ",e-bgremove"

    response = imagekit.files.upload(
        file = file.read(),
        file_name=file.name,
        folder=f'/resumes/{resume_id}/',
        transformation= {
            "pre" : transformation
        }
    )
    return response.url