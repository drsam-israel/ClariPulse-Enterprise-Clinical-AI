import streamlit as st


def render_metric_cards(metrics: list[dict], columns: int = 4) -> None:
    """Render enterprise KPI cards with automatic row wrapping."""

    for start in range(0, len(metrics), columns):
        row_metrics = metrics[start:start + columns]
        cols = st.columns(len(row_metrics), gap="large")

        for col, metric in zip(cols, row_metrics):
            with col:
                label = str(metric.get("label", ""))
                value = str(metric.get("value", ""))

                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p style="color:#64748B; font-size:15px; font-weight:700; margin-bottom:10px;">
                            {label}
                        </p>
                        <p style="color:#0B2E4A; font-size:26px; font-weight:700; line-height:1.2; margin:0;">
                            {value}
                        </p>
                        """,
                        unsafe_allow_html=True,
                    )