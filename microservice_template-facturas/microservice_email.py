from email_file import EmailIntegracion

class microservice_email(EmailIntegracion):
    
    @staticmethod
    def ejecucion(cod_planta, correo, password):

        instance_email = EmailIntegracion()
        instance_email.email_credenciales(cod_planta, correo, password)
