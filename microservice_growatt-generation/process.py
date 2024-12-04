# Importamos las clases ABC y abstractmethod del módulo abc
from abc import ABC, abstractmethod

# Definimos la clase AbstractAPI que hereda de ABC (clase base para crear clases abstractas)
class AbstractAPI(ABC):
    # Definimos el método try_step
    def try_step(self, step_method, *args):
        # Intentamos ejecutar el método step_method hasta 6 veces
        for _ in range(6):
            try:
                # Si el método se ejecuta correctamente, devolvemos el resultado
                return step_method(*args)
            except Exception as e:
                # Si ocurre una excepción, imprimimos un mensaje de error y volvemos a intentarlo
                print(f"Error durante {step_method.__name__}: {e}. Reintentando...")
        # Si después de 6 intentos el método no se ha ejecutado correctamente, lanzamos una excepción
        raise Exception(f"Fallo al ejecutar {step_method.__name__} después de 6 intentos")

    # Definimos el método execute
    def execute(self):
        # Intentamos ejecutar el método automation y guardamos el resultado en la variable path_xlsx
        path_xlsx = self.try_step(self.automation)

    # Definimos el método abstracto automation
    @abstractmethod
    def automation(self):
        pass