#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo principal del Gestor de Contraseñas Seguro.
Contiene la clase PasswordManager que maneja el almacenamiento y recuperación de contraseñas.
"""

import os
import json
import datetime
from crypto_utils import (
    get_master_key,
    encrypt_password,
    decrypt_password,
    setup_master_password
)

class PasswordManager:
    """
    Clase principal para el gestor de contraseñas.
    Maneja el almacenamiento y recuperación de contraseñas de forma segura.
    """
    
    def __init__(self, master_password):
        """
        Inicializa el gestor de contraseñas.
        
        Args:
            master_password (str): Contraseña maestra para acceder al gestor
        """
        self.master_key = get_master_key(master_password)
        self.db_file = "passwords.db"
        self.passwords = self._load_passwords()
    
    def _load_passwords(self):
        """
        Carga las contraseñas desde el archivo de base de datos.
        
        Returns:
            dict: Diccionario con las contraseñas almacenadas
        """
        if not os.path.exists(self.db_file):
            return {}
        
        try:
            with open(self.db_file, "rb") as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return {}
            
            # Descifrar los datos
            json_data = decrypt_password(encrypted_data.decode('utf-8'), self.master_key)
            
            if json_data:
                return json.loads(json_data)
            else:
                return {}
        except Exception as e:
            print(f"Error al cargar las contraseñas: {e}")
            return {}
    
    def _save_passwords(self):
        """
        Guarda las contraseñas en el archivo de base de datos.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        try:
            # Convertir el diccionario a JSON
            json_data = json.dumps(self.passwords)
            
            # Cifrar los datos
            encrypted_data = encrypt_password(json_data, self.master_key)
            
            # Guardar los datos cifrados
            with open(self.db_file, "wb") as f:
                f.write(encrypted_data.encode('utf-8'))
            
            return True
        except Exception as e:
            print(f"Error al guardar las contraseñas: {e}")
            return False
    
    def add_password(self, service, username, password):
        """
        Agrega una nueva contraseña al gestor.
        
        Args:
            service (str): Nombre del servicio
            username (str): Nombre de usuario o correo
            password (str): Contraseña
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        try:
            # Generar un ID único para la contraseña
            password_id = f"{service}_{username}"
            
            # Cifrar la contraseña
            encrypted_password = encrypt_password(password, self.master_key)
            
            # Guardar la contraseña en el diccionario
            self.passwords[password_id] = {
                "service": service,
                "username": username,
                "password": encrypted_password,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            
            # Guardar los cambios
            return self._save_passwords()
        except Exception as e:
            print(f"Error al agregar la contraseña: {e}")
            return False
    
    def get_password(self, service, username):
        """
        Obtiene una contraseña del gestor.
        
        Args:
            service (str): Nombre del servicio
            username (str): Nombre de usuario o correo
            
        Returns:
            tuple: (service, username, password, date) o None si no se encuentra
        """
        try:
            password_id = f"{service}_{username}"
            
            if password_id in self.passwords:
                password_data = self.passwords[password_id]
                
                # Descifrar la contraseña
                decrypted_password = decrypt_password(
                    password_data["password"],
                    self.master_key
                )
                
                return (
                    password_data["service"],
                    password_data["username"],
                    decrypted_password,
                    password_data["date"]
                )
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la contraseña: {e}")
            return None
    
    def get_all_passwords(self):
        """
        Obtiene todas las contraseñas almacenadas.
        
        Returns:
            list: Lista de tuplas (service, username, password, date)
        """
        try:
            result = []
            
            for password_id, password_data in self.passwords.items():
                # Descifrar la contraseña
                decrypted_password = decrypt_password(
                    password_data["password"],
                    self.master_key
                )
                
                result.append((
                    password_data["service"],
                    password_data["username"],
                    decrypted_password,
                    password_data["date"]
                ))
            
            return result
        except Exception as e:
            print(f"Error al obtener las contraseñas: {e}")
            return []
    
    def search_passwords(self, query):
        """
        Busca contraseñas por servicio.
        
        Args:
            query (str): Término de búsqueda
            
        Returns:
            list: Lista de tuplas (service, username, password, date) que coinciden con la búsqueda
        """
        try:
            query = query.lower()
            result = []
            
            for password_id, password_data in self.passwords.items():
                if query in password_data["service"].lower():
                    # Descifrar la contraseña
                    decrypted_password = decrypt_password(
                        password_data["password"],
                        self.master_key
                    )
                    
                    result.append((
                        password_data["service"],
                        password_data["username"],
                        decrypted_password,
                        password_data["date"]
                    ))
            
            return result
        except Exception as e:
            print(f"Error al buscar las contraseñas: {e}")
            return []
    
    def delete_password(self, service, username):
        """
        Elimina una contraseña del gestor.
        
        Args:
            service (str): Nombre del servicio
            username (str): Nombre de usuario o correo
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        try:
            password_id = f"{service}_{username}"
            
            if password_id in self.passwords:
                del self.passwords[password_id]
                return self._save_passwords()
            else:
                return False
        except Exception as e:
            print(f"Error al eliminar la contraseña: {e}")
            return False
    
    def change_master_password(self, new_password):
        """
        Cambia la contraseña maestra del gestor.
        
        Args:
            new_password (str): Nueva contraseña maestra
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        try:
            # Obtener todas las contraseñas descifradas
            all_passwords = self.get_all_passwords()
            
            # Configurar la nueva contraseña maestra
            setup_master_password(new_password)
            
            # Obtener la nueva clave maestra
            new_master_key = get_master_key(new_password)
            
            # Actualizar la clave maestra
            self.master_key = new_master_key
            
            # Reinicializar el diccionario de contraseñas
            self.passwords = {}
            
            # Volver a agregar todas las contraseñas con la nueva clave maestra
            for service, username, password, _ in all_passwords:
                self.add_password(service, username, password)
            
            return True
        except Exception as e:
            print(f"Error al cambiar la contraseña maestra: {e}")
            return False
