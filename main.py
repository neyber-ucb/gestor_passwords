#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gestor de Contraseñas Seguro
----------------------------
Aplicación de consola para gestionar contraseñas de forma segura.
"""

import os
import sys
import time
from getpass import getpass
from colorama import init, Fore, Style

# Importaciones locales
from password_manager import PasswordManager
from crypto_utils import setup_master_password, verify_master_password
from ui import clear_screen, print_header, print_menu, get_input

# Inicializar colorama para colores en consola
init(autoreset=True)

def main():
    """Función principal del gestor de contraseñas"""
    
    # Verificar si es la primera ejecución
    first_run = not os.path.exists("master.key")
    
    # Configuración inicial si es la primera ejecución
    if first_run:
        clear_screen()
        print_header("CONFIGURACIÓN INICIAL")
        print("\nBienvenido al Gestor de Contraseñas Seguro.")
        print("Para comenzar, debe crear una contraseña maestra.")
        print("Esta contraseña protegerá todas sus contraseñas almacenadas.")
        print(f"{Fore.YELLOW}IMPORTANTE: No olvide esta contraseña. No hay forma de recuperarla.")
        
        while True:
            master_password = getpass("\nIngrese su contraseña maestra: ")
            confirm_password = getpass("Confirme su contraseña maestra: ")
            
            if master_password == confirm_password:
                if len(master_password) < 8:
                    print(f"{Fore.RED}La contraseña debe tener al menos 8 caracteres.")
                    continue
                setup_master_password(master_password)
                print(f"{Fore.GREEN}Contraseña maestra configurada correctamente.")
                time.sleep(1.5)
                break
            else:
                print(f"{Fore.RED}Las contraseñas no coinciden. Intente nuevamente.")
    
    # Verificar la contraseña maestra para acceder al gestor
    clear_screen()
    print_header("GESTOR DE CONTRASEÑAS")
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        master_password = getpass("\nIngrese su contraseña maestra: ")
        if verify_master_password(master_password):
            # Inicializar el gestor de contraseñas con la contraseña maestra
            password_manager = PasswordManager(master_password)
            run_password_manager(password_manager)
            return
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"{Fore.RED}Contraseña incorrecta. Intentos restantes: {remaining}")
            else:
                print(f"{Fore.RED}Demasiados intentos fallidos. Saliendo por seguridad.")
                sys.exit(1)

def run_password_manager(password_manager):
    """Ejecuta el bucle principal del gestor de contraseñas"""
    
    while True:
        clear_screen()
        print_header("GESTOR DE CONTRASEÑAS")
        print_menu([
            "Agregar nueva contraseña",
            "Ver contraseñas almacenadas",
            "Buscar contraseña por servicio",
            "Eliminar contraseña",
            "Cambiar contraseña maestra",
            "Salir"
        ])
        
        option = get_input("\nSeleccione una opción: ", range(1, 7))
        
        if option == 1:
            add_password(password_manager)
        elif option == 2:
            view_passwords(password_manager)
        elif option == 3:
            search_password(password_manager)
        elif option == 4:
            delete_password(password_manager)
        elif option == 5:
            change_master_password(password_manager)
        elif option == 6:
            clear_screen()
            print("Gracias por usar el Gestor de Contraseñas Seguro.")
            print("Saliendo...")
            time.sleep(1)
            sys.exit(0)

def add_password(password_manager):
    """Agrega una nueva contraseña al gestor"""
    clear_screen()
    print_header("AGREGAR NUEVA CONTRASEÑA")
    
    service = input("Ingrese el nombre del servicio: ")
    username = input("Ingrese el usuario o correo: ")
    password = getpass("Ingrese la contraseña: ")
    confirm = getpass("Confirmar contraseña: ")
    
    if password != confirm:
        print(f"{Fore.RED}Las contraseñas no coinciden.")
        input("\nPresione Enter para continuar.")
        return
    
    success = password_manager.add_password(service, username, password)
    
    if success:
        print(f"{Fore.GREEN}Contraseña para '{service}' guardada correctamente.")
    else:
        print(f"{Fore.RED}Error al guardar la contraseña.")
    
    input("\nPresione Enter para continuar.")

def view_passwords(password_manager):
    """Muestra todas las contraseñas almacenadas"""
    clear_screen()
    print_header("CONTRASEÑAS ALMACENADAS")
    
    passwords = password_manager.get_all_passwords()
    
    if not passwords:
        print("No hay contraseñas almacenadas.")
        input("\nPresione Enter para continuar.")
        return
    
    while True:
        clear_screen()
        print_header("CONTRASEÑAS ALMACENADAS")
        
        # Mostrar lista de contraseñas
        print(f"{'#':<3} {'Servicio':<20} {'Usuario':<25} {'Fecha':<12}")
        print("-" * 60)
        
        for i, (service, username, _, date) in enumerate(passwords, 1):
            print(f"{i:<3} {service:<20} {username:<25} {date:<12}")
        
        print("\nSeleccione número para ver detalles o '0' para volver")
        option = get_input(": ", range(0, len(passwords) + 1))
        
        if option == 0:
            break
        
        # Mostrar detalles de la contraseña seleccionada
        service, username, password, date = passwords[option - 1]
        
        clear_screen()
        print_header(f"DETALLES - {service.upper()}")
        print(f"Servicio: {service}")
        print(f"Usuario: {username}")
        print(f"Contraseña: {password}")
        print(f"Fecha de creación: {date}")
        
        input("\nPresione Enter para continuar.")

def search_password(password_manager):
    """Busca contraseñas por servicio"""
    clear_screen()
    print_header("BUSCAR CONTRASEÑA POR SERVICIO")
    
    query = input("Ingrese el nombre del servicio a buscar: ")
    results = password_manager.search_passwords(query)
    
    if not results:
        print(f"No se encontraron resultados para '{query}'.")
        input("\nPresione Enter para continuar.")
        return
    
    print(f"\nSe encontraron {len(results)} resultados:")
    print(f"{'#':<3} {'Servicio':<20} {'Usuario':<25}")
    print("-" * 50)
    
    for i, (service, username, _, _) in enumerate(results, 1):
        print(f"{i:<3} {service:<20} {username:<25}")
    
    print("\nSeleccione número para ver detalles o '0' para volver")
    option = get_input(": ", range(0, len(results) + 1))
    
    if option != 0:
        service, username, password, date = results[option - 1]
        
        clear_screen()
        print_header(f"DETALLES - {service.upper()}")
        print(f"Servicio: {service}")
        print(f"Usuario: {username}")
        print(f"Contraseña: {password}")
        print(f"Fecha de creación: {date}")
    
    input("\nPresione Enter para continuar.")

def delete_password(password_manager):
    """Elimina una contraseña del gestor"""
    clear_screen()
    print_header("ELIMINAR CONTRASEÑA")
    
    passwords = password_manager.get_all_passwords()
    
    if not passwords:
        print("No hay contraseñas almacenadas.")
        input("\nPresione Enter para continuar.")
        return
    
    print(f"{'#':<3} {'Servicio':<20} {'Usuario':<25}")
    print("-" * 50)
    
    for i, (service, username, _, _) in enumerate(passwords, 1):
        print(f"{i:<3} {service:<20} {username:<25}")
    
    print("\nSeleccione número para eliminar o '0' para cancelar")
    option = get_input(": ", range(0, len(passwords) + 1))
    
    if option == 0:
        return
    
    service, username, _, _ = passwords[option - 1]
    
    print(f"\n¿Está seguro de eliminar la contraseña de '{service}' ({username})? (s/n)")
    confirm = input(": ").lower()
    
    if confirm == 's':
        success = password_manager.delete_password(service, username)
        
        if success:
            print(f"{Fore.GREEN}Contraseña eliminada correctamente.")
        else:
            print(f"{Fore.RED}Error al eliminar la contraseña.")
    
    input("\nPresione Enter para continuar.")

def change_master_password(password_manager):
    """Cambia la contraseña maestra"""
    clear_screen()
    print_header("CAMBIAR CONTRASEÑA MAESTRA")
    
    current_password = getpass("Ingrese su contraseña maestra actual: ")
    
    if not verify_master_password(current_password):
        print(f"{Fore.RED}Contraseña incorrecta.")
        input("\nPresione Enter para continuar.")
        return
    
    new_password = getpass("Ingrese su nueva contraseña maestra: ")
    confirm_password = getpass("Confirme su nueva contraseña maestra: ")
    
    if new_password != confirm_password:
        print(f"{Fore.RED}Las contraseñas no coinciden.")
        input("\nPresione Enter para continuar.")
        return
    
    if len(new_password) < 8:
        print(f"{Fore.RED}La contraseña debe tener al menos 8 caracteres.")
        input("\nPresione Enter para continuar.")
        return
    
    success = password_manager.change_master_password(new_password)
    
    if success:
        print(f"{Fore.GREEN}Contraseña maestra cambiada correctamente.")
    else:
        print(f"{Fore.RED}Error al cambiar la contraseña maestra.")
    
    input("\nPresione Enter para continuar.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario. Saliendo...")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {e}")
        sys.exit(1)
