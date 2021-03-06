import subprocess
import shutil
import uuid
import os
import base64
from io import BytesIO


# Title: Resize images to a smaller size
# Description: This extension demonstrate how you can call the GraphicsMagick library from the command
# Description: line in an extension. You could use that on the document body, a thumbnail or a field containing binary 
# Description: data in base64 format (like an avatar, when indexing users)
# Required data: 

# Command line command and arguments
COMPRESS_CMDLINE = 'gm convert {} -resample 150 -compress JPEG -quality 50 {}'

# decode to bytes
byte_data = BytesIO(base64.b64decode(document.get_meta_data_value("base64data")[0]))

document_api.v1.log("Original size: " + str(len(document.get_meta_data_value("base64data")[0])), severity="normal")

# Define original and compressed filenames
# original_file = os.path.join(document_api.working_path, str(uuid.uuid4()))
original_file = os.path.join(os.getcwd(), str(uuid.uuid4()))
compressed_file = original_file + ".jpg"

document_api.v1.log("Paths:" + original_file + "::" + compressed_file, severity="normal")

# Write the image to disk
with open(original_file, 'wb') as f:
    shutil.copyfileobj(byte_data, f)

document_api.v1.log("Image written to disk", severity="normal")

convert = subprocess.Popen(COMPRESS_CMDLINE.format(original_file, compressed_file), shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
out, err = convert.communicate()

document_api.v1.log("Errors (if any): " + out + "::" + err, severity="normal")

document_api.v1.log("Image compressed", severity="normal")

with open(compressed_file, 'rb') as f:
    base64data = base64.b64encode(f.read())
    document_api.v1.log("New size: " + str(len(base64data)), severity="normal")
    
document_api.v1.add_meta_data({"base64data": base64data})
