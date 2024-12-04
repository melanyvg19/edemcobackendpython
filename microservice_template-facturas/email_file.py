import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from info_email import DTO_email
import os
import pyodbc

class EmailIntegracion:

    @staticmethod
    def email_credenciales(cod_planta, correo, password):
        DB_CONFIG = {
            'DRIVER': '{ODBC Driver 17 for SQL Server}',
            'SERVER': '10.255.252.2',
            'DATABASE': 'edemco',
            'UID': 'temptech',
            'PWD': 'Edemco2024*+'
        }

        conn = None
        cursor = None

        try:
            conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.255.252.2;DATABASE=edemco;UID=temptech;PWD=Edemco2024*+'
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.email 
                FROM email e
                JOIN planta p ON e.id_planta = p.id_planta
                WHERE e.id_planta = ?
            """, (cod_planta,))
            result = cursor.fetchall()

            email_list = [row.email for row in result]

        except pyodbc.Error as e:
            print(f"Error para cod planta: {cod_planta}: {e}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        info_email = DTO_email()
        asunto, route = info_email.execute(cod_planta)
        url_img = r'C:\\Users\\usuario\Desktop\\Encabezado_correo.png'

        name_archive = os.path.basename(route)
        sender_email = correo
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(email_list)
        msg['Subject'] = asunto
        html_body = """
        <html>
            <body>
                <img src="cid:image1" alt="Factura">
            </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        if url_img:
            with open(url_img, 'rb') as f:
                mime_image = MIMEImage(f.read())
                mime_image.add_header('Content-ID', '<image1>')  # Relacionado con el CID en el cuerpo del correo
                mime_image.add_header('Content-Disposition', 'inline', filename="Encabezado_correo.png")
                msg.attach(mime_image)

        # Adjuntar el archivo PDF, solo el PDF, no la imagen
        with open(route, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=name_archive)
            msg.attach(pdf_attachment)

        # Envío del correo
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
        smtp_username = sender_email
        smtp_password = password
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, email_list, msg.as_string())
