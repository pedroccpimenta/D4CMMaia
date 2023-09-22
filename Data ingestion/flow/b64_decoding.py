# FLOW FROM SKY
# Emanuel Ferreira, Julho-Outubro 2022
# emanuel.ferreira@cm-maia.pt

# IMPORTS
# -------------------------------------------------------------------------------------------------------------
import flow_creds
import base64
# -------------------------------------------------------------------------------------------------------------

# CAMERA FRAME DECODING
base64_img = flow_creds.cframe
base64_img_bytes = base64_img.encode('utf-8')
with open (r"C:\Users\cmm1490\Documents\!MAIN\Projetos\Repositórios Git\Yunex-Data-Pipeline\Data export\camera_frame.png", 'wb') as file_to_save:
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    file_to_save.write(decoded_image_data)