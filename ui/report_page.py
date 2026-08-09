from pathlib import Path
import tempfile

import streamlit as st

from services.map_service import (
    create_static_farm_map,
)

from services.report_service import (
    generate_pdf_report,
)


def render_report_page():

    st.title("📄 Agricultural Field Report")

    farm = st.session_state.get(
        "farm_data"
    )

    results = st.session_state.get(
        "analysis_results"
    )

    recommendations = (
        st.session_state.get(
            "recommendations"
        )
    )

    if not farm:

        st.warning(
            "Complete Farm Data Input first."
        )

        return

    if not results:

        st.warning(
            "Run the Dashboard analysis first."
        )

        return

    if recommendations is None:

        from core.recommendations import (
            generate_recommendations,
        )

        weather = results["weather"]
        ndvi = results["ndvi"]

        recommendations = (
            generate_recommendations(
                crop=farm["crop"],
                ndvi=ndvi["mean_ndvi"],
                temperature=weather[
                    "temperature_c"
                ],
                humidity=weather[
                    "humidity_percent"
                ],
                rainfall=weather[
                    "rainfall_today_mm"
                ],
                irrigation_type=farm[
                    "irrigation_type"
                ],
            )
        )

        st.session_state.recommendations = (
            recommendations
        )

    if st.button(
        "📑 Generate Complete PDF Report",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Preparing report..."
        ):

            temp_dir = Path(
                tempfile.mkdtemp()
            )

            map_path = (
                temp_dir
                / "farm_location.png"
            )

            pdf_path = (
                temp_dir
                / "AgriDSS_Field_Report.pdf"
            )

            create_static_farm_map(
                farm["latitude"],
                farm["longitude"],
                str(map_path),
            )

            generate_pdf_report(
                farm=farm,
                weather=results["weather"],
                ndvi=results["ndvi"],
                recommendations=recommendations,
                map_path=str(map_path),
                output_path=str(pdf_path),
            )

            pdf_bytes = pdf_path.read_bytes()

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name="AgriDSS_Field_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            st.success(
                "Report generated successfully."
            )
