"""
CV Ready — Módulo de procesamiento de datos
=============================================
Este módulo corresponde a la Fase 2 (Procesamiento de datos) del proyecto
CV Ready. Se encarga de limpiar y estructurar el texto crudo de un CV antes
de enviarlo al motor de análisis con IA.

En la demo interactiva (cv_ready_app.html) esta limpieza básica se hace
directamente en el navegador para que la app funcione sin backend. Este
script representa la misma lógica implementada en Python, pensada para un
escenario real donde el procesamiento correría del lado del servidor
(por ejemplo, dentro de un endpoint de FastAPI).

Autor: Mateo Di Benedetto
"""

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. LIMPIEZA DE TEXTO
# ---------------------------------------------------------------------------

def limpiar_texto(texto_crudo: str) -> str:
    """
    Normaliza el texto extraído de un CV (por ejemplo, copiado de un PDF).

    - Saca espacios en blanco de más
    - Une líneas cortadas a la mitad de una oración (típico de PDFs mal
      extraídos, donde cada línea del documento se convierte en un salto
      de línea aunque la oración siga)
    - Elimina caracteres de control invisibles
    """
    texto = texto_crudo.replace("\r\n", "\n").replace("\r", "\n")

    # Elimina caracteres de control que a veces vienen de copiar un PDF
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", texto)

    # Colapsa 3+ saltos de línea seguidos en solo 2 (separación entre bloques)
    texto = re.sub(r"\n{3,}", "\n\n", texto)

    # Colapsa espacios múltiples dentro de una misma línea
    texto = re.sub(r"[ \t]{2,}", " ", texto)

    return texto.strip()


# ---------------------------------------------------------------------------
# 2. SEGMENTACIÓN EN SECCIONES
# ---------------------------------------------------------------------------

# Encabezados típicos de un CV en español, con variantes comunes.
# Se usa esto para dividir el documento en bloques temáticos antes de
# mandarlo a la IA, lo que permite análisis más precisos por sección.
SECCIONES_CONOCIDAS = {
    "experiencia": r"experiencia(\s+laboral)?|historial\s+laboral",
    "educacion": r"educaci[oó]n|formaci[oó]n\s+acad[eé]mica",
    "habilidades": r"habilidades|skills|competencias\s+t[eé]cnicas",
    "idiomas": r"idiomas|languages",
    "certificaciones": r"certificaciones|cursos|certificates",
    "resumen": r"resumen|perfil\s+profesional|about\s+me|summary",
}


@dataclass
class CVSegmentado:
    """Representa un CV ya dividido en secciones identificables."""
    secciones: dict = field(default_factory=dict)
    texto_sin_clasificar: str = ""


def segmentar_cv(texto_limpio: str) -> CVSegmentado:
    """
    Divide el texto del CV en secciones (Experiencia, Educación, etc.)
    usando los encabezados como puntos de corte.

    Estrategia: recorre el texto línea por línea. Cuando encuentra una
    línea que matchea alguno de los patrones de SECCIONES_CONOCIDAS, abre
    una sección nueva; todo el texto siguiente se acumula ahí hasta el
    próximo encabezado.
    """
    lineas = texto_limpio.split("\n")
    resultado = CVSegmentado()
    seccion_actual = None
    buffer_sin_clasificar = []

    patrones_compilados = {
        clave: re.compile(rf"^\s*({patron})\s*:?\s*$", re.IGNORECASE)
        for clave, patron in SECCIONES_CONOCIDAS.items()
    }

    for linea in lineas:
        linea_stripped = linea.strip()
        if not linea_stripped:
            continue

        seccion_detectada = None
        for clave, patron in patrones_compilados.items():
            if patron.match(linea_stripped):
                seccion_detectada = clave
                break

        if seccion_detectada:
            seccion_actual = seccion_detectada
            resultado.secciones.setdefault(seccion_actual, [])
            continue

        if seccion_actual:
            resultado.secciones[seccion_actual].append(linea_stripped)
        else:
            buffer_sin_clasificar.append(linea_stripped)

    # Convierte las listas de líneas en texto plano por sección
    resultado.secciones = {
        k: "\n".join(v) for k, v in resultado.secciones.items()
    }
    resultado.texto_sin_clasificar = "\n".join(buffer_sin_clasificar)

    return resultado


# ---------------------------------------------------------------------------
# 3. EXTRACCIÓN DE VIÑETAS (bullets de experiencia)
# ---------------------------------------------------------------------------

def extraer_bullets(texto_seccion: str) -> list[str]:
    """
    Extrae las líneas que funcionan como viñetas dentro de una sección
    (por ejemplo, los logros dentro de "Experiencia"), reconociendo los
    símbolos más comunes de lista: -, •, *, o números seguidos de punto.
    """
    patron_bullet = re.compile(r"^\s*[-•*]\s+|^\s*\d+[.)]\s+")
    bullets = []
    for linea in texto_seccion.split("\n"):
        if patron_bullet.match(linea):
            bullets.append(patron_bullet.sub("", linea).strip())
    return bullets


# ---------------------------------------------------------------------------
# 4. ARMADO DEL PAYLOAD PARA LA IA
# ---------------------------------------------------------------------------

def construir_payload_ia(cv_segmentado: CVSegmentado, descripcion_puesto: str = "") -> dict:
    """
    Arma el diccionario final que se enviaría al modelo de IA para el
    análisis (Fase 3). Mantener esta función separada de la limpieza
    permite testear cada etapa del pipeline de forma independiente.
    """
    return {
        "secciones": cv_segmentado.secciones,
        "texto_no_clasificado": cv_segmentado.texto_sin_clasificar,
        "descripcion_puesto": descripcion_puesto or None,
        "tiene_experiencia": "experiencia" in cv_segmentado.secciones,
        "tiene_habilidades": "habilidades" in cv_segmentado.secciones,
    }


# ---------------------------------------------------------------------------
# EJEMPLO DE USO / CASO DE PRUEBA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cv_de_ejemplo = """
    RESUMEN
    Analista de datos junior con experiencia en Python y SQL.


    EXPERIENCIA
    - Encargado de reportes de ventas mensuales
    - Uso de Excel para armar tableros
    Trabajé también en la limpieza de bases de datos grandes


    HABILIDADES
    Python, SQL, Power BI, Excel avanzado

    EDUCACION
    Tecnicatura en Ciencia de Datos, Coderhouse
    """

    print("=== 1. Texto limpio ===")
    limpio = limpiar_texto(cv_de_ejemplo)
    print(limpio)

    print("\n=== 2. CV segmentado ===")
    segmentado = segmentar_cv(limpio)
    for seccion, contenido in segmentado.secciones.items():
        print(f"\n[{seccion.upper()}]\n{contenido}")

    print("\n=== 3. Bullets detectados en Experiencia ===")
    bullets = extraer_bullets(segmentado.secciones.get("experiencia", ""))
    for b in bullets:
        print(f"  • {b}")

    print("\n=== 4. Payload final para la IA ===")
    payload = construir_payload_ia(segmentado, descripcion_puesto="Analista de Datos Jr - Python, SQL, Power BI")
    import json
    print(json.dumps(payload, indent=2, ensure_ascii=False))
