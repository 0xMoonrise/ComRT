"""
Divulgación: Aplicaciones de Radiolocalización y Telemetría
Ejecutar con:  streamlit run app_radiolocalizacion_telemetria.py
Dependencias:  pip install streamlit numpy plotly
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Radiolocalización y Telemetría",
    layout="wide",
)

PLANTILLA = "plotly_white"
CONFIG_PLOTLY = {"displaylogo": False, "scrollZoom": True}


def hora_hhmm(h):
    """Convierte horas decimales a formato HH:MM."""
    return f"{int(h):02d}:{int(round((h % 1) * 60)):02d}"


st.title("Aplicaciones de Radiolocalización y Telemetría")
st.caption(
    "Fundamentos, modelos matemáticos y simulaciones para la determinación "
    "de posición y la medición remota de variables físicas."
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Fundamentos", "Radiolocalización", "Telemetría", "Aplicaciones"]
)

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Radiolocalización")
        st.markdown(
            """
La radiolocalización es el conjunto de técnicas que emplean **ondas
electromagnéticas** para determinar la posición de un objeto. Se basa en que
ciertas propiedades de la señal recibida (potencia, tiempo de propagación o
ángulo de arribo) dependen de la geometría entre el emisor y el receptor.

**Técnicas principales**

- **RSSI** (*Received Signal Strength Indicator*): estima la distancia a partir
  de la atenuación de la potencia recibida.
- **ToA / TDoA** (*Time of Arrival / Time Difference of Arrival*): estima la
  distancia a partir del tiempo de propagación. Es el principio del GPS.
- **AoA** (*Angle of Arrival*): estima la dirección de la fuente mediante
  antenas direccionales o arreglos de antenas.
- **Trilateración**: determina la posición en el plano a partir de las
  distancias a tres puntos de referencia conocidos.
"""
        )
        st.markdown("Relación entre tiempo de propagación y distancia:")
        st.latex(r"d = c \cdot \Delta t, \qquad c \approx 3 \times 10^{8}\ \mathrm{m/s}")
        st.markdown(
            "Pérdida de propagación en espacio libre (ecuación de Friis, en dB), "
            "donde $f$ es la frecuencia en Hz y $d$ la distancia en metros:"
        )
        st.latex(
            r"\mathrm{FSPL}(d,f) = 20\log_{10}(d) + 20\log_{10}(f) "
            r"+ 20\log_{10}\!\left(\frac{4\pi}{c}\right)"
        )

    with c2:
        st.subheader("Telemetría")
        st.markdown(
            """
La telemetría es la **medición a distancia y la transmisión automática de
datos** desde un punto remoto hacia una estación receptora, donde la
información se almacena, se analiza y, en su caso, genera alertas.

**Cadena funcional típica**

1. **Sensor**: transduce una magnitud física a una señal eléctrica.
2. **Acondicionamiento y digitalización**: el microcontrolador convierte la
   señal en datos discretos y los empaqueta.
3. **Enlace de comunicación**: LoRa, Wi-Fi, red celular o satélite.
4. **Estación base**: recepción, registro, visualización y alarmas.

**Limitaciones habituales:** ruido de medición, pérdida de paquetes, consumo
energético y alcance del enlace.
"""
        )
        st.markdown(
            "Para que una señal pueda reconstruirse a partir de sus muestras, la "
            "frecuencia de muestreo debe satisfacer el criterio de Nyquist-Shannon, "
            "donde $f_{\\max}$ es la máxima componente en frecuencia de la señal:"
        )
        st.latex(r"f_s \geq 2\, f_{\max}")

    st.info(
        "La radiolocalización responde a la pregunta *dónde se encuentra* un "
        "objeto; la telemetría, a *en qué estado se encuentra*. En conjunto "
        "permiten un seguimiento integral de posición y condición."
    )

with tab2:
    st.subheader("Estimación de posición mediante RSSI y trilateración")

    st.markdown(
        "**1. Modelo de pérdida por trayectoria con sombreado log-normal.** "
        "La potencia recibida a una distancia $d$ de un emisor se modela como:"
    )
    st.latex(
        r"\mathrm{RSSI}(d) = P_0 - 10\, n \,\log_{10}\!\left(\frac{d}{d_0}\right) + X_\sigma, "
        r"\qquad X_\sigma \sim \mathcal{N}(0,\sigma^2)"
    )
    st.markdown(
        "donde $P_0$ es la potencia a la distancia de referencia $d_0$, $n$ es el "
        "exponente de pérdida ($n=2$ en espacio libre; $3 \\leq n \\leq 4$ en "
        "interiores con obstáculos) y $X_\\sigma$ es el ruido de sombreado en dB."
    )

    st.markdown("**2. Estimación de la distancia.** Despejando $d$ de la ecuación anterior:")
    st.latex(r"\hat{d} = d_0 \cdot 10^{\frac{P_0 - \mathrm{RSSI}}{10\, n}}")
    st.markdown(
        "Sustituyendo el modelo, el estimador queda expresado en función de la "
        "distancia real y del ruido:"
    )
    st.latex(r"\hat{d} = d \cdot 10^{-\frac{X_\sigma}{10\, n}}")
    st.markdown(
        "Por lo tanto, $\\hat{d}$ sigue una distribución log-normal y la dispersión "
        "relativa de la distancia estimada es aproximadamente:"
    )
    st.latex(r"\sigma_{\ln \hat{d}} = \frac{\sigma \,\ln 10}{10\, n}")
    st.markdown(
        "Esta expresión indica que el error de distancia crece con el ruido "
        "$\\sigma$ y disminuye al aumentar el exponente de pérdida $n$."
    )

    st.markdown(
        "**3. Trilateración.** Dadas $m = 3$ anclas en posiciones conocidas "
        "$(x_i, y_i)$ y distancias estimadas $\\hat{d}_i$, la posición "
        "$\\mathbf{p} = (x, y)$ debe satisfacer:"
    )
    st.latex(r"(x - x_i)^2 + (y - y_i)^2 = \hat{d}_i^{\,2}, \qquad i = 1, 2, 3")
    st.markdown(
        "Restando la primera ecuación a las restantes se eliminan los términos "
        "cuadráticos y se obtiene un sistema lineal $A\\,\\mathbf{p} = \\mathbf{b}$:"
    )
    st.latex(
        r"A = 2\begin{bmatrix} x_2 - x_1 & y_2 - y_1 \\ x_3 - x_1 & y_3 - y_1 \end{bmatrix}, "
        r"\qquad "
        r"\mathbf{b} = \begin{bmatrix} "
        r"\hat{d}_1^{2} - \hat{d}_2^{2} + x_2^2 - x_1^2 + y_2^2 - y_1^2 \\ "
        r"\hat{d}_1^{2} - \hat{d}_3^{2} + x_3^2 - x_1^2 + y_3^2 - y_1^2 "
        r"\end{bmatrix}"
    )
    st.markdown("La solución por mínimos cuadrados y el error de posicionamiento son:")
    st.latex(
        r"\hat{\mathbf{p}} = \left(A^{\top}A\right)^{-1}A^{\top}\mathbf{b}, "
        r"\qquad e = \lVert \hat{\mathbf{p}} - \mathbf{p} \rVert_2"
    )

    st.divider()
    st.markdown("#### Simulación interactiva")
    st.caption(
        "Pase el cursor sobre los elementos para ver sus valores, use la rueda "
        "del ratón para acercar y haga clic en la leyenda para ocultar o mostrar series."
    )

    col_ctrl, col_plot = st.columns([1, 3])

    with col_ctrl:
        x_real = st.slider("Posición real X (m)", 0.0, 10.0, 6.0, 0.5)
        y_real = st.slider("Posición real Y (m)", 0.0, 10.0, 4.0, 0.5)
        n_exp = st.slider("Exponente de pérdida n", 1.5, 4.0, 2.5, 0.1)
        sigma = st.slider(
            "Desviación del ruido σ (dB)", 0.0, 10.0, 3.0, 0.5,
            help="Mayor ruido implica mayor error de estimación.",
        )
        semilla = st.number_input("Semilla aleatoria", 0, 9999, 42)

    P0, d0 = -40.0, 1.0
    anclas = np.array([[0.0, 0.0], [10.0, 0.0], [5.0, 10.0]])
    real = np.array([x_real, y_real])
    rng = np.random.default_rng(int(semilla))

    d_real = np.maximum(np.linalg.norm(anclas - real, axis=1), 0.1)
    rssi = P0 - 10 * n_exp * np.log10(d_real / d0) + rng.normal(0, sigma, 3)
    d_est = d0 * 10 ** ((P0 - rssi) / (10 * n_exp))

    x1, y1 = anclas[0]
    A = 2 * (anclas[1:] - anclas[0])
    b = (
        d_est[0] ** 2 - d_est[1:] ** 2
        + anclas[1:, 0] ** 2 - x1 ** 2
        + anclas[1:, 1] ** 2 - y1 ** 2
    )
    est = np.linalg.lstsq(A, b, rcond=None)[0]
    error = float(np.linalg.norm(est - real))
    sigma_ln = sigma * np.log(10) / (10 * n_exp)

    with col_plot:
        g1, g2 = st.columns([1.2, 1])

        # Mapa de trilateración
        fig_mapa = go.Figure()
        theta = np.linspace(0, 2 * np.pi, 200)
        colores = ["#1f77b4", "#2ca02c", "#9467bd"]

        for i, (a, r) in enumerate(zip(anclas, d_est)):
            fig_mapa.add_trace(go.Scatter(
                x=a[0] + r * np.cos(theta),
                y=a[1] + r * np.sin(theta),
                mode="lines",
                line=dict(color=colores[i], dash="dash", width=1.5),
                name=f"Circunferencia {i + 1}",
                hovertemplate=(
                    f"Ancla {i + 1}<br>d̂ = {r:.2f} m<br>"
                    f"d real = {d_real[i]:.2f} m<extra></extra>"
                ),
            ))

        fig_mapa.add_trace(go.Scatter(
            x=anclas[:, 0], y=anclas[:, 1], mode="markers+text",
            marker=dict(symbol="triangle-up", size=14, color="#1f77b4"),
            text=[f"Ancla {i + 1}" for i in range(3)],
            textposition="top center",
            name="Anclas",
            hovertemplate="Ancla<br>(%{x:.1f}, %{y:.1f}) m<extra></extra>",
        ))
        fig_mapa.add_trace(go.Scatter(
            x=[real[0], est[0]], y=[real[1], est[1]], mode="lines",
            line=dict(color="red", dash="dot", width=2),
            name=f"Error e = {error:.2f} m",
            hovertemplate=f"Error e = {error:.2f} m<extra></extra>",
        ))
        fig_mapa.add_trace(go.Scatter(
            x=[real[0]], y=[real[1]], mode="markers",
            marker=dict(symbol="circle", size=13, color="green"),
            name="Posición real",
            hovertemplate="Real<br>(%{x:.2f}, %{y:.2f}) m<extra></extra>",
        ))
        fig_mapa.add_trace(go.Scatter(
            x=[est[0]], y=[est[1]], mode="markers",
            marker=dict(symbol="x", size=13, color="red", line=dict(width=2)),
            name="Posición estimada",
            hovertemplate="Estimada<br>(%{x:.2f}, %{y:.2f}) m<extra></extra>",
        ))

        fig_mapa.update_layout(
            template=PLANTILLA,
            title="Trilateración con distancias estimadas d̂<sub>i</sub>",
            xaxis=dict(title="x (m)", range=[-8, 18], zeroline=False),
            yaxis=dict(title="y (m)", range=[-8, 18], scaleanchor="x",
                       scaleratio=1, zeroline=False),
            legend=dict(orientation="h", yanchor="top", y=-0.2, x=0),
            margin=dict(l=10, r=10, t=50, b=10),
            height=520,
        )

        # Curva RSSI(d)
        d_curva = np.linspace(1, 15, 200)
        rssi_curva = P0 - 10 * n_exp * np.log10(d_curva / d0)

        fig_rssi = go.Figure()
        fig_rssi.add_trace(go.Scatter(
            x=np.concatenate([d_curva, d_curva[::-1]]),
            y=np.concatenate([rssi_curva + sigma, (rssi_curva - sigma)[::-1]]),
            fill="toself", fillcolor="rgba(31,119,180,0.15)",
            line=dict(width=0), hoverinfo="skip",
            name="Banda ±σ",
        ))
        fig_rssi.add_trace(go.Scatter(
            x=d_curva, y=rssi_curva, mode="lines",
            line=dict(color="#1f77b4", width=2.5),
            name="Modelo RSSI(d)",
            hovertemplate="d = %{x:.2f} m<br>RSSI = %{y:.1f} dBm<extra></extra>",
        ))
        fig_rssi.add_trace(go.Scatter(
            x=d_real, y=rssi, mode="markers+text",
            marker=dict(size=12, color="orange", line=dict(width=1, color="black")),
            text=[f"A{i + 1}" for i in range(3)],
            textposition="top right",
            customdata=np.column_stack([d_est]),
            name="Mediciones con ruido",
            hovertemplate=(
                "d real = %{x:.2f} m<br>RSSI medido = %{y:.1f} dBm<br>"
                "d̂ = %{customdata[0]:.2f} m<extra></extra>"
            ),
        ))
        fig_rssi.update_layout(
            template=PLANTILLA,
            title="Potencia recibida en función de la distancia",
            xaxis=dict(title="Distancia d (m)"),
            yaxis=dict(title="RSSI (dBm)"),
            legend=dict(orientation="h", yanchor="top", y=-0.2, x=0),
            margin=dict(l=10, r=10, t=50, b=10),
            height=520,
        )

        with g1:
            st.plotly_chart(fig_mapa, width='stretch', config=CONFIG_PLOTLY)
        with g2:
            st.plotly_chart(fig_rssi, width='stretch', config=CONFIG_PLOTLY)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Error de posición e", f"{error:.2f} m")
    m2.metric("Posición estimada", f"({est[0]:.1f}, {est[1]:.1f}) m")
    m3.metric("Ruido σ", f"{sigma:.1f} dB")
    m4.metric("Dispersión relativa teórica", f"{100 * sigma_ln:.1f} %",
              help="σ·ln(10) / (10·n), expresada en porcentaje.")

    st.info(
        "**Interpretación.** En el mapa, al aumentar σ las circunferencias dejan "
        "de intersecarse en un único punto y el error e crece. En la gráfica de "
        "potencia, la banda sombreada representa ±σ alrededor del modelo ideal: "
        "las mediciones tienden a caer dentro de ella. La dispersión relativa "
        "teórica cuantifica este efecto y disminuye al aumentar n. En sistemas "
        "reales se promedian múltiples mediciones o se aplican filtros (por "
        "ejemplo, el filtro de Kalman) para reducir el error."
    )

with tab3:
    st.subheader("Adquisición y transmisión de datos de una estación remota")

    st.markdown(
        "**1. Señal física.** Se modela la temperatura ambiente como una "
        "componente media más una oscilación diurna de periodo $T = 24$ h:"
    )
    st.latex(r"T(t) = T_m + A\,\sin\!\left(\frac{2\pi\,(t - t_0)}{24}\right)")
    st.markdown(
        "con $T_m = 26\\,^\\circ\\mathrm{C}$, $A = 6\\,^\\circ\\mathrm{C}$ y "
        "$t_0 = 9$ h, de modo que el máximo ocurre alrededor de las 15:00 h."
    )

    st.markdown(
        "**2. Medición discreta con ruido.** El sensor muestrea cada "
        "$\\Delta t = 15$ min, es decir, $N = 96$ muestras por día:"
    )
    st.latex(
        r"y_k = T(t_k) + \varepsilon_k, \qquad "
        r"\varepsilon_k \sim \mathcal{N}(0,\sigma_s^2), \qquad t_k = k\,\Delta t"
    )

    st.markdown(
        "**3. Canal con pérdida de paquetes.** Cada paquete se recibe con "
        "probabilidad $1-p$, donde $p$ es la probabilidad de pérdida. "
        "Sea $r_k$ una variable de Bernoulli que indica la recepción:"
    )
    st.latex(
        r"r_k \sim \mathrm{Bernoulli}(1-p), \qquad "
        r"\mathbb{E}[N_{\mathrm{rec}}] = N\,(1-p)"
    )

    st.markdown(
        "**4. Regla de alerta.** La estación base genera una alarma si el "
        "paquete fue recibido y la lectura supera el umbral $T_u$:"
    )
    st.latex(r"a_k = r_k \cdot \mathbb{1}\left[\, y_k > T_u \,\right]")

    st.markdown(
        "**5. Verificación del muestreo.** La componente dominante tiene "
        "frecuencia $f = 1/24\\ \\mathrm{h}^{-1}$ y la frecuencia de muestreo es "
        "$f_s = 4\\ \\mathrm{h}^{-1}$, por lo que se cumple con amplio margen:"
    )
    st.latex(r"f_s = 4\ \mathrm{h}^{-1} \gg 2f = \frac{2}{24}\ \mathrm{h}^{-1}")

    st.divider()
    st.markdown("#### Simulación interactiva")
    st.caption(
        "Pase el cursor sobre los puntos para ver hora y lectura. Use el "
        "selector inferior para desplazarse en el tiempo o seleccione una "
        "región para acercar."
    )

    k1, k2 = st.columns([1, 3])

    with k1:
        ruido_s = st.slider("Ruido del sensor σₛ (°C)", 0.0, 3.0, 0.8, 0.1)
        p_perdida = st.slider("Probabilidad de pérdida p (%)", 0, 60, 15, 5)
        umbral = st.slider("Umbral de alerta Tᵤ (°C)", 25.0, 40.0, 32.0, 0.5)
        semilla_t = st.number_input("Semilla aleatoria ", 0, 9999, 7, key="seed_t")

    rng_t = np.random.default_rng(int(semilla_t))
    t = np.arange(0, 24, 0.25)
    verdadera = 26 + 6 * np.sin(2 * np.pi * (t - 9) / 24)
    medida = verdadera + rng_t.normal(0, ruido_s, t.size)
    recibido = rng_t.random(t.size) > (p_perdida / 100)
    alertas = recibido & (medida > umbral)
    esperados = t.size * (1 - p_perdida / 100)
    horas = np.array([hora_hhmm(h) for h in t])

    with k2:
        fig_t = go.Figure()

        fig_t.add_hrect(
            y0=umbral, y1=max(40.0, umbral + 1), line_width=0,
            fillcolor="rgba(214,39,40,0.08)",
        )

        fig_t.add_trace(go.Scatter(
            x=t, y=verdadera, mode="lines",
            line=dict(color="gray", width=2),
            name="Señal real T(t)",
            customdata=horas,
            hovertemplate="%{customdata}<br>T = %{y:.2f} °C<extra></extra>",
        ))
        fig_t.add_trace(go.Scatter(
            x=t[recibido], y=medida[recibido], mode="markers",
            marker=dict(size=7, color="#1f77b4"),
            customdata=horas[recibido],
            name="Paquetes recibidos y<sub>k</sub>",
            hovertemplate="%{customdata}<br>y = %{y:.2f} °C<extra>Recibido</extra>",
        ))
        fig_t.add_trace(go.Scatter(
            x=t[~recibido], y=medida[~recibido], mode="markers",
            marker=dict(size=9, color="rgba(0,0,0,0)",
                        line=dict(width=1.5, color="red")),
            customdata=horas[~recibido],
            name="Paquetes perdidos",
            hovertemplate=(
                "%{customdata}<br>Lectura no recibida: %{y:.2f} °C"
                "<extra>Perdido</extra>"
            ),
        ))
        fig_t.add_trace(go.Scatter(
            x=t[alertas], y=medida[alertas], mode="markers",
            marker=dict(symbol="star", size=15, color="orange",
                        line=dict(width=1, color="black")),
            customdata=horas[alertas],
            name="Alerta a<sub>k</sub> = 1",
            hovertemplate="%{customdata}<br>y = %{y:.2f} °C<extra>Alerta</extra>",
        ))
        fig_t.add_hline(
            y=umbral, line=dict(color="red", dash="dash", width=1.5),
            annotation_text=f"Umbral T<sub>u</sub> = {umbral:.1f} °C",
            annotation_position="top left",
        )

        fig_t.update_layout(
            template=PLANTILLA,
            title="Flujo de telemetría durante 24 horas",
            xaxis=dict(
                title="Hora del día (h)", range=[0, 24],
                tickmode="linear", tick0=0, dtick=3,
                rangeslider=dict(visible=True, thickness=0.07),
            ),
            yaxis=dict(title="Temperatura (°C)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
            margin=dict(l=10, r=10, t=90, b=10),
            height=560,
            hovermode="closest",
        )
        st.plotly_chart(fig_t, width='stretch', config=CONFIG_PLOTLY)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Paquetes enviados N", int(t.size))
    r2.metric("Paquetes recibidos", int(recibido.sum()),
              delta=f"{int((~recibido).sum())} perdidos", delta_color="inverse")
    r3.metric("Recibidos esperados", f"{esperados:.1f}",
              help="Valor esperado N(1 − p).")
    r4.metric("Alertas generadas", int(alertas.sum()))

    st.info(
        "**Interpretación.** La curva gris representa la variable física real, "
        "mientras que los puntos azules corresponden únicamente a la información "
        "disponible en la estación base. La región sombreada indica la zona de "
        "alerta. El número de paquetes recibidos fluctúa alrededor de su valor "
        "esperado N(1 − p). Cuando p es elevada, puede perderse el intervalo en "
        "que se supera el umbral, por lo que los sistemas reales incorporan "
        "confirmaciones de recepción (ACK), retransmisiones y almacenamiento "
        "local en el nodo sensor."
    )

with tab4:
    st.subheader("Ámbitos de aplicación")
    st.markdown(
        "La siguiente tabla resume aplicaciones representativas, la técnica "
        "predominante y la magnitud que se mide o estima."
    )

    st.markdown(
        """
<div align="center">

| Ámbito | Aplicación | Técnica predominante | Magnitud medida o estimada |
|---|---|---|---|
| Navegación | GPS/GNSS en vehículos y dispositivos móviles | ToA (pseudodistancias) | Posición y tiempo |
| Aviación y marítimo | Radar de vigilancia y control de tráfico | ToA y AoA | Distancia, rumbo y velocidad |
| Logística | Rastreo de flotas y contenedores | GNSS con telemetría celular | Posición, velocidad, estado de carga |
| Medio ambiente | Radiotelemetría de fauna silvestre | AoA y RSSI | Posición y movimiento de individuos |
| Meteorología | Estaciones remotas y boyas oceanográficas | Telemetría por radio o satélite | Temperatura, presión, oleaje |
| Salud | Monitoreo remoto de signos vitales | Telemetría inalámbrica | Frecuencia cardiaca, saturación de oxígeno |
| Industria | Mantenimiento predictivo con sensores IoT | Telemetría (LoRa, Wi-Fi) | Vibración, temperatura, consumo |
| Agricultura | Agricultura de precisión | Telemetría y GNSS | Humedad del suelo, posición de maquinaria |
| Espacio | Telemetría de satélites y vehículos de lanzamiento | Telemetría por radiofrecuencia | Estado del sistema, actitud, órbita |
| Emergencias | Balizas de búsqueda y rescate | TDoA y Doppler | Posición del náufrago o aeronave |
| Interiores | Localización en edificios mediante Wi-Fi o BLE | RSSI y fingerprinting | Posición en interiores |

</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("#### Relación entre ambas disciplinas")
    st.markdown(
        "En numerosas aplicaciones ambos conceptos se combinan: el sistema "
        "estima la posición $\\hat{\\mathbf{p}}$ del objeto y, además, transmite "
        "un vector de variables de estado $\\mathbf{s}$. Cada paquete enviado a "
        "la estación base puede representarse como:"
    )
    st.latex(
        r"\mathbf{m}_k = \big(\, t_k,\ \hat{\mathbf{p}}_k,\ \mathbf{s}_k \,\big)"
    )
    st.markdown(
        "donde $t_k$ es la marca de tiempo, $\\hat{\\mathbf{p}}_k$ la posición "
        "estimada y $\\mathbf{s}_k$ las mediciones de los sensores. De este modo, "
        "la estación base dispone de la ubicación y de la condición del objeto "
        "de forma simultánea."
    )

st.caption(
    "Los modelos presentados son simplificaciones con fines didácticos. Los sistemas "
    "reales incorporan filtrado (por ejemplo, Kalman), calibración y fusión de sensores."
)
