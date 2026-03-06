import fitz  # PyMuPDF
import cv2
import numpy as np
import io

def scan_pdf_wechat(pdf_content):
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    
    detector = cv2.wechat_qrcode_WeChatQRCode()
    full_report = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        zoom = 4
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
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

        full_report[page_num + 1] = page_results

    return full_report