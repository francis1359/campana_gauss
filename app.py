import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import io


# Configuración
st.set_page_config(
    page_title="Campana de Gauss",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
}

.subtitle {
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.result {
    padding: 15px;
    border-radius: 10px;
    background: #f4f8fc;
    border: 1px solid #dbe7f3;
    text-align: center;
}

.result-label {
    color: #475569;
    font-size: 14px;
}

.result-value {
    font-size: 24px;
    font-weight: 700;
    color: #2563EB;
}
</style>
""", unsafe_allow_html=True)


# Colores
BLUE = "#2878B5"
GREEN = "#16A085"
RED = "#D62728"
PURPLE = "#7B2CBF"


# Interfaz
st.markdown(
    '<div class="main-title">📈 Campana de Gauss</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Calculadora de distribución normal</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    media = st.number_input(
        "Media (μ)",
        value=None,
        placeholder="Ingrese la media"
    )

with col2:
    desviacion = st.number_input(
        "Desviación estándar (σ)",
        value=None,
        min_value=0.01,
        placeholder="Ingrese la desviación estándar"
    )


tipo = st.selectbox(
    "¿Qué probabilidad deseas calcular?",
    [
        "Mayor que (X > x)",
        "Menor que (X < x)",
        "Entre dos valores (a < X < b)"
    ]
)


# Valores
if tipo.startswith("Entre"):

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "Valor inferior (a)",
            value=None,
            placeholder="Ingrese el valor inferior"
        )

    with col2:
        b = st.number_input(
            "Valor superior (b)",
            value=None,
            placeholder="Ingrese el valor superior"
        )

else:

    x = st.number_input(
        "Valor X",
        value=None,
        placeholder="Ingrese el valor X"
    )


# Etiquetas
def etiqueta(ax, x, texto, y, color, size=11):
    ax.text(
        x,
        y,
        texto,
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="top",
        color=color,
        fontsize=size,
        fontweight="bold"
    )


# Ejes X y Z
def configurar_ejes(ax):
    ax.set_xlabel("")
    ax.set_ylabel("Densidad")
    ax.grid(alpha=0.2)

    ax.plot(
        [0, 1],
        [0, 0],
        transform=ax.transAxes,
        color="black",
        linewidth=1,
        clip_on=False
    )

    ax.text(
        1.02,
        0.035,
        "X",
        transform=ax.transAxes,
        fontweight="bold"
    )

    ax.plot(
        [0, 1],
        [-0.20, -0.20],
        transform=ax.transAxes,
        color=PURPLE,
        linewidth=1.5,
        clip_on=False
    )

    ax.text(
        1.015,
        -0.20,
        "Z",
        transform=ax.transAxes,
        color=PURPLE,
        fontweight="bold"
    )


# Evitar choque entre ticks
def limpiar_ticks(ax, especiales):
    ticks = ax.get_xticks()

    ticks = [
        t for t in ticks
        if all(
            abs(t - e) > desviacion * 0.4
            for e in especiales
        )
    ]

    ax.set_xticks(ticks)


# Crear gráfica
def crear_grafica(
    media,
    desviacion,
    tipo,
    x=None,
    a=None,
    b=None,
    z=None,
    z_a=None,
    z_b=None
):

    valores = np.linspace(
        media - 4 * desviacion,
        media + 4 * desviacion,
        1000
    )

    densidad = norm.pdf(
        valores,
        media,
        desviacion
    )

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        valores,
        densidad,
        color=BLUE,
        linewidth=2.5
    )

    especiales = [media]

    # Mayor que
    if tipo == "Mayor que (X > x)":

        area = valores >= x

        ax.fill_between(
            valores[area],
            densidad[area],
            color=BLUE,
            alpha=0.4
        )

        ax.axvline(
            x,
            color=RED,
            linestyle="--",
            linewidth=2.5
        )

        etiqueta(
            ax,
            x,
            f"{x:,.0f}",
            -0.075,
            RED
        )

        etiqueta(
            ax,
            x,
            f"Z={z:.2f}",
            -0.135,
            PURPLE,
            10
        )

        especiales.append(x)

    # Menor que
    elif tipo == "Menor que (X < x)":

        area = valores <= x

        ax.fill_between(
            valores[area],
            densidad[area],
            color=BLUE,
            alpha=0.4
        )

        ax.axvline(
            x,
            color=RED,
            linestyle="--",
            linewidth=2.5
        )

        etiqueta(
            ax,
            x,
            f"{x:,.0f}",
            -0.075,
            RED
        )

        etiqueta(
            ax,
            x,
            f"Z={z:.2f}",
            -0.135,
            PURPLE,
            10
        )

        especiales.append(x)

    # Entre dos valores
    else:

        area = (
            (valores >= a) &
            (valores <= b)
        )

        ax.fill_between(
            valores[area],
            densidad[area],
            color=BLUE,
            alpha=0.4
        )

        ax.axvline(
            a,
            color=RED,
            linestyle="--",
            linewidth=2.5
        )

        ax.axvline(
            b,
            color=RED,
            linestyle="--",
            linewidth=2.5
        )

        distancia = abs(b - a)

        # Separar etiquetas cuando están muy cerca
        if distancia < desviacion * 0.45:

            separacion = desviacion * 0.12

            etiqueta(
                ax,
                a - separacion,
                f"{a:,.0f}",
                -0.075,
                RED
            )

            etiqueta(
                ax,
                a - separacion,
                f"Z={z_a:.2f}",
                -0.135,
                PURPLE,
                10
            )

            etiqueta(
                ax,
                b + separacion,
                f"{b:,.0f}",
                -0.075,
                RED
            )

            etiqueta(
                ax,
                b + separacion,
                f"Z={z_b:.2f}",
                -0.135,
                PURPLE,
                10
            )

        else:

            etiqueta(
                ax,
                a,
                f"{a:,.0f}",
                -0.075,
                RED
            )

            etiqueta(
                ax,
                a,
                f"Z={z_a:.2f}",
                -0.135,
                PURPLE,
                10
            )

            etiqueta(
                ax,
                b,
                f"{b:,.0f}",
                -0.075,
                RED
            )

            etiqueta(
                ax,
                b,
                f"Z={z_b:.2f}",
                -0.135,
                PURPLE,
                10
            )

        especiales.extend([a, b])

    # Media
    ax.axvline(
        media,
        color=GREEN,
        linestyle=":",
        linewidth=2.5
    )

    # Media al nivel de los valores del eje X
    if tipo.startswith("Entre"):

        etiqueta(
            ax,
            media,
            f"{media:,.0f}",
            -0.030,
            GREEN,
            10
        )

    else:

        etiqueta(
            ax,
            media,
            f"{media:,.0f}",
            -0.075,
            GREEN
        )

    limpiar_ticks(
        ax,
        especiales
    )

    ax.set_title(
        "Distribución Normal",
        fontsize=15
    )

    configurar_ejes(ax)

    plt.subplots_adjust(
        left=0.08,
        right=0.94,
        top=0.90,
        bottom=0.30
    )

    return fig


# Cálculo
if st.button(
    "Calcular probabilidad",
    type="primary",
    use_container_width=True
):

    if media is None or desviacion is None:
        st.warning(
            "Ingrese la media y la desviación estándar."
        )
        st.stop()

    # Entre dos valores
    if tipo.startswith("Entre"):

        if a is None or b is None:
            st.warning(
                "Ingrese los dos valores."
            )
            st.stop()

        if a >= b:
            st.error(
                "El valor inferior debe ser menor que el superior."
            )
            st.stop()

        z_a = (a - media) / desviacion
        z_b = (b - media) / desviacion

        probabilidad = (
            norm.cdf(z_b) -
            norm.cdf(z_a)
        )

        fig = crear_grafica(
            media,
            desviacion,
            tipo,
            a=a,
            b=b,
            z_a=z_a,
            z_b=z_b
        )

        st.subheader("Resultado")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="result">
                    <div class="result-label">Z₁</div>
                    <div class="result-value">{z_a:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="result">
                    <div class="result-label">Z₂</div>
                    <div class="result-value">{z_b:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="result">
                    <div class="result-label">Probabilidad</div>
                    <div class="result-value">
                        {probabilidad * 100:.2f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Mayor o menor
    else:

        if x is None:
            st.warning("Ingrese el valor X.")
            st.stop()

        z = (x - media) / desviacion

        if tipo.startswith("Mayor"):
            probabilidad = 1 - norm.cdf(z)
        else:
            probabilidad = norm.cdf(z)

        fig = crear_grafica(
            media,
            desviacion,
            tipo,
            x=x,
            z=z
        )

        st.subheader("Resultado")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                f"""
                <div class="result">
                    <div class="result-label">Valor Z</div>
                    <div class="result-value">{z:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="result">
                    <div class="result-label">Probabilidad</div>
                    <div class="result-value">
                        {probabilidad * 100:.2f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Gráfica
    st.subheader("Representación gráfica")

    st.pyplot(
        fig,
        use_container_width=True
    )

    # Descargar gráfica
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=300,
        bbox_inches="tight"
    )

    buffer.seek(0)

    st.download_button(
        "⬇️ Descargar gráfica",
        data=buffer,
        file_name="distribucion_normal.png",
        mime="image/png",
        use_container_width=True
    )