from PyPDF2 import PdfReader
import re

def limpiar_objeto(obj):
    for key in obj:
        if isinstance(obj[key], dict):
            limpiar_objeto(obj[key])
        else:
            obj[key] = obj[key].replace('\n', ' ').strip()
    return obj

def limpiar_nombre(nombre):
    nombre_limpio = nombre.replace('TERCERO DAÑOS A', ' ')
    nombre_limpio = nombre_limpio.replace('ASEGURADO DAÑOS A', ' ')
    return nombre_limpio.strip()

def limpiar_dni(dni):
    # elimar los primeros 6 digitos
    dni_limpio = dni[6:]
    return dni_limpio
def limpiar_dni_tercero(dni):
    dni_limpio = dni[5:]
    return dni_limpio

def extraer_texto(archivo_pdf):
    # Abre el archivo en modo lectura binaria
    with open(archivo_pdf, 'rb') as archivo:
        # Crea un objeto PdfReader
        lector_pdf = PdfReader(archivo)
        # Inicializa una cadena vacía para almacenar el texto
        texto = ''
        # Itera sobre todas las páginas del PDF
        for pagina in lector_pdf.pages:
            # Obtiene el texto de la página
            texto += pagina.extract_text()
        data = {
            'Denuncia de Siniestro': '',
            'Referencia': '',
            'Detalle del Lugar': '',
            'Descripción y consecuencias del siniestro': '',
            'Asegurado': {
                'Nombre': '',
                'DNI': '',
                'Teléfono': '',
                'Correo': '',
                'Marca': '',
                'Patente': '',
            },
            'Tercero': {
                'Nombre': '',
                'DNI': '',
                'Teléfono': '',
                'Correo': '',
                'Marca': '',
                'Patente': '',
            },
        }
        match = re.search(r'(Denuncia de Siniestros:)\n([\d]+)\n([\s\S]+?)(?=\nReferencia:)[\s\S]*?(?:Referencia:)\n*([\d]*)\n([\s\S]+?)(?=\nDetalle del Lugar:)[\s\S]*?(?:Detalle del Lugar:)\n([\w\d\s\(\)]+)\n([\s\S]+?)(?=\nDescripción y consecuencias del siniestro:)[\s\S]*?(?:Descripción y consecuencias del siniestro:)\s\n?([\s\n\w\íáó\.]*)\n(?:Comentario del Denunciante:)[\s\S]*?', texto)
        if match:
            data['Denuncia de Siniestro'] = match.group(2)
            data['Referencia'] = match.group(4)
            data['Detalle del Lugar'] = match.group(6)
            data['Descripción y consecuencias del siniestro'] = match.group(8)

        match = re.search(r'(DETALLE DE VEHÍCULO ASEGURADO)\n([\s\S]+?)(?=\nMarca\/Modelo:)[\s\S]*?(?:Marca\/Modelo:)\n([\d\w\/\.\s]+)\n([\s\S]+?)(?=\nPatente:)[\s\S]*?(?:Patente:)\n([\d\w]+)', texto)
        if match:
            data['Asegurado']['Marca'] = match.group(3)
            data['Asegurado']['Patente'] = match.group(5)
        match = re.search(r'(IDENTIFICACIÓN Y DOMICILIO DEL ASEGURADO)\n([\s\S]+?)(?=\nLocalidad:)[\s\S]*?(?:Localidad:)\n([\w\d]+)\n([\w\ó\é\í\ú\ñ]*\s[\w\ó\é\í\ú\ñ]*\s[\w\ó\é\í\ú\ñ]*)\n([\s\S]+?)(?=\nTeléfono:)[\s\S]*?(?:\nTeléfono:([\+\d\s]*))?\n', texto)
        if match:
            data['Asegurado']['Nombre'] = match.group(4)
            data['Asegurado']['DNI'] = match.group(3)
            data['Asegurado']['Teléfono'] = match.group(6)
        caso_num = input('Ingrese el número de caso: ')
        match = re.search(r'(RECLAMO:\n'+caso_num+'-)\s?([\w\d\s\ñ\í\ó\ú\á]+)\n([\s\S]+?)(?=\nDNI)[\s\S]*?(?:CUIT\/CUI |CUIT|CUIL|DNI)\n([\d]*)\n([\s\S]+?)(?=\nMarca\/Modelo:)\n(?:Marca\/Modelo:)\n([\w\s\d\.\/]+)\n([\s\S]+?)(?=\nPatente:)\n(?:Patente:)\n([\d\w]+)\n([\s\S]+?)(?=\nEmail:)[\s\S]*?(?:\nEmail:\n([\w\s\@\.\d\ñ]*))(Teléfono:)\n([\+\d]*)\n', texto)
        if match:
            data['Tercero']['Nombre'] = match.group(2)
            data['Tercero']['DNI'] = match.group(4)
            data['Tercero']['Marca'] = match.group(6)
            data['Tercero']['Patente'] = match.group(8)
            data['Tercero']['Correo'] = match.group(10)
            data['Tercero']['Teléfono'] = match.group(12)
        limpiar_objeto(data)
        nombre_clean = limpiar_nombre(data['Tercero']['Nombre'])
        data['Tercero']['Nombre'] = nombre_clean

        dni_clean = limpiar_dni_tercero(data['Tercero']['DNI'])
        data['Tercero']['DNI'] = dni_clean

        dni = limpiar_dni(data['Asegurado']['DNI'])
        data['Asegurado']['DNI'] = dni

        return data

if __name__ == '__main__':
    data = extraer_texto('denuncia.pdf')
    

