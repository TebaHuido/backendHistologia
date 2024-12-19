import pandas as pd
from .models import Alumno, Curso, CustomUser
from io import BytesIO

def create_alumnos_from_xls(file):
    try:
        # Read the file content into a BytesIO object
        file_content = BytesIO(file.read())
        
        # Debugging: Print the first few bytes of the file content
        print("First few bytes of the file content:", file_content.getvalue()[:100])
        
        # Specify the engine based on the file extension and skip the first row
        if file.name.endswith('.xls'):
            df = pd.read_excel(file_content, engine='xlrd', skiprows=1)
        else:
            df = pd.read_excel(file_content, engine='openpyxl', skiprows=1)
        
        # Debugging: Print the columns of the DataFrame
        print("Columns in the uploaded file:", df.columns)
        
        # Check if the required columns are present
        required_columns = ['RUT', 'NOMBRE', 'CARRERA', 'EMAIL']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Missing required column: {column}")
    except Exception as e:
        raise ValueError(f"Error reading the Excel file: {e}")

    created_alumnos = []
    existing_alumnos = []
    curso_name = None
    curso_created = False

    for _, row in df.iterrows():
        curso_name = row['CARRERA']
        curso, created = Curso.objects.get_or_create(asignatura=curso_name, anio=2024, semestre=True, grupo='A')
        if created:
            curso_created = True
        
        user, created = CustomUser.objects.get_or_create(
            username=row['RUT'],
            defaults={
                'email': row['EMAIL'],
                'is_profesor': False,
                'is_alumno': True,
                'password': 'defaultpassword'  # Set a default password or handle password setting securely
            }
        )
        
        alumno, created = Alumno.objects.get_or_create(
            user=user,
            defaults={
                'name': row['NOMBRE'],
            }
        )
        alumno.curso.add(curso)
        
        if created:
            created_alumnos.append(alumno.name)
        else:
            existing_alumnos.append(alumno.name)

    return {
        "curso": curso_name,
        "curso_created": curso_created,
        "created_alumnos": created_alumnos,
        "existing_alumnos": existing_alumnos
    }