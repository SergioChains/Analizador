import re
import tkinter as tk
from tkinter import filedialog
from pylint import lint


# Definición de diccionarios para categorías léxicas
operators = {'=': 'Igual op', '+': 'Suma op', '-': 'Resta op', '/': 'Division op', '*': 'Multiplicacion op', '%': 'Modulo op'}
logics = {'<': 'Menor que', '>': 'Mayor que',  '>=': 'Mayor o igual que',  '<=': 'Menor o igual que', '&&': 'AND', '||': 'OR', '!=': 'Diferente'}
data_type = {'usE': 'Entero', 'usD': 'Decimal', 'usCh': 'Caracter', 'long': 'largo'}
punctuation_symbol = {':': '2 Puntos', ';': 'Punto y coma', '.': 'Punto', ',': 'Coma' , '""': 'Comillas', '@': 'Arroba', '$': 'Concatena', '()': 'Parentesis', '{}': 'Llaves', '[]': 'Corchetes' , '<>': 'Encapsula'}
identifier = {'a': 'caracter', 'b': 'caracter', 'c': 'caracter', 'd': 'caracter'}
letras = {'a, b, c, d, e, f, g, h' : 'Letras minusculas', 'A...Z' : 'Letras mayusculas'}
numeros = {'0' : 'Numero','1' : 'Numero','2' : 'Numero','3' : 'Numero','4' : 'Numero','5' : 'Numero','6' : 'Numero','7' : 'Numero','8' : 'Numero','9' : 'Numero'}
InicioPrograma={'Program' : 'Inicio de Programa'}
AperturaPrograma = {'++[' : 'Apertura del programa e inicio de zona de variables'}
CierrePrograma = {']--' : 'Cierre del programa'}
AperturaCuerpoP = {'Main+[' : 'Apertura del cuerpo del programa y cierre de zona de variables'}
CierreCuerpoP= {']-' : 'Cierre del cuerpo del programa'}
 
def check_program_structure(content):
    errors = []
    lines = content.split("\n")

    # Verificar inicio y fin del programa
    if not lines[0].startswith('Program'):
        errors.append("La primera línea no contiene la palabra clave 'Program'.")
    if not lines[-1].strip().endswith(']--'):
        errors.append("La última línea no contiene el cierre correcto ']--'.")

    # Verificar la sección de variables
    variables_section = False
    for i, line in enumerate(lines):
        if '++[' in line:
            if variables_section:  # Se encontró una segunda sección de variables
                errors.append(f"Se encontró una segunda sección de variables en la línea {i + 1}.")
            variables_section = True
        elif 'Main+[' in line:
            if not variables_section:  # Se cierra la sección de variables sin haber sido abierta
                errors.append(f"Se encontró un cierre de sección de variables sin apertura en la línea {i + 1}.")
            variables_section = False

    if variables_section:  # No se encontró cierre para la sección de variables
        errors.append("No se encontró un cierre para la sección de variables.")

def check_main_section(lines):
    errors = []
    main_section_started = False
    main_section_closed = False

    for i, line in enumerate(lines):
        # Verificar el inicio de la sección Main
        if 'Main +[' in line:
            if main_section_started:
                # Error si ya se había iniciado una sección Main
                errors.append(f"Error: Se encontró una segunda apertura de 'Main' en la línea {i + 1}.")
            else:
                main_section_started = True
        
        # Verificar el cierre de la sección Main
        elif ']-' in line and main_section_started:
            main_section_closed = True
            break  # No se necesitan más verificaciones una vez que Main se cierra

    # Verificar si la sección Main fue abierta pero no cerrada
    if main_section_started and not main_section_closed:
        errors.append("Error: No se encontró un cierre para la función principal 'Main'.")

    # Verificar si la sección Main fue cerrada pero no abierta
    if not main_section_started and main_section_closed:
        errors.append("Error: Se encontró un cierre de 'Main' sin una apertura previa.")

    return errors

# Función para eliminar comentarios del contenido
def remove_comments(content):
    content = re.sub(r'#.*', '', content)  # Elimina comentarios de una línea
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Elimina comentarios de bloques
    return content

# Modificada para recolectar y retornar errores
def check_characters(content):
    valid_pattern = re.compile(r'^[a-zA-Z0-9\s\+\-\*/=%<>&|\[\]\{\}\(\),;:.!@#$^]+$')
    errors = []
    for line_number, line in enumerate(content.split("\n"), start=1):
        if not valid_pattern.match(line):
            for character in line:
                if not valid_pattern.match(character):
                    errors.append((line_number, character))
    return errors

# Obtiene las claves de los diccionarios
operators_key = operators.keys()
logics_key = logics.keys()
data_type_key = data_type.keys()
punctuation_symbol_key = punctuation_symbol.keys()
identifier_key = identifier.keys()
letras_key = letras.keys()
numeros_key = numeros.keys()
inicio_key = InicioPrograma.keys()
apertura_key = AperturaPrograma.keys()
cierre_key  = CierrePrograma.keys()
aperturaP_key = AperturaCuerpoP.keys()
cierreP_key = CierreCuerpoP.keys()


# Nombre del archivo .txt a analizar
file_name = "Codigo.txt"

try:
    # Abre el archivo .txt para lectura
    with open(file_name, 'r') as file:
        # Lee el contenido del archivo
        content = file.read()

        # Divide el contenido en líneas
        program = content.split("\n")

        # Inicializa un contador para el número de líneas
        count = 0

        # Recorre cada línea del programa
        for line in program:
            count += 1
            print("line#", count, "\n", line)

            # Divide la línea en tokens (separados por espacios en blanco)
            tokens = re.findall(r'\S+|\s+', line)
            tokens = [token.strip() for token in tokens if token.strip()]  # Filtra los tokens no vacíos
            print("Tokens are", tokens)
            print("Line#", count, "propiedades: \n")

            # Procesa cada token
            for token in tokens:
                if token in operators_key:
                    print("El operator es:", operators[token])
                if token in logics_key:
                    print("El operador es:", logics[token])
                if token in data_type_key:
                    print("El tipo de dato es:", data_type[token])
                if token in punctuation_symbol_key:
                    print(token, "Simbolo de puntuacion:", punctuation_symbol[token])
                if token in identifier_key:
                    print(token, "Variable:", identifier[token])
                if token in letras_key:
                    print(token, "el dato es:", letras[token])
                if token in numeros_key:
                    print(token, "el dato es:", numeros[token])
                if token in inicio_key:
                    print(token, "Esto es: ", InicioPrograma[token]) 
                if token in apertura_key:
                    print(token, "Esto es: ", AperturaPrograma[token]) 
                if token in cierre_key:
                    print(token, "Esto es: ", CierrePrograma[token]) 
                if token in aperturaP_key:
                    print(token, "Esto es: ", AperturaCuerpoP[token]) 
                if token in cierreP_key:
                    print(token, "Esto es: ", CierreCuerpoP[token])                 
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _")

except FileNotFoundError:
    print(f"El archivo '{file_name}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

def analyze_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
            # Elimina comentarios
            content = remove_comments(content)
            
            # Llama a la función de verificación de caracteres
            errors = check_characters(content)
            if errors:
                for line_number, character in errors:
                    output_text.insert(tk.END, f"Error: Carácter no válido '{character}' encontrado en la línea {line_number}.\n")
            else:
                output_text.insert(tk.END, "No se encontraron caracteres no válidos.\n")

 # Llama a la función de verificación de estructura de programa
            structure_errors = check_program_structure(content)
            if structure_errors:
                for error in structure_errors:
                    output_text.insert(tk.END, f"Error de estructura: {error}\n")
            else:
                output_text.insert(tk.END, "La estructura del programa es válida.\n")


            # Procede con el análisis a pesar de los errores
            program = content.split("\n")
            count = 0

            for line in program:
                count += 1
                output_text.insert(tk.END, f"line#{count}\n{line}\n")

                tokens = re.findall(r'\S+|\s+', line)
                tokens = [token.strip() for token in tokens if token.strip()]

                output_text.insert(tk.END, f"Tokens are {tokens}\n")
                output_text.insert(tk.END, f"Line#{count} propiedades\n")

                for token in tokens:
                    if token in operators_key:
                        output_text.insert(tk.END, f"El operador es: {operators[token]}\n")
                    if token in logics_key:
                        output_text.insert(tk.END, f"El operador es: {logics[token]}\n")
                    if token in data_type_key:
                        output_text.insert(tk.END, f"----Zona de variables---- \nEl tipo de dato es: {data_type[token]}\n")
                    if token in punctuation_symbol_key:
                        output_text.insert(tk.END, f"{token} Simbolo de puntuacion:  {punctuation_symbol[token]}\n")
                    if token in identifier_key:
                        output_text.insert(tk.END, f"{token} Es un: {identifier[token]}\n")
                    if token in letras_key:
                        output_text.insert(tk.END, f"{token} Dato alfabetico: {letras[token]}\n")
                    if token in numeros_key:
                        output_text.insert(tk.END, f"{token} es un: {numeros[token]}\n")
                    if token in inicio_key:
                        output_text.insert(tk.END, f"{token} es: {InicioPrograma[token]}\n")
                    if token in apertura_key:
                        output_text.insert(tk.END, f"{token} es: {AperturaPrograma[token]}\n")
                    if token in cierre_key:
                        output_text.insert(tk.END, f"{token} es: {CierrePrograma[token]}\n")
                    if token in aperturaP_key:
                        output_text.insert(tk.END, f"{token} es: {AperturaCuerpoP[token]}\n")
                    if token in cierreP_key:
                        output_text.insert(tk.END, f"{token} es: {CierreCuerpoP[token]}\n")                
                         

                output_text.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")

            # Verificar errores con pylint
            pylint_stdout, pylint_stderr = lint.py_run([file_path], return_std=True)
            output_text.insert(tk.END, "\nPyLint Output:\n")
            output_text.insert(tk.END, pylint_stdout.getvalue())
            output_text.insert(tk.END, "\nPyLint Errors:\n")
            output_text.insert(tk.END, pylint_stderr.getvalue())

    except FileNotFoundError:
        output_text.insert(tk.END, f"El archivo '{file_path}' no se encontró.\n")
    except Exception as e:
        output_text.insert(tk.END, f"Ocurrió un error: {e}\n")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        analyze_file(file_path)

def setup_gui():
    root = tk.Tk()
    root.title("Analizador de CodeChains")
    open_button = tk.Button(root, text="Abrir Archivo", command=open_file)
    open_button.pack(pady=10)
    global output_text
    output_text = tk.Text(root, height=20, width=80)
    output_text.pack()
    return root

# Ejecución principal
if __name__ == "__main__":
    root = setup_gui()
    root.mainloop()