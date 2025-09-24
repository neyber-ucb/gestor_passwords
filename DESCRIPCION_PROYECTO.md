# Gestor de Contraseñas Seguro - Descripción del Proyecto

## Información General

- **Nombre del Proyecto**: Gestor de Contraseñas Seguro
- **Desarrollador**: [Tu Nombre]
- **Fecha**: Septiembre 2025
- **Repositorio**: [URL del repositorio GitHub/GitLab]

## Descripción del Proyecto

El Gestor de Contraseñas Seguro es una aplicación de consola desarrollada como parte del trabajo final del curso de Seguridad Informática. La aplicación permite a los usuarios almacenar, administrar y proteger múltiples contraseñas de forma segura, evitando la reutilización y el almacenamiento inseguro de las mismas.

## Tecnologías Empleadas

### Lenguaje de Programación
- **Python 3.8+**: Elegido por su facilidad de uso, amplia disponibilidad de bibliotecas de criptografía y portabilidad entre sistemas operativos.

### Bibliotecas Principales
- **cryptography (v41.0.5)**: Biblioteca de criptografía de alto nivel que proporciona primitivas criptográficas seguras y actualizadas.
- **pycryptodome (v3.19.0)**: Implementación de algoritmos criptográficos de bajo nivel.
- **colorama (v0.4.6)**: Para mejorar la experiencia de usuario en la consola con colores.
- **tabulate (v0.9.0)**: Para formatear tablas en la consola.

### Algoritmos Criptográficos
- **AES-256-GCM**: Algoritmo de cifrado simétrico utilizado para proteger las contraseñas almacenadas.
- **PBKDF2-HMAC-SHA256**: Función de derivación de claves basada en contraseña para proteger la contraseña maestra.
- **Salting**: Uso de valores aleatorios (salt) para prevenir ataques de diccionario y de tabla arcoíris.

### Almacenamiento
- **Archivos encriptados**: Las contraseñas se almacenan en un archivo encriptado (`passwords.db`) utilizando AES-256-GCM.
- **Separación de datos sensibles**: La contraseña maestra se almacena de forma separada en `master.key` como un hash derivado con PBKDF2.

## Funcionalidades Implementadas

1. **Sistema de Contraseña Maestra**
   - Creación y verificación segura de la contraseña maestra
   - Limitación de intentos fallidos (3 intentos)
   - Cambio de contraseña maestra con re-cifrado de todas las contraseñas almacenadas

2. **Gestión de Contraseñas**
   - Agregar nuevas contraseñas con servicio, usuario y contraseña
   - Ver listado de contraseñas almacenadas
   - Buscar contraseñas por servicio
   - Eliminar contraseñas existentes

3. **Seguridad**
   - Cifrado de contraseñas utilizando AES-256-GCM
   - Protección de la contraseña maestra con PBKDF2-HMAC-SHA256
   - Almacenamiento seguro en archivos encriptados
   - Uso de `getpass` para ocultar la entrada de contraseñas
   - Comparación de hashes en tiempo constante para prevenir ataques de tiempo

4. **Interfaz de Usuario**
   - Interfaz de consola intuitiva con menús claros
   - Uso de colores para mejorar la experiencia de usuario
   - Mensajes de error y confirmación claros

## Decisiones Técnicas

### Cifrado Simétrico vs. Asimétrico
Se optó por utilizar cifrado simétrico (AES-256-GCM) para las contraseñas almacenadas debido a:
- **Eficiencia**: El cifrado simétrico es más rápido y requiere menos recursos.
- **Simplicidad**: Para una aplicación local, el cifrado simétrico es suficiente.
- **Seguridad**: AES-256-GCM proporciona confidencialidad y autenticación de los datos.

### Protección de la Contraseña Maestra
Para proteger la contraseña maestra se utilizó PBKDF2-HMAC-SHA256 con:
- **100,000 iteraciones**: Para aumentar el costo computacional de un ataque de fuerza bruta.
- **Salt aleatorio de 16 bytes**: Para prevenir ataques de diccionario y de tabla arcoíris.
- **Clave derivada de 32 bytes**: Para proporcionar una seguridad de 256 bits.

### Estructura del Proyecto
El proyecto se organizó en módulos separados para facilitar el mantenimiento y la comprensión:
- **main.py**: Punto de entrada de la aplicación y lógica principal.
- **crypto_utils.py**: Funciones criptográficas para cifrado, descifrado y hash.
- **password_manager.py**: Clase principal para gestionar las contraseñas.
- **ui.py**: Funciones para la interfaz de usuario.

### Almacenamiento de Datos
Se decidió utilizar archivos encriptados en lugar de una base de datos SQL por:
- **Simplicidad**: No requiere configuración adicional de bases de datos.
- **Portabilidad**: Los archivos pueden ser fácilmente respaldados o transferidos.
- **Seguridad**: Todo el contenido del archivo está cifrado, no solo las contraseñas.

## Capturas de Pantalla

[Aquí se incluirían capturas de pantalla de la aplicación en funcionamiento]

## Conclusiones y Mejoras Futuras

El Gestor de Contraseñas Seguro cumple con los requisitos establecidos, proporcionando una solución segura y funcional para el almacenamiento y gestión de contraseñas. Sin embargo, existen varias mejoras que podrían implementarse en el futuro:

1. **Interfaz gráfica**: Desarrollar una interfaz gráfica para mejorar la experiencia de usuario.
2. **Generador de contraseñas**: Añadir una función para generar contraseñas seguras.
3. **Sincronización en la nube**: Permitir la sincronización segura de las contraseñas entre dispositivos.
4. **Autenticación de dos factores**: Implementar 2FA para aumentar la seguridad.
5. **Exportación e importación**: Permitir la exportación e importación segura de contraseñas.

## Referencias

1. [Documentación de la biblioteca cryptography](https://cryptography.io/en/latest/)
2. [NIST SP 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
3. [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
