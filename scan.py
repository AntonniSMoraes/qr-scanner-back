import fitz
import cv2
import numpy as np
import os

# Criar pasta para as imagens se não existir
IMAGE_DIR = "temp_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def scan_pdf_wechat(pdf_content):
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    detector = cv2.wechat_qrcode_WeChatQRCode()
    
    full_report = [] # Mudando para lista para facilitar o Map no React Native

    for page_num in range(len(doc)):
        page = doc[page_num]
        # Zoom 2 é suficiente para visualização e economiza banda/memória
        mat = fitz.Matrix(2, 2) 
        pix = page.get_pixmap(matrix=mat)
        
        # Salvar a imagem da página
        image_filename = f"page_{page_num + 1}.jpg"
        image_path = os.path.join(IMAGE_DIR, image_filename)
        pix.save(image_path)

        # Converter para OpenCV detectar QR
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n >= 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        res, points = detector.detectAndDecode(img)

        page_results = []
        if res:
            for i, url in enumerate(res):
                if url:
                    rect_points = points[i]
                    x_min = float(np.min(rect_points[:, 0]))
                    y_min = float(np.min(rect_points[:, 1]))
                    x_max = float(np.max(rect_points[:, 0]))
                    y_max = float(np.max(rect_points[:, 1]))

                    page_results.append({
                        "url": url,
                        "x_pct": round((x_min / pix.width) * 100, 2),
                        "y_pct": round((y_min / pix.height) * 100, 2),
                        "w_pct": round(((x_max - x_min) / pix.width) * 100, 2),
                        "h_pct": round(((y_max - y_min) / pix.height) * 100, 2)
                    })

        full_report.append({
            "page": page_num + 1,
            "image_url": f"/static/{image_filename}", # Rota que o FastAPI vai servir
            "qrcodes": page_results
        })

    return full_report
