from os import cpu_count

import pandas
import streamlit as st
from ecoindex.models.compute import WindowSize
from ecoindex.scraper.helper import bulk_analysis
from loguru import logger

st.set_page_config(
    page_title="Ecoindex",
    page_icon="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.866em%22 font-size=%22100%22>🟢</text></svg>",
    initial_sidebar_state="auto",
)
st.title("Ecoindex")

tab_local, tab_website = st.tabs(["Ecoindex Local", "Ecoindex.fr"])

form_container = tab_local.container()
results_container = tab_local.container()
form_container.header("Lancer une analyse")

try:
    import playwright  # noqa

except ImportError:
    st.toast("Playwright n'est pas installé", icon="⚠️")
    st.info("Pour configurer Playwright, veuillez suivre les instructions suivantes:")
    st.code(
        """
        python -m playwright install
        """
    )

    st.stop()


def run_analysis(
    urls: str,
    sizes: list[tuple[int, int]],
    wait_before_scroll: int,
    wait_after_scroll: int,
):
    analysis_results = bulk_analysis(
        max_workers=cpu_count(),
        urls=urls.splitlines(),
        window_sizes=[WindowSize(width=w, height=h) for w, h in sizes],
        logger=logger,
        wait_before_scroll=wait_before_scroll,
        wait_after_scroll=wait_after_scroll,
    )
    analysis = []
    nb_analysis = len(urls.splitlines()) * len(sizes)
    progress_bar = results_container.progress(
        0, text=f"{nb_analysis} analyse en cours..."
    )

    for i, (result, error) in enumerate(analysis_results):
        progress_bar.progress((i + 1) / nb_analysis)
        analysis.append({**result.__dict__, "error": error})

    progress_bar.empty()

    df = pandas.DataFrame(analysis)
    # Apply colors on error column style
    # df.style.applymap(lambda x: "color: red" if x else "", subset=["error"])

    # Apply colors on grade column
    colors = {
        "A": "#349A47",
        "B": "#51B84B",
        "C": "#CADB2A",
        "D": "#F6EB15",
        "E": "#FECD06",
        "F": "#F99839",
        "G": "#ED2124",
    }
    # df = df.style.applymap(
    #     lambda x: f"color: {colors[x]}" if x else "", subset=["grade"]
    # )

    results_container.header("Résultats de l'analyse")
    results_container.dataframe(
        df,
        use_container_width=True,
        column_config={
            "url": st.column_config.LinkColumn(
                "Url",
                help="Url analysée",
            ),
            "width": st.column_config.NumberColumn(
                "Largeur",
                help="Largeur de la fenêtre en pixels",
                step=1,
                format="%d",
            ),
            "height": st.column_config.NumberColumn(
                "Hauteur",
                help="Hauteur de la fenêtre en pixels",
                step=1,
                format="%d",
            ),
            "size": st.column_config.NumberColumn(
                "Taille",
                help="Taille de la page en kilo octets",
                step=0.1,
                format="%fKo",
            ),
            "nodes": st.column_config.NumberColumn(
                "Noeuds",
                help="Nombre de noeuds HTML",
                step=1,
                format="%d",
            ),
            "requests": st.column_config.NumberColumn(
                "Requêtes",
                help="Nombre de requêtes HTTP",
                step=1,
                format="%d",
            ),
            "grade": st.column_config.TextColumn(
                "Grade",
                help="Grade Ecoindex",
            ),
            "score": st.column_config.ProgressColumn(
                "Score",
                help="Score Ecoindex",
                min_value=0,
                max_value=100,
                format="%f",
            ),
            "ges": st.column_config.NumberColumn(
                "GES",
                help="Emissions de GES équivalent en grammes",
                step=0.01,
                format="%fg",
            ),
            "water": st.column_config.NumberColumn(
                "Eau",
                help="Consommation d'eau équivalente en litres",
                step=0.01,
                format="%fl",
            ),
            "ecoindex_version": st.column_config.TextColumn(
                "Version",
                help="Version de l'Ecoindex",
            ),
            "date": st.column_config.DateColumn(
                "Date",
                help="Date de l'analyse",
                format="D/M/Y H:m:s",
            ),
            "page_type": st.column_config.TextColumn(
                "Type",
                help="Type de page",
                disabled=True,
            ),
            "error": st.column_config.TextColumn(
                "Erreur",
                help="Erreur lors de l'analyse",
            ),
        },
        hide_index=True,
    )


with form_container.form("ecoindex_analyzis"):
    urls = st.text_area(
        label="Urls à analyser",
        value="https://www.ecoindex.fr",
        help="Une url par ligne",
    )
    sizes = st.multiselect(
        label="Tailles de fenêtre",
        options=[(1920, 1080), (1280, 720), (800, 600)],
        default=[(1920, 1080)],
    )

    with st.expander("Options"):
        col1, col2 = st.columns(2)
        wait_before_scroll = col1.number_input(
            label="Attendre avant de scroller",
            value=3,
            min_value=0,
            help="Temps d'attente avant de scroller en secondes pour que la page se charge complètement",
        )

        wait_after_scroll = col2.number_input(
            label="Attendre après avoir scrollé",
            value=3,
            min_value=0,
            help="Temps d'attente après avoir scrollé en secondes pour que la page se charge complètement",
        )
        basic_auth = st.text_input(label="Authentification de base", disabled=True)
        session_cookie = st.text_input(label="Cookie de session", disabled=True)

    submitted = st.form_submit_button(
        label="Lancer l'analyse",
    )

    if submitted:
        run_analysis(
            urls=urls,
            sizes=sizes,
            wait_before_scroll=wait_before_scroll,
            wait_after_scroll=wait_after_scroll,
        )


container_website_search = tab_website.container()
container_website_results = tab_website.container()

container_website_search.header("Rechercher un résultat d'analyse")
