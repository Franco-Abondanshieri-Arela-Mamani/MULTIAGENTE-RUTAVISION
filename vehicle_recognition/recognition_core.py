import cv2
import pytesseract
import numpy as np
from PIL import Image

# Forzar la ruta de Tesseract en Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocesar_imagen(imagen_ruta_o_array):
    """
    Preprocesa una imagen para mejorar el reconocimiento OCR.
    Acepta ruta de archivo o un array NumPy (imagen de OpenCV).
    """
    if isinstance(imagen_ruta_o_array, str):
        img = cv2.imread(imagen_ruta_o_array)
    else:
        img = imagen_ruta_o_array

    if img is None:
        raise ValueError("No se pudo cargar la imagen. Verifique la ruta o el formato.")

    # Convertir a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización OTSU
    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binaria

def reconocer_numero_vehiculo(datos_imagen):
    """
    Reconoce un número de vehículo en una imagen.
    datos_imagen puede ser un archivo de bytes (ej. de una solicitud POST).
    """
    try:
        imagen = Image.open(datos_imagen)
        img_np = np.array(imagen)

        if img_np.shape[2] == 4:
            img_np = img_np[:, :, :3]

        procesada = preprocesar_imagen(img_np)

        config = '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        texto = pytesseract.image_to_string(procesada, config=config).strip()

        numero_vehiculo = ''.join(filter(str.isdigit, texto))

        if numero_vehiculo:
            return {"detectado": True, "numero": numero_vehiculo, "texto_crudo": texto}
        else:
            return {"detectado": False, "numero": None, "texto_crudo": texto}

    except Exception as e:
        return {"detectado": False, "numero": None, "error": str(e)}

# Ejemplo de uso local
if __name__ == "__main__":
    try:
        with open('test_vehiculo_32.png', 'rb') as f:
            resultado = reconocer_numero_vehiculo(f)
            print(f"Resultado del reconocimiento (desde archivo): {resultado}")
    except FileNotFoundError:
        print("Crea un archivo 'test_vehiculo_32.png' para probar el reconocimiento.")
    except Exception as e:
        print(f"Error durante la prueba de archivo: {e}")

    try:
        dummy_img = np.zeros((100, 300, 3), dtype=np.uint8)
        cv2.putText(dummy_img, "32", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        is_success, buffer = cv2.imencode(".png", dummy_img)
        if is_success:
            from io import BytesIO
            resultado_bytes = reconocer_numero_vehiculo(BytesIO(buffer.tobytes()))
            print(f"Resultado del reconocimiento (desde bytes simulados): {resultado_bytes}")
    except Exception as e:
        print(f"Error durante la prueba de bytes simulados: {e}") 