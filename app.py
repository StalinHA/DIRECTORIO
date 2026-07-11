import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import json
from pathlib import Path
import uuid
import io
import csv
import base64
from PIL import Image
import sqlite3
import hashlib

# Configuración de la página
st.set_page_config(
    page_title="Directorio de Contactos Profesional",
    page_icon="📇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados - Dark Futurista
st.markdown("""
<style>
    /* Importar fuente Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables de color */
    :root {
        --bg-primary: #0a0e14;
        --bg-secondary: #131820;
        --bg-tertiary: #1a1f2e;
        --bg-card: #1e2433;
        --border-color: #2a3040;
        --text-primary: #e4e8f0;
        --text-secondary: #a0a8b8;
        --accent-primary: #6366f1;
        --accent-secondary: #818cf8;
        --success: #10b981;
        --danger: #ef4444;
        --whatsapp: #25D366;
    }
    
    /* Estilos globales */
    .stApp {
        background: linear-gradient(135deg, #0a0e14 0%, #131820 100%);
    }
    
    .main .block-container {
        background: #131820;
        border-radius: 20px;
        border: 1px solid #2a3040;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        padding: 2rem;
    }
    
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #0a0e14 0%, #131820 100%);
        border-bottom: 1px solid #2a3040;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        opacity: 0.5;
    }
    
    .app-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #e4e8f0 0%, #a0a8b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Tarjetas de estadísticas */
    .stat-card {
        background: #1e2433;
        border: 1px solid #2a3040;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .stat-card:hover {
        border-color: #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #a0a8b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
    }
    
    /* Tarjetas de contacto */
    .contact-card {
        background: #1e2433;
        border: 1px solid #2a3040;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .contact-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .contact-card:hover {
        border-color: #3a4060;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transform: translateY(-4px);
    }
    
    .contact-card:hover::before {
        opacity: 1;
    }
    
    .contact-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e4e8f0;
    }
    
    .contact-position {
        font-size: 0.85rem;
        color: #818cf8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .contact-entity {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    /* Inputs personalizados */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: #1a1f2e;
        border: 1px solid #2a3040;
        color: #e4e8f0;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: #1a1f2e;
        border-right: 1px solid #2a3040;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #1a1f2e;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Dataframe */
    .dataframe {
        background: #1e2433;
        border: 1px solid #2a3040;
        border-radius: 8px;
    }
    
    .dataframe th {
        background: #1a1f2e;
        color: #818cf8;
        font-weight: 600;
    }
    
    .dataframe td {
        color: #a0a8b8;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1e2433;
        border: 1px solid #2a3040;
        border-radius: 8px;
        color: #e4e8f0;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #e4e8f0;
        font-weight: 700;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981;
    }
    
    /* WhatsApp button */
    .whatsapp-btn {
        background: #25D366;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .whatsapp-btn:hover {
        background: #20bd5a;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de la base de datos
def init_db():
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    
    # Tabla de grupos
    c.execute('''
        CREATE TABLE IF NOT EXISTS grupos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            tipo TEXT DEFAULT 'personalizado',
            color TEXT DEFAULT '#6366f1',
            fecha_creacion TEXT,
            creado_por TEXT
        )
    ''')
    
    # Tabla de contactos
    c.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id TEXT PRIMARY KEY,
            grupo_id TEXT,
            nombre TEXT NOT NULL,
            apellido TEXT,
            cargo TEXT,
            entidad TEXT,
            telefono TEXT NOT NULL,
            correos TEXT,
            comentario TEXT,
            estado TEXT DEFAULT 'activo',
            fecha_creacion TEXT,
            fecha_edicion TEXT,
            editado_por TEXT,
            FOREIGN KEY (grupo_id) REFERENCES grupos (id)
        )
    ''')
    
    # Tabla de historial inmutable
    c.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id TEXT PRIMARY KEY,
            contacto_id TEXT,
            tipo_evento TEXT,
            usuario TEXT,
            fecha_hora TEXT,
            descripcion TEXT,
            detalles TEXT,
            ip TEXT
        )
    ''')
    
    # Insertar grupos predefinidos si no existen
    c.execute('SELECT COUNT(*) FROM grupos')
    if c.fetchone()[0] == 0:
        grupos_default = [
            ('proveedores', 'Proveedores', 'predefinido', '#3B82F6'),
            ('publicas', 'Entidades Públicas', 'predefinido', '#10B981'),
            ('privadas', 'Entidades Privadas', 'predefinido', '#8B5CF6')
        ]
        for g in grupos_default:
            c.execute('''
                INSERT INTO grupos (id, nombre, tipo, color, fecha_creacion, creado_por)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (g[0], g[1], g[2], g[3], get_peru_datetime(), 'sistema'))
    
    conn.commit()
    conn.close()

def get_peru_datetime():
    """Obtener fecha y hora actual en zona horaria de Perú"""
    peru_tz = pytz.timezone('America/Lima')
    return datetime.now(peru_tz).strftime('%d/%m/%Y %H:%M:%S')

def generate_id():
    """Generar ID único"""
    return str(uuid.uuid4())

# Funciones CRUD
def add_group(nombre, color):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    group_id = generate_id()
    c.execute('''
        INSERT INTO grupos (id, nombre, tipo, color, fecha_creacion, creado_por)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group_id, nombre, 'personalizado', color, get_peru_datetime(), 'Administrador'))
    conn.commit()
    conn.close()
    return group_id

def get_groups():
    conn = sqlite3.connect('directorio.db')
    df = pd.read_sql_query('SELECT * FROM grupos ORDER BY tipo, nombre', conn)
    conn.close()
    return df

def add_contact(contact_data):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    contact_id = generate_id()
    fecha = get_peru_datetime()
    
    c.execute('''
        INSERT INTO contactos (id, grupo_id, nombre, apellido, cargo, entidad, 
                              telefono, correos, comentario, estado, fecha_creacion, 
                              fecha_edicion, editado_por)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        contact_id,
        contact_data.get('grupo_id'),
        contact_data['nombre'],
        contact_data.get('apellido', ''),
        contact_data.get('cargo', ''),
        contact_data.get('entidad', ''),
        contact_data['telefono'],
        json.dumps(contact_data.get('correos', [])),
        contact_data.get('comentario', ''),
        'activo',
        fecha,
        fecha,
        'Administrador'
    ))
    
    # Registrar en historial
    add_history(contact_id, 'CREACION', 'Administrador', 
                f'Contacto "{contact_data["nombre"]} {contact_data.get("apellido", "")}" creado',
                json.dumps(contact_data))
    
    conn.commit()
    conn.close()
    return contact_id

def update_contact(contact_id, contact_data):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    fecha = get_peru_datetime()
    
    c.execute('''
        UPDATE contactos 
        SET grupo_id = ?, nombre = ?, apellido = ?, cargo = ?, entidad = ?,
            telefono = ?, correos = ?, comentario = ?, fecha_edicion = ?, editado_por = ?
        WHERE id = ?
    ''', (
        contact_data.get('grupo_id'),
        contact_data['nombre'],
        contact_data.get('apellido', ''),
        contact_data.get('cargo', ''),
        contact_data.get('entidad', ''),
        contact_data['telefono'],
        json.dumps(contact_data.get('correos', [])),
        contact_data.get('comentario', ''),
        fecha,
        'Administrador',
        contact_id
    ))
    
    add_history(contact_id, 'EDICION', 'Administrador', 
                f'Contacto actualizado', json.dumps(contact_data))
    
    conn.commit()
    conn.close()

def soft_delete_contact(contact_id):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    fecha = get_peru_datetime()
    
    c.execute('UPDATE contactos SET estado = ?, fecha_edicion = ? WHERE id = ?',
              ('eliminado', fecha, contact_id))
    
    add_history(contact_id, 'ELIMINACION', 'Administrador', 
                'Contacto marcado como eliminado (soft delete)', '{}')
    
    conn.commit()
    conn.close()

def restore_contact(contact_id):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    fecha = get_peru_datetime()
    
    c.execute('UPDATE contactos SET estado = ?, fecha_edicion = ? WHERE id = ?',
              ('activo', fecha, contact_id))
    
    add_history(contact_id, 'RESTAURACION', 'Administrador', 
                'Contacto restaurado', '{}')
    
    conn.commit()
    conn.close()

def add_history(contact_id, tipo, usuario, descripcion, detalles):
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO historial (id, contacto_id, tipo_evento, usuario, fecha_hora, 
                              descripcion, detalles, ip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (generate_id(), contact_id, tipo, usuario, get_peru_datetime(), 
          descripcion, detalles, '127.0.0.1'))
    
    conn.commit()
    conn.close()

def get_contacts(grupo_id=None, show_deleted=False):
    conn = sqlite3.connect('directorio.db')
    
    query = 'SELECT * FROM contactos'
    conditions = []
    
    if not show_deleted:
        conditions.append("estado = 'activo'")
    
    if grupo_id:
        conditions.append(f"grupo_id = '{grupo_id}'")
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY fecha_creacion DESC'
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_history(contacto_id=None):
    conn = sqlite3.connect('directorio.db')
    if contacto_id:
        df = pd.read_sql_query(
            'SELECT * FROM historial WHERE contacto_id = ? ORDER BY fecha_hora DESC',
            conn, params=(contacto_id,))
    else:
        df = pd.read_sql_query('SELECT * FROM historial ORDER BY fecha_hora DESC', conn)
    conn.close()
    return df

def get_stats():
    conn = sqlite3.connect('directorio.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM contactos WHERE estado = 'activo'")
    activos = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM contactos WHERE estado = 'eliminado'")
    eliminados = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM grupos")
    grupos = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM historial")
    historial = c.fetchone()[0]
    
    conn.close()
    return {'activos': activos, 'eliminados': eliminados, 'grupos': grupos, 'historial': historial}

def export_history_csv():
    df = get_history()
    if df.empty:
        return None
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Inicializar base de datos
init_db()

# Header principal
st.markdown("""
<div class="app-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                    border-radius: 12px; display: flex; align-items: center; justify-content: center;
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);">
            <span style="color: white; font-size: 1.5rem; font-weight: 700;">D</span>
        </div>
        <h1 class="app-title">Directorio de Contactos Profesional</h1>
    </div>
    <p style="color: #6b7280; margin-top: 0.5rem;">Sistema de Gestión de Contactos - Zona Horaria: Lima, Perú (UTC-5)</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h3 style="color: #818cf8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px;">
            Navegación
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar grupos
    grupos_df = get_groups()
    
    view_option = st.radio(
        "Seleccionar Grupo",
        ["Todos los Contactos"] + grupos_df['nombre'].tolist(),
        key="group_selector"
    )
    
    # Determinar grupo seleccionado
    selected_group_id = None
    if view_option != "Todos los Contactos":
        selected_group = grupos_df[grupos_df['nombre'] == view_option]
        if not selected_group.empty:
            selected_group_id = selected_group.iloc[0]['id']
    
    st.markdown("---")
    
    # Opciones adicionales
    show_deleted = st.checkbox("Mostrar contactos eliminados", key="show_deleted")
    
    st.markdown("---")
    
    # Agregar nuevo grupo
    st.markdown("<h4 style='color: #818cf8;'>Nuevo Grupo</h4>", unsafe_allow_html=True)
    with st.form("add_group_form"):
        new_group_name = st.text_input("Nombre del Grupo")
        new_group_color = st.color_picker("Color", "#6366f1")
        if st.form_submit_button("Crear Grupo"):
            if new_group_name:
                add_group(new_group_name, new_group_color)
                st.success("Grupo creado exitosamente")
                st.rerun()
            else:
                st.error("Ingrese un nombre para el grupo")

# Contenido principal
col1, col2, col3, col4 = st.columns(4)

stats = get_stats()

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['activos']}</div>
        <div class="stat-label">Contactos Activos</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['grupos']}</div>
        <div class="stat-label">Grupos</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['historial']}</div>
        <div class="stat-label">Eventos Registrados</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{stats['eliminados']}</div>
        <div class="stat-label">Eliminados</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Búsqueda
search_term = st.text_input("", placeholder="Buscar contactos por nombre, cargo, entidad, teléfono...", key="search")

# Acciones principales
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown(f"### {view_option}")
with col2:
    if st.button("Nuevo Contacto", key="add_contact_btn"):
        st.session_state.show_add_contact = True
with col3:
    if st.button("Exportar Historial CSV", key="export_btn"):
        csv_data = export_history_csv()
        if csv_data:
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="historial_directorio.csv" class="whatsapp-btn">Descargar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("No hay datos para exportar")

st.markdown("---")

# Modal para agregar/editar contacto
if 'show_add_contact' in st.session_state and st.session_state.show_add_contact:
    with st.expander("Nuevo Contacto", expanded=True):
        with st.form("contact_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre *")
                cargo = st.text_input("Cargo")
                telefono = st.text_input("WhatsApp * (+51 999 888 777)")
                grupo = st.selectbox("Grupo", ["Sin grupo"] + grupos_df['nombre'].tolist())
            
            with col2:
                apellido = st.text_input("Apellido (opcional)")
                entidad = st.text_input("Entidad / Empresa")
                correo1 = st.text_input("Correo Principal")
                correo2 = st.text_input("Correo Secundario")
            
            comentario = st.text_area("Comentario", placeholder="Notas adicionales...")
            
            submitted = st.form_submit_button("Guardar Contacto")
            
            if submitted:
                if not nombre or not telefono:
                    st.error("Nombre y WhatsApp son obligatorios")
                else:
                    grupo_id = None
                    if grupo != "Sin grupo":
                        grupo_selected = grupos_df[grupos_df['nombre'] == grupo]
                        if not grupo_selected.empty:
                            grupo_id = grupo_selected.iloc[0]['id']
                    
                    correos = []
                    if correo1:
                        correos.append(correo1)
                    if correo2:
                        correos.append(correo2)
                    
                    contact_data = {
                        'grupo_id': grupo_id,
                        'nombre': nombre,
                        'apellido': apellido,
                        'cargo': cargo,
                        'entidad': entidad,
                        'telefono': telefono,
                        'correos': correos,
                        'comentario': comentario
                    }
                    
                    if 'edit_contact_id' in st.session_state:
                        update_contact(st.session_state.edit_contact_id, contact_data)
                        del st.session_state.edit_contact_id
                        st.success("Contacto actualizado exitosamente")
                    else:
                        add_contact(contact_data)
                        st.success("Contacto creado exitosamente")
                    
                    st.session_state.show_add_contact = False
                    st.rerun()

# Mostrar contactos
contacts_df = get_contacts(selected_group_id, show_deleted)

if not contacts_df.empty:
    # Filtrar por búsqueda
    if search_term:
        mask = (
            contacts_df['nombre'].str.contains(search_term, case=False, na=False) |
            contacts_df['apellido'].str.contains(search_term, case=False, na=False) |
            contacts_df['cargo'].str.contains(search_term, case=False, na=False) |
            contacts_df['entidad'].str.contains(search_term, case=False, na=False) |
            contacts_df['telefono'].str.contains(search_term, case=False, na=False)
        )
        contacts_df = contacts_df[mask]
    
    if contacts_df.empty:
        st.info("No se encontraron contactos con los criterios de búsqueda")
    else:
        for _, contact in contacts_df.iterrows():
            is_deleted = contact['estado'] == 'eliminado'
            
            # Obtener correos
            try:
                correos = json.loads(contact['correos']) if contact['correos'] else []
            except:
                correos = []
            
            # Card de contacto
            card_style = "border: 1px solid #ef4444;" if is_deleted else ""
            
            st.markdown(f"""
            <div class="contact-card" style="{card_style}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="display: flex; gap: 1rem;">
                        <div style="width: 48px; height: 48px; border-radius: 12px; 
                                  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                                  display: flex; align-items: center; justify-content: center;
                                  color: white; font-weight: 600; font-size: 1.2rem;">
                            {contact['nombre'][0].upper()}{contact['apellido'][0].upper() if contact['apellido'] else ''}
                        </div>
                        <div>
                            <div class="contact-name">
                                {contact['nombre']} {contact['apellido'] if contact['apellido'] else ''}
                                {'<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; margin-left: 8px;">Eliminado</span>' if is_deleted else ''}
                            </div>
                            <div class="contact-position">{contact['cargo'] if contact['cargo'] else 'Sin cargo'}</div>
                            <div class="contact-entity">{contact['entidad'] if contact['entidad'] else 'Sin entidad'}</div>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #2a3040;">
                    <div style="color: #a0a8b8; font-size: 0.9rem; margin-bottom: 0.5rem;">
                        Tel: {contact['telefono']}
                    </div>
                    {f'<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 0.5rem;">Correos: {", ".join(correos)}</div>' if correos else ''}
                    {f'<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 0.5rem;">Nota: {contact["comentario"]}</div>' if contact['comentario'] else ''}
                    <div style="color: #6b7280; font-size: 0.7rem; margin-top: 0.5rem;">
                        Creado: {contact['fecha_creacion']} (Lima, Perú)
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botones de acción
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if not is_deleted:
                    clean_phone = ''.join(filter(str.isdigit, str(contact['telefono'])))
                    whatsapp_url = f"https://wa.me/{clean_phone}"
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">WhatsApp</a>', 
                              unsafe_allow_html=True)
            
            with col2:
                if st.button("Editar", key=f"edit_{contact['id']}"):
                    st.session_state.show_add_contact = True
                    st.session_state.edit_contact_id = contact['id']
                    # Pre-llenar formulario
                    st.session_state.edit_nombre = contact['nombre']
                    st.session_state.edit_apellido = contact['apellido']
                    st.rerun()
            
            with col3:
                if not is_deleted:
                    if st.button("Eliminar", key=f"delete_{contact['id']}"):
                        soft_delete_contact(contact['id'])
                        st.rerun()
                else:
                    if st.button("Restaurar", key=f"restore_{contact['id']}"):
                        restore_contact(contact['id'])
                        st.rerun()
            
            with col4:
                if st.button("Historial", key=f"history_{contact['id']}"):
                    st.session_state.show_history = contact['id']
                    st.rerun()
            
            # Mostrar historial
            if 'show_history' in st.session_state and st.session_state.show_history == contact['id']:
                st.markdown("---")
                st.markdown("#### Historial de Eventos (Inmutable)")
                
                history_df = get_history(contact['id'])
                if not history_df.empty:
                    for _, event in history_df.iterrows():
                        dot_color = {
                            'CREACION': '#10b981',
                            'EDICION': '#6366f1',
                            'ELIMINACION': '#ef4444',
                            'RESTAURACION': '#10b981'
                        }.get(event['tipo_evento'], '#6366f1')
                        
                        st.markdown(f"""
                        <div style="padding: 0.5rem; border-bottom: 1px solid #2a3040; margin-bottom: 0.5rem;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: {dot_color}; 
                                          box-shadow: 0 0 10px {dot_color};"></div>
                                <strong style="color: #a0a8b8;">{event['tipo_evento']}</strong>
                                <span style="color: #6b7280; font-size: 0.7rem;">{event['fecha_hora']}</span>
                            </div>
                            <div style="color: #6b7280; font-size: 0.8rem; margin-left: 1rem;">
                                {event['descripcion']}
                            </div>
                            <div style="color: #6b7280; font-size: 0.6rem; margin-left: 1rem;">
                                Usuario: {event['usuario']} | IP: {event['ip']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No hay eventos registrados")
                
                if st.button("Cerrar Historial", key=f"close_history_{contact['id']}"):
                    del st.session_state.show_history
                    st.rerun()
            
            st.markdown("---")
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #6b7280;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">No hay contactos registrados</div>
        <p>Cree un nuevo contacto utilizando el botón "Nuevo Contacto"</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
    <p>Sistema de Directorio de Contactos v2.0 | Zona Horaria: America/Lima (UTC-5) | Última actualización: {get_peru_datetime()}</p>
    <p>Historial inmutable activado | Soft delete habilitado</p>
</div>
""", unsafe_allow_html=True)