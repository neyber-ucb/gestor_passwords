# Gestor de Contraseñas Seguro

Aplicación de consola para gestionar contraseñas de forma segura, utilizando técnicas de cifrado para proteger la información sensible.

## Características

- Almacenamiento seguro de contraseñas mediante cifrado
- Persistencia de datos en archivos encriptados
- Interfaz de consola intuitiva
- Funcionalidades para crear, ver, buscar y eliminar contraseñas
- Sistema de contraseña maestra para proteger el acceso

## Requisitos

- Python 3.8 o superior
- Bibliotecas requeridas (ver `requirements.txt`)

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/gestor-contrasenas-seguro.git
   cd gestor-contrasenas-seguro
   ```

2. Crear y activar un entorno virtual:
   ```
   # En sistemas Unix/Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # En Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Asegúrate de tener el entorno virtual activado:
   ```
   # El prompt de tu terminal debería mostrar (venv)
   # Si no está activado, ejecuta:
   
   # En sistemas Unix/Linux/macOS
   source venv/bin/activate
   
   # En Windows
   venv\Scripts\activate
   ```

2. Ejecutar la aplicación:
   ```
   python main.py
   ```

3. En el primer inicio, se solicitará crear una contraseña maestra para proteger el acceso al gestor.

4. Utilizar el menú interactivo para gestionar las contraseñas:
   - Agregar nuevas contraseñas
   - Ver contraseñas almacenadas
   - Buscar contraseñas por servicio
   - Eliminar contraseñas
   - Cambiar la contraseña maestra

## Seguridad

- Las contraseñas se almacenan cifradas utilizando algoritmos de cifrado simétrico (AES-256)
- La contraseña maestra se protege mediante hash (PBKDF2-HMAC-SHA256)
- Los datos se guardan en archivos encriptados

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
