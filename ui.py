#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de interfaz de usuario para el Gestor de Contraseñas Seguro.
Proporciona funciones para mostrar menús y manejar la entrada del usuario.
"""

import os
import platform
from colorama import Fore, Style

def clear_screen():
    """Limpia la pantalla de la consola según el sistema operativo"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header(title):
    """Imprime un encabezado con formato para las pantallas del gestor"""
    width = 60
    print(f"{Fore.CYAN}+" + "-" * width + "+")
    print(f"{Fore.CYAN}|" + " " * ((width - len(title)) // 2) + f"{Fore.WHITE}{Style.BRIGHT}{title}" + 
          " " * ((width - len(title) + 1) // 2) + f"{Fore.CYAN}|")
    print(f"{Fore.CYAN}+" + "-" * width + "+")

def print_menu(options):
    """Imprime un menú con opciones numeradas"""
    for i, option in enumerate(options, 1):
        print(f"{Fore.YELLOW}[{i}] {Fore.WHITE}{option}")

def get_input(prompt, valid_range=None):
    """
    Solicita entrada al usuario y valida que sea un número dentro del rango especificado.
    
    Args:
        prompt (str): Mensaje a mostrar al usuario
        valid_range (range, opcional): Rango de valores válidos
        
    Returns:
        int: Opción seleccionada por el usuario
    """
    while True:
        try:
            value = input(prompt)
            option = int(value)
            
            if valid_range is None or option in valid_range:
                return option
            else:
                print(f"{Fore.RED}Opción no válida. Intente nuevamente.")
        except ValueError:
            print(f"{Fore.RED}Por favor, ingrese un número válido.")

def print_table(headers, data):
    """
    Imprime una tabla con formato para mostrar datos.
    
    Args:
        headers (list): Lista de encabezados de columna
        data (list): Lista de filas, donde cada fila es una lista de valores
    """
    # Determinar el ancho de cada columna
    col_widths = [len(h) for h in headers]
    
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Imprimir encabezados
    header_row = ""
    for i, header in enumerate(headers):
        header_row += f"{header:<{col_widths[i] + 2}}"
    print(f"{Fore.YELLOW}{header_row}")
    
    # Imprimir línea separadora
    separator = ""
    for width in col_widths:
        separator += "-" * (width + 2)
    print(separator)
    
    # Imprimir datos
    for row in data:
        row_str = ""
        for i, cell in enumerate(row):
            row_str += f"{str(cell):<{col_widths[i] + 2}}"
        print(row_str)

def print_password_details(service, username, password, date):
    """
    Imprime los detalles de una contraseña con formato.
    
    Args:
        service (str): Nombre del servicio
        username (str): Nombre de usuario o correo
        password (str): Contraseña
        date (str): Fecha de creación
    """
    print(f"{Fore.YELLOW}Servicio: {Fore.WHITE}{service}")
    print(f"{Fore.YELLOW}Usuario: {Fore.WHITE}{username}")
    print(f"{Fore.YELLOW}Contraseña: {Fore.WHITE}{password}")
    print(f"{Fore.YELLOW}Fecha de creación: {Fore.WHITE}{date}")
