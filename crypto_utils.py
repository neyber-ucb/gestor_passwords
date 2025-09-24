#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de utilidades criptográficas para el Gestor de Contraseñas Seguro.
Proporciona funciones para el manejo seguro de la contraseña maestra y el cifrado de contraseñas.
"""

import os
import base64
import hashlib
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

# Constantes para el cifrado
SALT_SIZE = 16  # 128 bits
KEY_SIZE = 32   # 256 bits
NONCE_SIZE = 12 # 96 bits
ITERATIONS = 100000

def generate_salt():
    """
    Genera un salt aleatorio para el hash de la contraseña.
    
    Returns:
        bytes: Salt aleatorio de 16 bytes (128 bits)
    """
    return os.urandom(SALT_SIZE)

def derive_key(password, salt):
    """
    Deriva una clave a partir de una contraseña y un salt utilizando PBKDF2.
    
    Args:
        password (str): Contraseña de la que derivar la clave
        salt (bytes): Salt para la derivación
        
    Returns:
        bytes: Clave derivada de 32 bytes (256 bits)
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def hash_password(password, salt=None):
    """
    Genera un hash seguro de la contraseña utilizando PBKDF2-HMAC-SHA256.
    
    Args:
        password (str): Contraseña a hashear
        salt (bytes, opcional): Salt para el hash. Si no se proporciona, se genera uno nuevo.
        
    Returns:
        tuple: (hash_bytes, salt_bytes)
    """
    if salt is None:
        salt = generate_salt()
    
    key = derive_key(password, salt)
    return key, salt

def setup_master_password(password):
    """
    Configura la contraseña maestra, generando un hash y guardándolo en un archivo.
    
    Args:
        password (str): Contraseña maestra a configurar
        
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        key, salt = hash_password(password)
        
        # Guardar el salt y el hash en el archivo master.key
        with open("master.key", "wb") as f:
            f.write(salt)
            f.write(key)
        
        return True
    except Exception as e:
        print(f"Error al configurar la contraseña maestra: {e}")
        return False

def verify_master_password(password):
    """
    Verifica si la contraseña proporcionada coincide con la contraseña maestra almacenada.
    
    Args:
        password (str): Contraseña a verificar
        
    Returns:
        bool: True si la contraseña es correcta, False en caso contrario
    """
    try:
        # Leer el salt y el hash del archivo master.key
        with open("master.key", "rb") as f:
            stored_salt = f.read(SALT_SIZE)
            stored_key = f.read(KEY_SIZE)
        
        # Generar el hash de la contraseña proporcionada con el mismo salt
        key, _ = hash_password(password, stored_salt)
        
        # Comparar los hashes (tiempo constante para evitar timing attacks)
        return secrets.compare_digest(key, stored_key)
    except Exception as e:
        print(f"Error al verificar la contraseña maestra: {e}")
        return False

def encrypt_data(data, key):
    """
    Cifra datos utilizando AES-GCM.
    
    Args:
        data (str): Datos a cifrar
        key (bytes): Clave de cifrado
        
    Returns:
        bytes: Datos cifrados (nonce + ciphertext + tag)
    """
    # Convertir los datos a bytes si es necesario
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Generar un nonce aleatorio
    nonce = os.urandom(NONCE_SIZE)
    
    # Cifrar los datos
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    
    # Devolver el nonce concatenado con el texto cifrado
    return nonce + ciphertext

def decrypt_data(encrypted_data, key):
    """
    Descifra datos utilizando AES-GCM.
    
    Args:
        encrypted_data (bytes): Datos cifrados (nonce + ciphertext + tag)
        key (bytes): Clave de cifrado
        
    Returns:
        str: Datos descifrados
    """
    try:
        # Extraer el nonce y el texto cifrado
        nonce = encrypted_data[:NONCE_SIZE]
        ciphertext = encrypted_data[NONCE_SIZE:]
        
        # Descifrar los datos
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Convertir los datos a string si es necesario
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"Error al descifrar los datos: {e}")
        return None

def encrypt_password(password, master_key):
    """
    Cifra una contraseña utilizando la clave maestra.
    
    Args:
        password (str): Contraseña a cifrar
        master_key (bytes): Clave maestra para el cifrado
        
    Returns:
        str: Contraseña cifrada en formato base64
    """
    encrypted = encrypt_data(password, master_key)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_password(encrypted_password, master_key):
    """
    Descifra una contraseña utilizando la clave maestra.
    
    Args:
        encrypted_password (str): Contraseña cifrada en formato base64
        master_key (bytes): Clave maestra para el descifrado
        
    Returns:
        str: Contraseña descifrada
    """
    try:
        encrypted_bytes = base64.b64decode(encrypted_password)
        return decrypt_data(encrypted_bytes, master_key)
    except Exception as e:
        print(f"Error al descifrar la contraseña: {e}")
        return None

def get_master_key(password):
    """
    Obtiene la clave maestra a partir de la contraseña maestra.
    
    Args:
        password (str): Contraseña maestra
        
    Returns:
        bytes: Clave maestra
    """
    try:
        with open("master.key", "rb") as f:
            salt = f.read(SALT_SIZE)
        
        key, _ = hash_password(password, salt)
        return key
    except Exception as e:
        print(f"Error al obtener la clave maestra: {e}")
        return None
