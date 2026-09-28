import streamlit as st
import random
import string

# Configuración de página
st.set_page_config(
    page_title="Ubuntu: Cartas de Conexión",
    page_icon="🧩",
    layout="centered"
)

# -----------------------------------------------------------------------------
# MEMORIA COMPARTIDA ENTRE JUGADORES (SALAS GLOBALES)
# -----------------------------------------------------------------------------
@st.cache_resource
def obtener_base_datos_salas():
    return {}

BD_SALAS = obtener_base_datos_salas()

# -----------------------------------------------------------------------------
# DICCIONARIO BASE DE PREGUNTAS
# -----------------------------------------------------------------------------
PREGUNTAS_BASE = {
    "PENSAMIENTOS": [
        "En este último tiempo, ¿qué me ha estado dando vueltas constantemente en la cabeza, o me ha quitado un poco el sueño?",
        "Si no necesitara un sueldo, ¿a qué dedicaría mi tiempo?",
        "Si tuviera que definir esta etapa de mi vida en tres palabras, ¿cuáles serían y por qué?",
        "¿Hay algo que tendría que 'soltar' para ser más feliz en el presente?",
        "Si me quedaran pocos años de vida, ¿qué cosas haría diferente a partir de este momento?",
        "¿En qué área de mi vida quisiera desarrollarme más? ¿Por qué?",
        "¿Qué quisiera hacer de manera diferente en mi vida y qué me aportaría hacerlo?",
        "¿Considero que tengo algún propósito de vida en este momento? ¿Siento que estoy viviendo de acuerdo a él?",
        "¿Con qué piedra tropiezo constantemente?",
        "¿Cómo me imagino en 5 años más? Considera las diferentes áreas de tu vida.",
        "¿Cuál ha sido mi mayor cambio personal en el último tiempo?",
        "Si tuviera una máquina para volver el tiempo atrás, ¿cambiaría algo de mi historia? ¿Por qué?",
        "¿Cuáles son los tres sueños que me gustaría cumplir, aunque parezcan fantasía o muy lejanos?",
        "¿Qué importancia tiene en mi vida la dimensión espiritual? ¿La cultivo de alguna manera?"
    ],
    "CONEXIONES": [
        "¿Quién es la persona que más ha influido en mi modo de ver la vida? ¿Por qué?",
        "¿Qué cualidad de algún familiar me gustaría tener? ¿Por qué?",
        "¿Qué considero que valoran más de mí mis seres queridos?",
        "¿Quiénes considero que son luz para mí en este momento de mi vida?",
        "¿Cuáles son las tres características que más valoro en un amigo/a? ¿Por qué?",
        "¿A qué relación quisiera dedicarle más tiempo en este momento de mi vida? Cuenta un poco por qué.",
        "¿Qué es lo más significativo que he hecho por alguien?",
        "¿Qué es lo que más me llama la atención en una persona? (Atractivo exterior e interior)",
        "¿Cuál ha sido la aventura que más he disfrutado con amigos/as? Cuenta cómo fue.",
        "¿Cuál es la primera impresión que creo que la gente saca de mí? ¿Qué de eso no es cierto?",
        "¿Cuál creo que es la mejor manera para solucionar una diferencia con alguien?",
        "¿Hay algo que sería incapaz de perdonar? ¿Qué y por qué?",
        "Tres características y/o costumbres de mi familia de origen que me gustan y que quisiera mantener. Una que no me gusta y que quisiera mejorar es...",
        "¿Siento que tenga alguna conversación pendiente con alguien? ¿Qué podría hacer para tenerla?",
        "¿A qué persona de mi vida admiro mucho y por qué?"
    ],
    "EMOCIONES": [
        "¿Cuáles son mis mayores miedos en la vida?",
        "¿Qué me ayuda a encontrar la calma en esos momentos en los que la pierdo?",
        "¿Qué recuerdos me hacen sonreír instantáneamente cuando vienen a mi mente?",
        "¿De qué temas me resulta incómodo hablar?",
        "¿Cuál fue mi mayor alegría y mi mayor tristeza esta semana?",
        "¿Hay alguna emoción con la que me cueste más lidiar, o que no me resulte fácil gestionar?",
        "Cuando estoy triste, algo que me ayuda es... Y, ¿de qué manera me gusta ser acompañado/a en esos momentos?",
        "¿De qué me siento cansado/a en este momento de mi vida?",
        "¿Cuál es esa situación, persona o pensamiento con la que me pongo particularmente nervioso/a?",
        "¿Qué es eso que me emociona y me mueve tanto por dentro, que incluso a veces me saca algunas lágrimas?",
        "¿Cuáles son esas cosas que más alegran mi corazón? ¿Cuando estoy así de contento/a, qué hago?",
        "¿Qué es eso en la vida con lo que me enojo particularmente? ¿Qué pienso, qué digo y qué hago cuando estoy enojado/a?",
        "¿Qué fue lo último que hizo que se me escaparan unas lágrimas? ¿Hace cuánto tiempo fue?"
    ],
    "RECUERDOS": [
        "¿Cómo describiría mi etapa escolar?",
        "¿Qué características de mi 'yo' de niño/a se mantienen hoy?",
        "¿Cuál fue esa moda o estilo que seguí, que hoy considero vergonzoso?",
        "¿Cuál ha sido el momento más feliz de mi vida?",
        "¿Hay algo que quisiera repetir y/o que nunca volvería a hacer en la vida?",
        "¿Cuál ha sido mi mayor vergüenza o 'chascarro' en la vida?",
        "¿Cuáles fueron los hitos más importantes de mi niñez?",
        "¿Cuáles fueron los hitos más importantes de mi juventud?",
        "¿Cuáles son esas historias de mi vida, que le quisiera 'contar a mis nietos/as'?",
        "Puedo echar a volar mi curiosidad, ¿qué me gustaría que me cuentes de tu historia?",
        "¿Cuáles eran mis juegos favoritos de niño/a? ¿Considero que tienen algo que ver conmigo hoy?"
    ],
    "GENERAL": [
        "Si pudiera ser del sexo opuesto por un día, ¿qué haría?",
        "¿Qué es lo más raro/paranormal que me ha pasado en la vida?",
        "¿Cómo sería un fin de semana 'redondito/ideal' para mí, en este momento de mi vida?",
        "Si tuviera que dar una charla TED que va a escuchar todo el mundo, ¿sobre qué tema hablaría y por qué?",
        "Si pudiera tener un superpoder, ¿cuál elegiría? Explica por qué, y qué harías con él.",
        "Si me reencarnara en un objeto, ¿cuál definitivamente no me gustaría ser?",
        "Si mañana despierto atrevido/a y dispuesto/a a todo, ¿qué locura me lanzaría a hacer?",
        "Si pudiera cambiar la época en la que nací, ¿por cuál sería? ¿Qué me gustaría vivir ahí?",
        "Si pudiera vivir dentro de una película por un día, ¿cuál sería? ¿Qué me gustaría vivir ahí?",
        "¿Con qué animal me siento identificado/a? ¿Por qué?",
        "Si tuviera que elegir uno de mis cinco sentidos, ¿cuál sería y por qué?",
        "Si en este momento me pudiera hacer un 'autoregalo' (no necesariamente material), ¿cuál sería y por qué?",
        "¿Qué es lo más loco que he hecho en mi vida?",
        "Si pudiera ser un/a famoso/a durante un día, ¿quién sería y qué haría?"
    ]
}

ESTILOS_CATEGORIA = {
    "PENSAMIENTOS": {"bg": "#b4bd5c", "text": "#305727"},
    "CONEXIONES":  {"bg": "#93C5FD", "text": "#1E3A8A"},
    "EMOCIONES":   {"bg": "#FCA5A5", "text": "#7F1D1D"},
    "RECUERDOS":   {"bg": "#D8B4FE", "text": "#581C87"},
    "GENERAL":     {"bg": "#FDE68A", "text": "#78350F"}
}

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@700;800&family=Patrick+Hand&family=Caveat:wght@600;700&display=swap');
    @import url('https://fonts.cdnfonts.com/css/bryndan-write');

    .stApp {
        background: linear-gradient(135deg, #b4b86a 0%, #12cdb0 100%) !important;
        background-attachment: fixed !important;
        color: #1E293B;
    }
    
    h1, h2, h3, p {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    h1, h2, h3 {
        color: #1E293B !important;
        text-align: center;
        font-weight: 700 !important;
    }
    
    /* BOTONES DE CATEGORÍA */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        border-radius: 50px !important;
        border: 3px solid #000000 !important;
        box-shadow: 4px 5px 0px #000000 !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
    }

    div.stButton > button, 
    div.stButton > button *, 
    div.stButton > button p {
        font-family: 'Comfortaa', cursive, sans-serif !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
    }

    .st-key-btn_PENSAMIENTOS button { background-color: #b4bd5c !important; color: #23431d !important; }
    .st-key-btn_CONEXIONES button { background-color: #93C5FD !important; color: #1E3A8A !important; }
    .st-key-btn_EMOCIONES button { background-color: #FCA5A5 !important; color: #7F1D1D !important; }
    .st-key-btn_RECUERDOS button { background-color: #D8B4FE !important; color: #581C87 !important; }
    .st-key-btn_GENERAL button { background-color: #FDE68A !important; color: #78350F !important; }

    div.stButton > button:hover {
        transform: translate(-1px, -1px) !important;
        box-shadow: 6px 7px 0px #000000 !important;
        filter: brightness(1.03) !important;
    }
    
    div.stButton > button:active {
        transform: translate(3px, 3px) !important;
        box-shadow: 1px 2px 0px #000000 !important;
    }

    .carta-box {
        padding: 40px 30px;
        border-radius: 24px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
        border: 3px solid #000000;
    }
    
    .pregunta-texto {
        font-family: 'Bryndan Write', 'Patrick Hand', 'Caveat', cursive, sans-serif !important;
        font-size: 32px !important;
        font-weight: 500;
        line-height: 1.4;
    }

    .sala-badge {
        background: #000000;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
    }

    .turno-badge {
        background: #12cdb0;
        color: #000000;
        padding: 10px 24px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 18px;
        border: 3px solid #000000;
        box-shadow: 3px 4px 0px #000000;
        display: inline-block;
        margin-top: 10px;
    }

    .dado-card {
        background: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 3px 3px 0px #000000;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONTROL DE SALA Y ROLES
# -----------------------------------------------------------------------------
if 'codigo_sala' not in st.session_state:
    st.session_state.codigo_sala = None
if 'mi_rol' not in st.session_state:
    st.session_state.mi_rol = None

def crear_nueva_sala():
    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    BD_SALAS[codigo] = {
        "mazos": {cat: list(preg) for cat, preg in PREGUNTAS_BASE.items()},
        "carta_actual": None,
        "jugadores": {
            "jugador1": "Jugador 1",
            "jugador2": None
        },
        "dados": {
            "jugador1": None,
            "jugador2": None
        },
        "turno": None,
        "mensajes": []  # Almacena los mensajes del chat
    }
    return codigo

def sacar_carta_sala(codigo_sala, cat, rol_jugador):
    sala = BD_SALAS[codigo_sala]
    if len(sala["mazos"][cat]) > 0:
        pregunta = random.choice(sala["mazos"][cat])
        sala["mazos"][cat].remove(pregunta)
        
        nombre_actual = sala["jugadores"][rol_jugador]
        sala["carta_actual"] = {
            "categoria": cat,
            "pregunta": pregunta,
            "jugador": nombre_actual
        }
        
        # Alternar turno al otro jugador
        sala["turno"] = "jugador2" if rol_jugador == "jugador1" else "jugador1"

# -----------------------------------------------------------------------------
# INTERFAZ: LOBBY
# -----------------------------------------------------------------------------
st.title("🧩 Ubuntu: Cartas de Conexión")

if not st.session_state.codigo_sala:
    st.markdown("<p style='text-align: center; font-weight: 600;'>Para jugar juntos, ambos deben ingresar a la misma sala.</p>", unsafe_allow_html=True)
    st.divider()

    col_crear, col_unirse = st.columns(2)

    with col_crear:
        st.subheader("Crear Partida")
        if st.button("➕ Crear Nueva Sala"):
            nueva_sala = crear_nueva_sala()
            st.session_state.codigo_sala = nueva_sala
            st.session_state.mi_rol = "jugador1"
            st.rerun()

    with col_unirse:
        st.subheader("Unirse a Partida")
        codigo_input = st.text_input("Código de Sala (4 letras/números):").strip().upper()
        if st.button("🔗 Unirse a la Sala"):
            if codigo_input in BD_SALAS:
                sala = BD_SALAS[codigo_input]
                if st.session_state.codigo_sala == codigo_input:
                    st.rerun()
                elif sala["jugadores"]["jugador2"] is None:
                    sala["jugadores"]["jugador2"] = "Jugador 2"
                    st.session_state.codigo_sala = codigo_input
                    st.session_state.mi_rol = "jugador2"
                    st.rerun()
                else:
                    st.error("¡La sala ya está llena! Solo se permiten 2 jugadores por partida.")
            else:
                st.error("¡Esa sala no existe! Revisa el código.")

else:
    # -----------------------------------------------------------------------------
    # INTERFAZ: TABLERO EN VIVO
    # -----------------------------------------------------------------------------
    codigo_sala = st.session_state.codigo_sala
    mi_rol = st.session_state.mi_rol

    if codigo_sala not in BD_SALAS:
        st.session_state.codigo_sala = None
        st.session_state.mi_rol = None
        st.rerun()

    sala_datos = BD_SALAS[codigo_sala]
    j1_nombre = sala_datos["jugadores"]["jugador1"]
    j2_nombre = sala_datos["jugadores"]["jugador2"]

    # BARRA LATERAL (Sidebar)
    st.sidebar.title("⚙️ Opciones de Sala")
    st.sidebar.markdown(f"**Código de sala:** `{codigo_sala}`")
    st.sidebar.markdown(f"**Tu Rol:** `{mi_rol.upper()}`")
    st.sidebar.divider()
    st.sidebar.subheader("Nombres de Jugadores:")

    if mi_rol == "jugador1":
        nuevo_nombre_j1 = st.sidebar.text_input("Mi nombre (Jugador 1):", value=j1_nombre)
        if nuevo_nombre_j1.strip():
            sala_datos["jugadores"]["jugador1"] = nuevo_nombre_j1.strip()
        
        if j2_nombre:
            st.sidebar.text_input("Jugador 2:", value=j2_nombre, disabled=True)
        else:
            st.sidebar.info("⏳ Esperando a que el Jugador 2 se conecte...")

    elif mi_rol == "jugador2":
        st.sidebar.text_input("Jugador 1 (Anfitrión):", value=j1_nombre, disabled=True)
        nuevo_nombre_j2 = st.sidebar.text_input("Mi nombre (Jugador 2):", value=j2_nombre or "Jugador 2")
        if nuevo_nombre_j2.strip():
            sala_datos["jugadores"]["jugador2"] = nuevo_nombre_j2.strip()

    st.sidebar.divider()
    if st.sidebar.button("🔄 Reiniciar Mazo y Dados"):
        BD_SALAS[codigo_sala]["mazos"] = {cat: list(preg) for cat, preg in PREGUNTAS_BASE.items()}
        BD_SALAS[codigo_sala]["carta_actual"] = None
        BD_SALAS[codigo_sala]["dados"] = {"jugador1": None, "jugador2": None}
        BD_SALAS[codigo_sala]["turno"] = None
        st.rerun()

    # HEADER DE SALA
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown(f"<div class='sala-badge'>SALA: {codigo_sala}</div>", unsafe_allow_html=True)
    with col_head2:
        if st.button("🚪 Salir"):
            if mi_rol == "jugador2":
                sala_datos["jugadores"]["jugador2"] = None
            st.session_state.codigo_sala = None
            st.session_state.mi_rol = None
            st.rerun()

    # -----------------------------------------------------------------------------
    # TABLERO Y CHAT SINCRONIZADOS CADA 2 SEGUNDOS
    # -----------------------------------------------------------------------------
    @st.fragment(run_every="2s")
    def tablero_juego_sincronizado(codigo_sala, mi_rol):
        sala = BD_SALAS.get(codigo_sala)
        if not sala:
            return

        j1 = sala["jugadores"]["jugador1"]
        j2 = sala["jugadores"]["jugador2"]

        # 1. ESPERA DEL JUGADOR 2
        if not j2:
            st.warning(f"👋 ¡Hola {j1}! Pásale el código **`{codigo_sala}`** a tu compañera para que se una a la partida.")
            st.info("⏳ Esta pantalla avanzará automáticamente cuando el Jugador 2 se conecte...")
            return

        # 2. DADOS
        d1 = sala["dados"]["jugador1"]
        d2 = sala["dados"]["jugador2"]

        st.subheader("🎲 Sorteo con Dado")
        col_dado1, col_dado2 = st.columns(2)

        with col_dado1:
            st.markdown(f"<div class='dado-card'><b>{j1}</b>", unsafe_allow_html=True)
            if d1 is not None:
                st.markdown(f"<h2 style='margin:10px 0;'>🎲 {d1}</h2>", unsafe_allow_html=True)
            else:
                st.write("Aún no ha tirado")
                if mi_rol == "jugador1":
                    if st.button("🎲 Tirar mi dado", key="btn_dado_j1"):
                        sala["dados"]["jugador1"] = random.randint(1, 6)
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col_dado2:
            st.markdown(f"<div class='dado-card'><b>{j2}</b>", unsafe_allow_html=True)
            if d2 is not None:
                st.markdown(f"<h2 style='margin:10px 0;'>🎲 {d2}</h2>", unsafe_allow_html=True)
            else:
                st.write("Aún no ha tirado")
                if mi_rol == "jugador2":
                    if st.button("🎲 Tirar mi dado", key="btn_dado_j2"):
                        sala["dados"]["jugador2"] = random.randint(1, 6)
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # EVALUACIÓN DE DADOS Y TURNO INICIAL
        if d1 is not None and d2 is not None and sala["turno"] is None:
            if d1 > d2:
                sala["turno"] = "jugador1"
            elif d2 > d1:
                sala["turno"] = "jugador2"
            else:
                st.error("¡Empataron los dados! Tiren de nuevo.")
                if st.button("🔄 Repetir tiro de dados"):
                    sala["dados"] = {"jugador1": None, "jugador2": None}
                    st.rerun()

        st.divider()

        # 3. INDICADOR DE TURNO
        es_mi_turno = (sala["turno"] == mi_rol)
        nombre_turno_actual = sala["jugadores"].get(sala["turno"], "Nadie (tiren los dados)")

        if sala["turno"]:
            if es_mi_turno:
                st.markdown(f"<div style='text-align:center;'><span class='turno-badge'>🎯 ¡ES TU TURNO DE ELEGIR CARTA!</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center;'><span class='turno-badge' style='background:#fca5a5;'>⏳ TURNO DE: {nombre_turno_actual.upper()}</span></div>", unsafe_allow_html=True)
        else:
            st.info("💡 Ambos deben tirar sus dados arriba para definir quién empieza.")

        st.write("")
        st.subheader("Elige un mazo:")

        # 4. BOTONES DE MAZOS
        col1, col2, col3 = st.columns(3)
        fila_1 = [("PENSAMIENTOS", col1), ("CONEXIONES", col2), ("EMOCIONES", col3)]

        for cat, col in fila_1:
            cant = len(sala["mazos"][cat])
            with col:
                if col.button(cat, key=f"btn_{cat}", disabled=(cant == 0 or not es_mi_turno)):
                    sacar_carta_sala(codigo_sala, cat, mi_rol)
                    st.rerun()

        st.write("")

        sp_izq, col_recuerdos, col_general, sp_der = st.columns([0.5, 1, 1, 0.5])

        cant_recuerdos = len(sala["mazos"]["RECUERDOS"])
        with col_recuerdos:
            if col_recuerdos.button("RECUERDOS", key="btn_RECUERDOS", disabled=(cant_recuerdos == 0 or not es_mi_turno)):
                sacar_carta_sala(codigo_sala, "RECUERDOS", mi_rol)
                st.rerun()

        cant_general = len(sala["mazos"]["GENERAL"])
        with col_general:
            if col_general.button("GENERAL", key="btn_GENERAL", disabled=(cant_general == 0 or not es_mi_turno)):
                sacar_carta_sala(codigo_sala, "GENERAL", mi_rol)
                st.rerun()

        # 5. CARTA DESPLEGADA
        if sala["carta_actual"]:
            cat = sala["carta_actual"]["categoria"]
            pregunta = sala["carta_actual"]["pregunta"]
            quien_saco = sala["carta_actual"]["jugador"]
            estilo = ESTILOS_CATEGORIA[cat]
            
            st.markdown(f"""
                <div class="carta-box" style="background-color: {estilo['bg']}; color: {estilo['text']};">
                    <div style="font-size: 14px; font-weight: 700; opacity: 0.8; margin-bottom: 8px;">
                        CARTA DE {quien_saco.upper()}
                    </div>
                    <div class="pregunta-texto">{pregunta}</div>
                </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # 6. SECCIÓN CHAT DE LA SALA EN VIVO
        # -------------------------------------------------------------------------
        st.divider()
        st.subheader("💬 Chat de la Sala")

        # Mensajes en caja scrollable
        chat_box = st.container(height=180)
        with chat_box:
            if not sala["mensajes"]:
                st.caption("Aún no hay mensajes. ¡Escribe algo para hablar mientras juegan!")
            for msg in sala["mensajes"]:
                if msg["rol"] == mi_rol:
                    st.markdown(f"**Tú ({msg['autor']}):** {msg['texto']}")
                else:
                    st.markdown(f"**{msg['autor']}:** {msg['texto']}")

        # Formulario para mandar mensajes
        mi_nombre_chat = sala["jugadores"][mi_rol] or ("Jugador 1" if mi_rol == "jugador1" else "Jugador 2")
        with st.form("form_chat_sala", clear_on_submit=True):
            col_txt, col_btn = st.columns([4, 1])
            with col_txt:
                texto_mensaje = st.text_input("Escribe un mensaje...", placeholder="Escribe un mensaje aquí...", label_visibility="collapsed")
            with col_btn:
                btn_enviar = st.form_submit_button("Enviar 📩")

            if btn_enviar and texto_mensaje.strip():
                sala["mensajes"].append({
                    "rol": mi_rol,
                    "autor": mi_nombre_chat,
                    "texto": texto_mensaje.strip()
                })
                st.rerun()

    # LLAMADA A LA FUNCIÓN AUTO-SINCRONIZADA
    tablero_juego_sincronizado(codigo_sala, mi_rol)