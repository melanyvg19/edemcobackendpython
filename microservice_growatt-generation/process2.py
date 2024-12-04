# Importamos las clases ABC y abstractmethod del módulo abc
from abc import ABC, abstractmethod

# Definimos la clase AbstractAPI que hereda de ABC (clase base para crear clases abstractas)
class AbstractAPI(ABC):
    # Definimos el método try_step
    def try_step(self, step_method, *args):
        # Intentamos ejecutar el método step_method hasta 5 veces
        for _ in range(5):
            try:
                # Si el método se ejecuta correctamente, devolvemos el resultado
                return step_method(*args)
            except Exception as e:
                # Si ocurre una excepción, imprimimos un mensaje de error y volvemos a intentarlo
                print(f"Error durante {step_method.__name__}: {e}. Reintentando...")
        # Si después de 5 intentos el método no se ha ejecutado correctamente, lanzamos una excepción
        raise Exception(f"Fallo al ejecutar {step_method.__name__} después de 3 intentos")

    # Definimos el método execute
    def execute(self):
        # Intentamos ejecutar el método data_parameters y guardamos el resultado en la variable json_data
        json_data = self.try_step(self.data_parameters)
        # Devolvemos los datos en formato JSON
        return json_data

    # Definimos el método abstracto data_parameters
    @abstractmethod
    def data_parameters(self):
        pass