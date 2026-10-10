import streamlit as st
import pandas as pd
import numpy as np
import io

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Plateforme d'analyse statistique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 25px;
}

.section-title {
    font-size: 23px;
    font-weight: 650;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITRE
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 Plateforme d’analyse statistique et de Machine Learning'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Électricité • Emploi • Entrepreneuriat'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INITIALISATION DES VARIABLES
# ============================================================

if "emploi" not in st.session_state:
    st.session_state.emploi = None

if "energie" not in st.session_state:
    st.session_state.energie = None

if "data" not in st.session_state:
    st.session_state.data = None

if "emploi_name" not in st.session_state:
    st.session_state.emploi_name = None

if "energie_name" not in st.session_state:
    st.session_state.energie_name = None

if "fusion_effectuee" not in st.session_state:
    st.session_state.fusion_effectuee = False


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Choisir une fonctionnalité",
    [
        "🏠 Accueil",
        "📂 Importation & Fusion",
        "🔎 Diagnostic",
        "👀 Aperçu des données",
        "📋 Informations variables",
        "❌ Valeurs manquantes",
        "🔁 Doublons",
        "📊 Statistiques descriptives",
        "📁 Export",
        "🧹 Nettoyage interactif",
        "📈 Analyse exploratoire (Étape 3)",
        "🤖 Machine Learning (Étape 4)",
        "🔮 Prédiction interactive (Étape 5)",
        "📦 Export complet (Étape 6)"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Étape 1 : importation, fusion et diagnostic initial."
)


# ============================================================
# FONCTION DE LECTURE
# ============================================================

def lire_fichier(fichier):

    extension = fichier.name.split(".")[-1].lower()

    try:

        if extension == "xlsx":

            df = pd.read_excel(
                fichier,
                engine="openpyxl"
            )

        elif extension == "csv":

            try:
                df = pd.read_csv(fichier)

            except UnicodeDecodeError:

                fichier.seek(0)

                df = pd.read_csv(
                    fichier,
                    encoding="latin1"
                )

        else:

            st.error(
                "Format non supporté. "
                "Utilisez un fichier Excel (.xlsx) ou CSV (.csv)."
            )

            return None

        return df

    except Exception as e:

        st.error(
            f"Erreur lors de la lecture du fichier : {e}"
        )

        return None


# ============================================================
# FONCTION DE NORMALISATION DES NOMS DE COLONNES
# ============================================================

def normaliser_colonnes(df):

    df = df.copy()

    # Suppression des espaces inutiles
    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    return df


# ============================================================
# FONCTION DE FUSION
# ============================================================

def fusionner_bases(emploi, energie):

    emploi = emploi.copy()
    energie = energie.copy()

    # --------------------------------------------------------
    # Clés utilisées dans ton travail
    # --------------------------------------------------------

    cles = [
        "ID",
        "strate",
        "DÉPARTE",
        "mileu_rÃ©sidence",
        "age",
        "sexe"
    ]

    # Vérification des clés
    cles_emploi = [
        c for c in cles
        if c in emploi.columns
    ]

    cles_energie = [
        c for c in cles
        if c in energie.columns
    ]

    if len(cles_emploi) != len(cles):
        manque = [
            c for c in cles
            if c not in emploi.columns
        ]

        return None, (
            "Clé(s) absente(s) de la base Emploi : "
            + ", ".join(manque)
        )

    if len(cles_energie) != len(cles):
        manque = [
            c for c in cles
            if c not in energie.columns
        ]

        return None, (
            "Clé(s) absente(s) de la base Énergie : "
            + ", ".join(manque)
        )

    # --------------------------------------------------------
    # Vérification des doublons sur les clés
    # --------------------------------------------------------

    doublons_emploi = emploi.duplicated(
        subset=cles,
        keep=False
    ).sum()

    doublons_energie = energie.duplicated(
        subset=cles,
        keep=False
    ).sum()

    # --------------------------------------------------------
    # Fusion
    # --------------------------------------------------------

    data = pd.merge(
        emploi,
        energie,
        on=cles,
        how="inner",
        suffixes=("_emploi", "_energie")
    )

    # --------------------------------------------------------
    # Renommage des colonnes
    # --------------------------------------------------------

    renommage = {
        "mileu_rÃ©sidence": "milieu_residence",
        "activitÃ©s": "activites",
        "DÉPARTE": "departement",
        "entreprenariat": "entrepreneuriat"
    }

    data = data.rename(
        columns=renommage
    )

    informations = {
        "doublons_cles_emploi": doublons_emploi,
        "doublons_cles_energie": doublons_energie
    }

    return data, informations


# ============================================================
# PAGE ACCUEIL
# ============================================================

if page == "🏠 Accueil":

    st.markdown(
        '<div class="section-title">Bienvenue</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        Cette application est destinée à réaliser une analyse
        statistique et une modélisation Machine Learning à partir
        des données relatives à l'emploi, à l'entrepreneuriat et
        à l'accès à l'électricité au Sénégal.
        """
    )

    st.markdown("### 🔄 Fonctionnement")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            **1 — Importation**

            Importer simultanément les deux bases :
            
            • Travail et emploi
            
            • Utilisation de l'énergie
            """
        )

    with col2:

        st.info(
            """
            **2 — Fusion**

            Les deux bases sont fusionnées
            à partir des identifiants communs.
            """
        )

    with col3:

        st.info(
            """
            **3 — Diagnostic**

            Vérification des dimensions,
            variables, valeurs manquantes
            et doublons.
            """
        )

    st.markdown("---")

    st.markdown("### 🚀 Étapes suivantes")

    st.write(
        """
        Après cette étape, l'application sera progressivement
        complétée avec :

        **Étape 2 :** nettoyage interactif

        **Étape 3 :** analyse descriptive univariée, bivariée
        et multivariée

        **Étape 4 :** modèles Machine Learning

        **Étape 5 :** prédiction interactive
        """
    )


# ============================================================
# IMPORTATION ET FUSION
# ============================================================

elif page == "📂 Importation & Fusion":

    st.markdown(
        '<div class="section-title">'
        '📂 Importation des deux bases'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        Importez les deux bases nécessaires à votre étude.
        Les deux fichiers sont conservés séparément avant
        la fusion.
        """
    )

    # --------------------------------------------------------
    # BASE EMPLOI
    # --------------------------------------------------------

    st.subheader("1️⃣ Base Travail et Emploi")

    fichier_emploi = st.file_uploader(
        "Importer la base Travail et Emploi",
        type=["xlsx", "csv"],
        key="upload_emploi"
    )

    if fichier_emploi is not None:

        df_emploi = lire_fichier(fichier_emploi)

        if df_emploi is not None:

            df_emploi = normaliser_colonnes(
                df_emploi
            )

            st.session_state.emploi = df_emploi
            st.session_state.emploi_name = (
                fichier_emploi.name
            )

            st.success(
                f"Base Emploi chargée : "
                f"{fichier_emploi.name}"
            )

    # --------------------------------------------------------
    # BASE ENERGIE
    # --------------------------------------------------------

    st.subheader("2️⃣ Base Utilisation de l'énergie")

    fichier_energie = st.file_uploader(
        "Importer la base Utilisation de l'énergie",
        type=["xlsx", "csv"],
        key="upload_energie"
    )

    if fichier_energie is not None:

        df_energie = lire_fichier(
            fichier_energie
        )

        if df_energie is not None:

            df_energie = normaliser_colonnes(
                df_energie
            )

            st.session_state.energie = df_energie
            st.session_state.energie_name = (
                fichier_energie.name
            )

            st.success(
                f"Base Énergie chargée : "
                f"{fichier_energie.name}"
            )

    # --------------------------------------------------------
    # AFFICHAGE DES DEUX BASES
    # --------------------------------------------------------

    if (
        st.session_state.emploi is not None
        and
        st.session_state.energie is not None
    ):

        st.markdown("---")

        st.subheader("📊 Résumé des deux bases")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### 👷 Base Emploi")

            st.write(
                f"Fichier : "
                f"`{st.session_state.emploi_name}`"
            )

            st.metric(
                "Lignes",
                f"{st.session_state.emploi.shape[0]:,}"
            )

            st.metric(
                "Colonnes",
                f"{st.session_state.emploi.shape[1]:,}"
            )

        with col2:

            st.write("### ⚡ Base Énergie")

            st.write(
                f"Fichier : "
                f"`{st.session_state.energie_name}`"
            )

            st.metric(
                "Lignes",
                f"{st.session_state.energie.shape[0]:,}"
            )

            st.metric(
                "Colonnes",
                f"{st.session_state.energie.shape[1]:,}"
            )

        # ----------------------------------------------------
        # APERÇU DES COLONNES
        # ----------------------------------------------------

        with st.expander("🔎 Voir les colonnes de la base Emploi"):

            st.write(
                st.session_state.emploi.columns.tolist()
            )

        with st.expander("🔎 Voir les colonnes de la base Énergie"):

            st.write(
                st.session_state.energie.columns.tolist()
            )

        st.markdown("---")

        # ----------------------------------------------------
        # BOUTON DE FUSION
        # ----------------------------------------------------

        st.subheader("🔗 Fusion des bases")

        st.write(
            """
            La fusion utilise les six variables communes
            suivantes :
            """
        )

        st.code(
            """
ID
strate
DÉPARTE
mileu_rÃ©sidence
age
sexe
            """
        )

        fusionner = st.button(
            "🔗 Fusionner les deux bases",
            type="primary",
            use_container_width=True
        )

        if fusionner:

            data, resultat = fusionner_bases(
                st.session_state.emploi,
                st.session_state.energie
            )

            if data is None:

                st.error(
                    resultat
                )

            else:

                st.session_state.data = data
                # Réinitialiser la base nettoyée lors d'une nouvelle fusion
                st.session_state.data_clean = data.copy()
                st.session_state.data_original_cleaning = data.copy()

                st.session_state.fusion_effectuee = True

                st.success(
                    "✅ Fusion réalisée avec succès !"
                )

                # --------------------------------------------
                # INFORMATIONS FUSION
                # --------------------------------------------

                st.markdown("### 📊 Résultat de la fusion")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Base Emploi",
                        f"{len(st.session_state.emploi):,}"
                    )

                with col2:

                    st.metric(
                        "Base Énergie",
                        f"{len(st.session_state.energie):,}"
                    )

                with col3:

                    st.metric(
                        "Base fusionnée",
                        f"{len(data):,}"
                    )

                st.write(
                    f"**Nombre de colonnes après fusion : "
                    f"{data.shape[1]}**"
                )

                # --------------------------------------------
                # DOUBLONS SUR LES CLES
                # --------------------------------------------

                st.markdown(
                    "### 🔑 Vérification des clés"
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.metric(
                        "Doublons des clés - Emploi",
                        resultat[
                            "doublons_cles_emploi"
                        ]
                    )

                with c2:

                    st.metric(
                        "Doublons des clés - Énergie",
                        resultat[
                            "doublons_cles_energie"
                        ]
                    )

                # --------------------------------------------
                # APERCU
                # --------------------------------------------

                st.markdown(
                    "### 👀 Aperçu de la base fusionnée"
                )

                st.dataframe(
                    data.head(10),
                    use_container_width=True
                )

    else:

        st.info(
            "Importez les deux bases pour pouvoir effectuer "
            "la fusion."
        )


# ============================================================
# DIAGNOSTIC
# ============================================================

elif page == "🔎 Diagnostic":

    st.markdown(
        '<div class="section-title">'
        '🔎 Diagnostic de la base fusionnée'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord importer et fusionner "
            "les deux bases."
        )

    else:

        data = st.session_state.data

        # ----------------------------------------------------
        # INDICATEURS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Observations",
                f"{data.shape[0]:,}"
            )

        with col2:

            st.metric(
                "Variables",
                f"{data.shape[1]:,}"
            )

        with col3:

            st.metric(
                "Valeurs manquantes",
                f"{data.isna().sum().sum():,}"
            )

        with col4:

            st.metric(
                "Doublons complets",
                f"{data.duplicated().sum():,}"
            )

        st.markdown("---")

        # ----------------------------------------------------
        # TYPES
        # ----------------------------------------------------

        st.subheader("📋 Types de variables")

        types = pd.DataFrame({
            "Variable": data.columns,
            "Type": data.dtypes.astype(str).values,
            "Valeurs uniques": [
                data[col].nunique(dropna=True)
                for col in data.columns
            ],
            "Manquants": [
                data[col].isna().sum()
                for col in data.columns
            ],
            "% manquants": [
                round(
                    data[col].isna().mean() * 100,
                    2
                )
                for col in data.columns
            ]
        })

        st.dataframe(
            types,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# APERÇU DES DONNEES
# ============================================================

elif page == "👀 Aperçu des données":

    st.markdown(
        '<div class="section-title">'
        '👀 Aperçu de la base fusionnée'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord fusionner les deux bases."
        )

    else:

        data = st.session_state.data

        n = st.number_input(
            "Nombre de lignes à afficher",
            min_value=1,
            max_value=len(data),
            value=min(20, len(data)),
            step=1
        )

        st.dataframe(
            data.head(int(n)),
            use_container_width=True
        )


# ============================================================
# INFORMATIONS VARIABLES
# ============================================================

elif page == "📋 Informations variables":

    st.markdown(
        '<div class="section-title">'
        '📋 Informations sur les variables'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord fusionner les deux bases."
        )

    else:

        data = st.session_state.data

        informations = pd.DataFrame({
            "Variable": data.columns,
            "Type": data.dtypes.astype(str),
            "Non nuls": data.notna().sum(),
            "Manquants": data.isna().sum(),
            "% manquants": (
                data.isna().mean() * 100
            ).round(2),
            "Valeurs uniques": [
                data[col].nunique(dropna=True)
                for col in data.columns
            ]
        })

        st.dataframe(
            informations,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# VALEURS MANQUANTES
# ============================================================

elif page == "❌ Valeurs manquantes":

    st.markdown(
        '<div class="section-title">'
        '❌ Valeurs manquantes'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord fusionner les deux bases."
        )

    else:

        data = st.session_state.data

        missing = pd.DataFrame({
            "Variable": data.columns,
            "Nombre": data.isna().sum(),
            "Pourcentage (%)": (
                data.isna().mean() * 100
            ).round(2)
        })

        missing = missing[
            missing["Nombre"] > 0
        ].sort_values(
            "Nombre",
            ascending=False
        )

        if missing.empty:

            st.success(
                "Aucune valeur manquante."
            )

        else:

            st.dataframe(
                missing,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# DOUBLONS
# ============================================================

elif page == "🔁 Doublons":

    st.markdown(
        '<div class="section-title">'
        '🔁 Doublons'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord fusionner les deux bases."
        )

    else:

        data = st.session_state.data

        doublons = data.duplicated().sum()

        st.metric(
            "Nombre de doublons complets",
            f"{doublons:,}"
        )

        if doublons == 0:

            st.success(
                "Aucun doublon complet détecté."
            )

        else:

            st.warning(
                f"{doublons} doublon(s) détecté(s)."
            )

            st.dataframe(
                data[data.duplicated(keep=False)],
                use_container_width=True
            )


# ============================================================
# STATISTIQUES DESCRIPTIVES
# ============================================================

elif page == "📊 Statistiques descriptives":

    st.markdown(
        '<div class="section-title">'
        '📊 Statistiques descriptives'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Veuillez d'abord fusionner les deux bases."
        )

    else:

        data = st.session_state.data

        # NUMERIQUES
        st.subheader(
            "🔢 Variables quantitatives"
        )

        quantitatives = data.select_dtypes(
            include=np.number
        ).columns.tolist()

        if quantitatives:

            stats = data[
                quantitatives
            ].describe().T

            stats["Asymétrie"] = [
                data[col].skew()
                for col in quantitatives
            ]

            st.dataframe(
                stats.round(3),
                use_container_width=True
            )

        else:

            st.info(
                "Aucune variable quantitative détectée."
            )

        st.markdown("---")

        # QUALITATIVES
        st.subheader(
            "🔤 Variables qualitatives"
        )

        qualitatives = data.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        if qualitatives:

            variable = st.selectbox(
                "Sélectionner une variable",
                qualitatives
            )

            frequences = (
                data[variable]
                .value_counts(dropna=False)
                .rename_axis("Modalité")
                .reset_index(name="Effectif")
            )

            frequences[
                "Pourcentage (%)"
            ] = (
                frequences["Effectif"]
                / frequences["Effectif"].sum()
                * 100
            ).round(2)

            st.dataframe(
                frequences,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# EXPORT
# ============================================================

elif page == "📁 Export":

    st.markdown(
        '<div class="section-title">'
        '📁 Export'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.data is None:

        st.warning(
            "Aucune base fusionnée disponible."
        )

    else:

        data = st.session_state.data

        st.success(
            "La base fusionnée est prête à être exportée."
        )

        # CSV
        csv = data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Télécharger la base fusionnée en CSV",
            csv,
            "data_fusionnee.csv",
            "text/csv",
            use_container_width=True
        )

        # EXCEL
        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            data.to_excel(
                writer,
                index=False,
                sheet_name="Data"
            )

        excel = output.getvalue()

        st.download_button(
            "⬇️ Télécharger la base fusionnée en Excel",
            excel,
            "data_fusionnee.xlsx",
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet",
            use_container_width=True
        )

elif page == "🧹 Nettoyage interactif":

    st.title("🧹 Étape 2 — Nettoyage interactif des données")

    st.markdown("""
    Cette étape permet de préparer la base de données avant les analyses
    statistiques et les modèles de Machine Learning.
    """)

    # ============================================================
    # VERIFICATION DE LA BASE
    # ============================================================

    if (
        "data" not in st.session_state
        or not isinstance(st.session_state.data, pd.DataFrame)
    ):
        st.warning(
            "Veuillez d'abord aller dans « Importation & Fusion », "
            "charger les deux bases et cliquer sur « Fusionner les deux bases »."
        )
        st.stop()

    # ============================================================
    # INITIALISATION DE LA BASE NETTOYEE
    # ============================================================

    if (
        "data_clean" not in st.session_state
        or not isinstance(st.session_state.data_clean, pd.DataFrame)
    ):
        st.session_state.data_clean = st.session_state.data.copy()

    if (
        "data_original_cleaning" not in st.session_state
        or not isinstance(st.session_state.data_original_cleaning, pd.DataFrame)
    ):
        st.session_state.data_original_cleaning = st.session_state.data.copy()

    data = st.session_state.data_clean

    # ============================================================
    # VARIABLES IMPORTANTES
    # ============================================================

    # Variables dépendantes
    targets = [
        "travail",
        "entrepreneuriat"
    ]

    # Variables monétaires / dépenses pour transformation logarithmique
    variables_log_defaut = [
        "Impots_taxes",
        "transfertsArgents",
        "dep_gaz",
        "dep_charbon",
        "dep_bois",
        "dep_bougiepetrol",
        "dep_elec",
        "dep_carburant"
    ]

    # Variables quantitatives
    variables_quantitatives = data.select_dtypes(
        include=np.number
    ).columns.tolist()

    # ============================================================
    # SIDEBAR
    # ============================================================

    st.sidebar.header("🧹 Nettoyage")

    menu = st.sidebar.radio(
        "Choisir une opération",
        [
            "📊 État initial",
            "❌ Valeurs manquantes",
            "📈 Valeurs aberrantes",
            "🔢 Transformation logarithmique",
            "📊 Comparaison avant / après",
            "💾 Enregistrer / télécharger"
        ]
    )

    # ============================================================
    # 1. ETAT INITIAL
    # ============================================================

    if menu == "📊 État initial":

        st.header("📊 État initial de la base")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Nombre d'observations",
                f"{data.shape[0]:,}"
            )

        with col2:
            st.metric(
                "Nombre de variables",
                data.shape[1]
            )

        with col3:
            st.metric(
                "Valeurs manquantes",
                f"{data.isna().sum().sum():,}"
            )

        with col4:
            st.metric(
                "Variables numériques",
                len(variables_quantitatives)
            )

        st.subheader("Aperçu de la base")

        st.dataframe(
            data.head(20),
            use_container_width=True
        )

        st.subheader("Types des variables")

        types_df = pd.DataFrame({
            "Variable": data.columns,
            "Type": data.dtypes.astype(str).values,
            "Valeurs manquantes": [
                data[col].isna().sum()
                for col in data.columns
            ]
        })

        st.dataframe(
            types_df,
            use_container_width=True
        )


    # ============================================================
    # 2. VALEURS MANQUANTES
    # ============================================================

    elif menu == "❌ Valeurs manquantes":

        st.header("❌ Traitement des valeurs manquantes")

        st.info("""
        **Règle appliquée :**

        • `travail` et `entrepreneuriat` sont les variables dépendantes :
          leurs valeurs manquantes sont conservées.

        • Pour les variables explicatives, les valeurs manquantes sont
          remplacées par `Non_renseigne`.
        """)

        # --------------------------------------------------------
        # TABLEAU AVANT TRAITEMENT
        # --------------------------------------------------------

        st.subheader("1️⃣ Situation avant traitement")

        missing_before = pd.DataFrame({
            "Variable": data.columns,
            "Valeurs manquantes": [
                data[col].isna().sum()
                for col in data.columns
            ],
            "Pourcentage (%)": [
                round(data[col].isna().mean() * 100, 2)
                for col in data.columns
            ]
        })

        missing_before = missing_before[
            missing_before["Valeurs manquantes"] > 0
        ]

        if len(missing_before) == 0:
            st.success("✅ Aucune valeur manquante dans la base.")
        else:
            st.dataframe(
                missing_before,
                use_container_width=True
            )

        # --------------------------------------------------------
        # VARIABLES DEPENDANTES
        # --------------------------------------------------------

        st.subheader("2️⃣ Variables dépendantes")

        target_missing = pd.DataFrame({
            "Variable": targets,
            "Valeurs manquantes": [
                data[col].isna().sum()
                if col in data.columns else 0
                for col in targets
            ],
            "Pourcentage (%)": [
                round(data[col].isna().mean() * 100, 2)
                if col in data.columns else 0
                for col in targets
            ]
        })

        st.dataframe(
            target_missing,
            use_container_width=True
        )

        st.warning("""
        ⚠️ Les valeurs manquantes des variables dépendantes ne sont pas
        remplacées par `Oui`, `Non` ou `Non_renseigne`.

        Elles seront simplement exclues lors de l'entraînement du modèle
        correspondant.
        """)

        # --------------------------------------------------------
        # VARIABLES EXPLICATIVES
        # --------------------------------------------------------

        st.subheader("3️⃣ Variables explicatives")

        variables_explicatives = [
            col for col in data.columns
            if col not in targets
        ]

        missing_predictors = {
            col: data[col].isna().sum()
            for col in variables_explicatives
            if data[col].isna().sum() > 0
        }

        if len(missing_predictors) == 0:

            st.success(
                "✅ Aucune valeur manquante dans les variables explicatives."
            )

        else:

            st.write(
                "Variables explicatives contenant des valeurs manquantes :"
            )

            st.dataframe(
                pd.DataFrame({
                    "Variable": list(missing_predictors.keys()),
                    "Valeurs manquantes": list(missing_predictors.values())
                }),
                use_container_width=True
            )

            if st.button(
                "🧹 Remplacer les valeurs manquantes",
                type="primary"
            ):

                nombre_remplace = 0

                for col in variables_explicatives:

                    nb_missing = data[col].isna().sum()

                    if nb_missing > 0:

                        # Pour les variables qualitatives
                        if (
                            data[col].dtype == "object"
                            or isinstance(
                                data[col].dtype,
                                pd.CategoricalDtype
                            )
                        ):

                            data[col] = data[col].fillna(
                                "Non_renseigne"
                            )

                            nombre_remplace += nb_missing

                        else:

                            # Cas particulier si une variable quantitative
                            # possède des valeurs manquantes.
                            #
                            # On la convertit en object afin de respecter
                            # la règle "Non_renseigne".
                            data[col] = data[col].astype(object)

                            data[col] = data[col].where(
                                data[col].notna(),
                                "Non_renseigne"
                            )

                            nombre_remplace += nb_missing

                st.session_state.data_clean = data

                st.success(
                    f"✅ {nombre_remplace:,} valeur(s) manquante(s) "
                    "ont été remplacées par `Non_renseigne`."
                )

                st.rerun()

        # --------------------------------------------------------
        # CONTROLE APRES
        # --------------------------------------------------------

        st.subheader("4️⃣ Contrôle après traitement")

        missing_after = pd.DataFrame({
            "Variable": data.columns,
            "Valeurs manquantes": [
                data[col].isna().sum()
                for col in data.columns
            ],
            "Pourcentage (%)": [
                round(data[col].isna().mean() * 100, 2)
                for col in data.columns
            ]
        })

        missing_after = missing_after[
            missing_after["Valeurs manquantes"] > 0
        ]

        if len(missing_after) == 0:

            st.success(
                "✅ Il ne reste aucune valeur manquante."
            )

        else:

            st.dataframe(
                missing_after,
                use_container_width=True
            )


    # ============================================================
    # 3. DETECTION DES VALEURS ABERRANTES
    # ============================================================

    elif menu == "📈 Valeurs aberrantes":

        st.header("📈 Détection des valeurs aberrantes")

        st.info("""
        La méthode utilisée est la méthode de l'**écart interquartile (IQR)**.

        Une observation est considérée comme aberrante si :

        **x < Q1 − 1,5 × IQR**

        ou

        **x > Q3 + 1,5 × IQR**
        """)

        # Sélection des variables numériques
        variables_num = [
            col for col in data.columns
            if pd.api.types.is_numeric_dtype(data[col])
        ]

        # Exclusion éventuelle de ID
        variables_num_analyse = [
            col for col in variables_num
            if col != "ID"
        ]

        resultats_iqr = []

        for col in variables_num_analyse:

            serie = pd.to_numeric(
                data[col],
                errors="coerce"
            ).dropna()

            if len(serie) == 0:
                continue

            q1 = serie.quantile(0.25)
            q3 = serie.quantile(0.75)

            iqr = q3 - q1

            borne_inf = q1 - 1.5 * iqr
            borne_sup = q3 + 1.5 * iqr

            nb_outliers = (
                (serie < borne_inf) |
                (serie > borne_sup)
            ).sum()

            pourcentage = (
                nb_outliers / len(serie)
            ) * 100

            resultats_iqr.append({
                "Variable": col,
                "Q1": q1,
                "Q3": q3,
                "IQR": iqr,
                "Borne inférieure": borne_inf,
                "Borne supérieure": borne_sup,
                "Nombre aberrant": nb_outliers,
                "Pourcentage (%)": pourcentage
            })

        iqr_df = pd.DataFrame(resultats_iqr)

        if len(iqr_df) > 0:

            iqr_df = iqr_df.sort_values(
                "Nombre aberrant",
                ascending=False
            )

            # Arrondi
            iqr_affichage = iqr_df.copy()

            colonnes_num = [
                "Q1",
                "Q3",
                "IQR",
                "Borne inférieure",
                "Borne supérieure",
                "Pourcentage (%)"
            ]

            iqr_affichage[colonnes_num] = (
                iqr_affichage[colonnes_num]
                .round(2)
            )

            st.dataframe(
                iqr_affichage,
                use_container_width=True
            )

        # --------------------------------------------------------
        # EXPLICATION
        # --------------------------------------------------------

        st.subheader("📌 Interprétation")

        st.write("""
        Les valeurs aberrantes ne sont pas supprimées de la base.

        Pour les variables monétaires et les dépenses énergétiques,
        une transformation logarithmique sera proposée dans la rubrique
        **Transformation logarithmique**.

        La variable `age` est également contrôlée par la méthode IQR,
        mais elle n'est pas transformée logarithmiquement.
        """)

        # Cas particulier carburant
        if "dep_carburant" in data.columns:

            st.warning("""
            ⚠️ `dep_carburant` possède Q1 = 0 et Q3 = 0.
            Son IQR est donc égal à 0. Les valeurs positives sont alors
            considérées comme aberrantes selon la règle IQR.

            La transformation `log1p` peut réduire fortement son asymétrie,
            mais elle ne fera pas nécessairement disparaître le statut
            d'aberration selon l'IQR.
            """)


    # ============================================================
    # 4. TRANSFORMATION LOGARITHMIQUE
    # ============================================================

    elif menu == "🔢 Transformation logarithmique":

        st.header("🔢 Transformation logarithmique")

        st.info("""
        La transformation utilisée est :

        **log(x) = log(1 + x)**

        Elle est appliquée avec `np.log1p()`.

        L'objectif est de réduire l'asymétrie des variables monétaires
        et des dépenses très dispersées.
        """)

        # Variables disponibles
        variables_disponibles = [
            col for col in variables_log_defaut
            if col in data.columns
        ]

        # Sélection utilisateur
        variables_selectionnees = st.multiselect(
            "Choisir les variables à transformer",
            variables_disponibles,
            default=variables_disponibles
        )

        remplacer_original = st.checkbox(
            "Remplacer la variable originale par sa version logarithmique",
            value=False
        )

        if remplacer_original:

            st.warning("""
            ⚠️ La variable originale sera remplacée par sa transformation
            logarithmique. Il est généralement préférable de conserver
            la variable originale et de créer une variable `_log`.
            """)

        if st.button(
            "🔄 Appliquer la transformation logarithmique",
            type="primary"
        ):

            if len(variables_selectionnees) == 0:

                st.warning(
                    "Veuillez sélectionner au moins une variable."
                )

            else:

                transformations_effectuees = []

                for col in variables_selectionnees:

                    serie = pd.to_numeric(
                        data[col],
                        errors="coerce"
                    )

                    # Vérification des valeurs négatives
                    if (serie.dropna() < 0).any():

                        st.error(
                            f"❌ {col} contient des valeurs négatives. "
                            "La transformation log1p n'est pas appliquée."
                        )

                        continue

                    # Nom de la nouvelle variable
                    nouvelle_colonne = col + "_log"

                    # Transformation
                    data[nouvelle_colonne] = np.log1p(serie)

                    # Option remplacement
                    if remplacer_original:

                        data[col] = data[nouvelle_colonne]

                        # Suppression de la colonne _log
                        data.drop(
                            columns=[nouvelle_colonne],
                            inplace=True
                        )

                    transformations_effectuees.append(col)

                st.session_state.data_clean = data

                if len(transformations_effectuees) > 0:

                    st.success(
                        "✅ Transformation logarithmique effectuée pour : "
                        + ", ".join(transformations_effectuees)
                    )

                st.rerun()

        # --------------------------------------------------------
        # TABLEAU DES SKEWNESS
        # --------------------------------------------------------

        st.subheader("📊 Asymétrie avant / après")

        lignes = []

        for col in variables_selectionnees:

            if col not in data.columns:
                continue

            serie_avant = pd.to_numeric(
                st.session_state.data_original_cleaning[col],
                errors="coerce"
            )

            # Version log
            log_col = col + "_log"

            if log_col in data.columns:

                serie_apres = pd.to_numeric(
                    data[log_col],
                    errors="coerce"
                )

            else:

                # Si remplacement de la variable originale
                serie_apres = pd.to_numeric(
                    data[col],
                    errors="coerce"
                )

            lignes.append({
                "Variable": col,
                "Asymétrie avant": serie_avant.skew(),
                "Asymétrie après": serie_apres.skew()
            })

        if len(lignes) > 0:

            skew_df = pd.DataFrame(lignes)

            skew_df[
                ["Asymétrie avant", "Asymétrie après"]
            ] = skew_df[
                ["Asymétrie avant", "Asymétrie après"]
            ].round(4)

            st.dataframe(
                skew_df,
                use_container_width=True
            )


    # ============================================================
    # 5. COMPARAISON AVANT / APRES
    # ============================================================

    elif menu == "📊 Comparaison avant / après":

        st.header("📊 Comparaison avant / après nettoyage")

        data_original = st.session_state.data_original_cleaning
        data_clean = st.session_state.data_clean

        # --------------------------------------------------------
        # DIMENSIONS
        # --------------------------------------------------------

        st.subheader("1️⃣ Dimensions")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Base originale",
                f"{data_original.shape[0]:,} lignes × "
                f"{data_original.shape[1]} variables"
            )

        with col2:

            st.metric(
                "Base nettoyée",
                f"{data_clean.shape[0]:,} lignes × "
                f"{data_clean.shape[1]} variables"
            )

        # --------------------------------------------------------
        # VALEURS MANQUANTES
        # --------------------------------------------------------

        st.subheader("2️⃣ Valeurs manquantes")

        missing_comparison = []

        for col in data_original.columns:

            if col in data_clean.columns:

                avant = data_original[col].isna().sum()
                apres = data_clean[col].isna().sum()

                missing_comparison.append({
                    "Variable": col,
                    "Avant": avant,
                    "Après": apres,
                    "Différence": apres - avant
                })

        missing_df = pd.DataFrame(
            missing_comparison
        )

        missing_df = missing_df[
            (missing_df["Avant"] > 0) |
            (missing_df["Après"] > 0)
        ]

        if len(missing_df) > 0:

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        else:

            st.success(
                "Aucune valeur manquante détectée."
            )

        # --------------------------------------------------------
        # SKEWNESS
        # --------------------------------------------------------

        st.subheader("3️⃣ Asymétrie des variables")

        lignes = []

        for col in variables_log_defaut:

            if col not in data_original.columns:
                continue

            serie_avant = pd.to_numeric(
                data_original[col],
                errors="coerce"
            )

            if col + "_log" in data_clean.columns:

                serie_apres = pd.to_numeric(
                    data_clean[col + "_log"],
                    errors="coerce"
                )

                lignes.append({
                    "Variable": col,
                    "Skewness avant": serie_avant.skew(),
                    "Skewness après": serie_apres.skew()
                })

        if len(lignes) > 0:

            skew_comparison = pd.DataFrame(lignes)

            skew_comparison[
                ["Skewness avant", "Skewness après"]
            ] = skew_comparison[
                ["Skewness avant", "Skewness après"]
            ].round(4)

            st.dataframe(
                skew_comparison,
                use_container_width=True
            )

        # --------------------------------------------------------
        # CIBLES
        # --------------------------------------------------------

        st.subheader("4️⃣ Contrôle des variables dépendantes")

        target_comparison = []

        for col in targets:

            if col in data_original.columns:

                target_comparison.append({
                    "Variable": col,
                    "Manquants avant": data_original[col].isna().sum(),
                    "Manquants après": data_clean[col].isna().sum()
                })

        st.dataframe(
            pd.DataFrame(target_comparison),
            use_container_width=True
        )

        st.success("""
        ✅ Les valeurs manquantes des variables dépendantes sont conservées.
        Elles ne sont donc pas artificiellement transformées en une modalité.
        """)


    # ============================================================
    # 6. ENREGISTREMENT / TELECHARGEMENT
    # ============================================================

    elif menu == "💾 Enregistrer / télécharger":

        st.header("💾 Enregistrer la base nettoyée")

        data_clean = st.session_state.data_clean

        st.subheader("📊 Résumé final")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Observations",
                f"{data_clean.shape[0]:,}"
            )

        with col2:
            st.metric(
                "Variables",
                data_clean.shape[1]
            )

        with col3:
            st.metric(
                "Valeurs manquantes",
                f"{data_clean.isna().sum().sum():,}"
            )

        # --------------------------------------------------------
        # APERCU
        # --------------------------------------------------------

        st.subheader("Aperçu")

        st.dataframe(
            data_clean.head(20),
            use_container_width=True
        )

        # --------------------------------------------------------
        # CSV
        # --------------------------------------------------------

        csv_data = data_clean.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=csv_data,
            file_name="base_nettoyee.csv",
            mime="text/csv"
        )

        # --------------------------------------------------------
        # EXCEL
        # --------------------------------------------------------

        buffer = io.BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            data_clean.to_excel(
                writer,
                index=False,
                sheet_name="Data"
            )

        buffer.seek(0)

        st.download_button(
            label="⬇️ Télécharger en Excel",
            data=buffer,
            file_name="base_nettoyee.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        st.success("""
        ✅ La base nettoyée est maintenant disponible dans
        `st.session_state.data_clean`.

        Elle pourra être utilisée directement pour les prochaines étapes :
        analyse univariée, bivariée, multivariée et Machine Learning.
        """)


    # ============================================================
    # BOUTON RESET
    # ============================================================

    st.sidebar.markdown("---")

    if st.sidebar.button("🔄 Réinitialiser le nettoyage"):

        st.session_state.data_clean = (
            st.session_state.data_original_cleaning.copy()
        )

        st.success(
            "✅ La base a été restaurée à son état initial."
        )

        st.rerun()


elif page == "📈 Analyse exploratoire (Étape 3)":

    st.title("📈 Étape 3 — Analyse exploratoire des données")
    st.markdown("""
    Explorez les distributions, les relations entre variables et les résultats
    des tests statistiques. Les tests sont choisis automatiquement selon le
    type des variables sélectionnées.
    """)

    # Utiliser la base nettoyée si elle existe, sinon la base fusionnée.
    if isinstance(st.session_state.get("data_clean"), pd.DataFrame):
        df_eda = st.session_state.data_clean.copy()
        source_label = "base nettoyée"
    elif isinstance(st.session_state.get("data"), pd.DataFrame):
        df_eda = st.session_state.data.copy()
        source_label = "base fusionnée (non nettoyée)"
    else:
        st.warning("Chargez et fusionnez d’abord les deux bases à l’étape 1.")
        st.stop()

    try:
        import plotly.express as px
        import plotly.graph_objects as go
        from scipy import stats
        from scipy.stats import chi2_contingency
    except ImportError:
        st.error("Installez les bibliothèques nécessaires : pip install plotly scipy")
        st.stop()

    st.caption(f"Source utilisée : {source_label} — {df_eda.shape[0]:,} lignes et {df_eda.shape[1]} colonnes")
    st.info("Les valeurs manquantes des variables choisies sont exclues uniquement pour le calcul ou le graphique concerné. Aucune valeur manquante de la cible entrepreneuriat n’est automatiquement transformée en ‘Non’.")

    # Détecter les types de variables sans supposer que toutes les colonnes sont bien typées.
    numeric_cols = df_eda.select_dtypes(include=np.number).columns.tolist()
    all_cols = df_eda.columns.tolist()
    categorical_cols = [c for c in all_cols if c not in numeric_cols]
    if not all_cols:
        st.warning("La base ne contient aucune colonne exploitable.")
        st.stop()

    tab_uni, tab_bi, tab_multi, tab_tests = st.tabs([
        "1. Univariée", "2. Bivariée", "3. Multivariée", "4. Tests statistiques"
    ])

    # -------------------- UNIVARIÉE --------------------
    with tab_uni:
        st.subheader("Analyse univariée")
        col_u, col_opt = st.columns([2, 1])
        with col_u:
            var_u = st.selectbox("Choisir une variable", all_cols, key="eda_uni_var")
        serie = df_eda[var_u].dropna()
        with col_opt:
            st.metric("Observations disponibles", f"{len(serie):,}")
            st.metric("Valeurs manquantes", f"{df_eda[var_u].isna().sum():,}")

        if var_u in numeric_cols:
            desc = serie.describe().to_frame(name="Valeur").round(4)
            st.dataframe(desc, use_container_width=True)
            c1, c2 = st.columns(2)
            with c1:
                fig = px.histogram(df_eda, x=var_u, marginal="rug", title=f"Distribution de {var_u}",
                                   nbins=30, opacity=0.8)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = px.box(df_eda, y=var_u, points="outliers", title=f"Boîte à moustaches — {var_u}")
                st.plotly_chart(fig, use_container_width=True)
            if len(serie) >= 3:
                st.write(f"**Médiane :** {serie.median():.4g}  |  **Écart-type :** {serie.std():.4g}  |  **Asymétrie :** {serie.skew():.4g}")
        else:
            freq = serie.astype(str).value_counts(dropna=False).rename_axis("Modalité").reset_index(name="Effectif")
            freq["Pourcentage (%)"] = (freq["Effectif"] / max(freq["Effectif"].sum(), 1) * 100).round(2)
            st.dataframe(freq, use_container_width=True)
            fig = px.bar(freq.head(40), x="Modalité", y="Effectif", text="Pourcentage (%)",
                         title=f"Répartition de {var_u}")
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

    # -------------------- BIVARIÉE --------------------
    with tab_bi:
        st.subheader("Analyse bivariée")
        c1, c2 = st.columns(2)
        with c1:
            var_x = st.selectbox("Variable X", all_cols, index=all_cols.index("acces_elec") if "acces_elec" in all_cols else 0, key="eda_bi_x")
        with c2:
            defaults_y = "travail" if "travail" in all_cols and var_x != "travail" else ("entrepreneuriat" if "entrepreneuriat" in all_cols and var_x != "entrepreneuriat" else all_cols[-1])
            var_y = st.selectbox("Variable Y", all_cols, index=all_cols.index(defaults_y), key="eda_bi_y")
        if var_x == var_y:
            st.warning("Choisissez deux variables différentes pour l’analyse bivariée.")
        else:
            pair = df_eda[[var_x, var_y]].dropna().copy()
            x_num, y_num = var_x in numeric_cols, var_y in numeric_cols
            st.caption(f"Observations utilisées : {len(pair):,}")
            if pair.empty:
                st.warning("Aucune observation complète pour cette paire de variables.")
            elif x_num and y_num:
                fig = px.scatter(pair, x=var_x, y=var_y, title=f"{var_x} en fonction de {var_y}", opacity=0.65)
                st.plotly_chart(fig, use_container_width=True)
                if len(pair) >= 3 and pair[var_x].nunique() > 1 and pair[var_y].nunique() > 1:
                    r, pval = stats.pearsonr(pair[var_x], pair[var_y])
                    rho, p_s = stats.spearmanr(pair[var_x], pair[var_y])
                    st.write(f"**Corrélation de Pearson :** r = {r:.4f}, p = {pval:.4g}")
                    st.write(f"**Corrélation de Spearman :** ρ = {rho:.4f}, p = {p_s:.4g}")
            elif x_num != y_num:
                cat_var, num_var = (var_y, var_x) if x_num else (var_x, var_y)
                pair[cat_var] = pair[cat_var].astype(str)
                fig = px.box(pair, x=cat_var, y=num_var, points="outliers", title=f"{num_var} selon {cat_var}")
                st.plotly_chart(fig, use_container_width=True)
                groups = [g[num_var].dropna().to_numpy() for _, g in pair.groupby(cat_var) if len(g[num_var].dropna()) > 0]
                if len(groups) == 2 and all(len(g) >= 2 for g in groups):
                    test_name = st.selectbox("Test de comparaison", ["Mann–Whitney (non paramétrique)", "t de Welch (moyennes)"], key="eda_test_two")
                    if test_name.startswith("Mann"):
                        stat, pval = stats.mannwhitneyu(groups[0], groups[1], alternative="two-sided")
                        st.write(f"**Mann–Whitney :** U = {stat:.4g}, p = {pval:.4g}")
                    else:
                        stat, pval = stats.ttest_ind(groups[0], groups[1], equal_var=False, nan_policy="omit")
                        st.write(f"**Test t de Welch :** t = {stat:.4g}, p = {pval:.4g}")
                elif len(groups) >= 3:
                    stat, pval = stats.kruskal(*groups)
                    st.write(f"**Kruskal–Wallis :** H = {stat:.4g}, p = {pval:.4g}")
                    st.caption("Pour trois groupes ou plus, Kruskal–Wallis compare les distributions ; un résultat significatif ne précise pas quels groupes diffèrent.")
            else:
                pair[var_x] = pair[var_x].astype(str)
                pair[var_y] = pair[var_y].astype(str)
                ct = pd.crosstab(pair[var_x], pair[var_y])
                st.dataframe(ct, use_container_width=True)
                fig = px.bar(ct.reset_index().melt(id_vars=var_x, var_name=var_y, value_name="Effectif"),
                             x=var_x, y="Effectif", color=var_y, barmode="group", title=f"{var_x} × {var_y}")
                st.plotly_chart(fig, use_container_width=True)
                if ct.shape[0] >= 2 and ct.shape[1] >= 2:
                    chi2, pval, dof, expected = chi2_contingency(ct)
                    n = ct.to_numpy().sum()
                    denom = min(ct.shape[0] - 1, ct.shape[1] - 1)
                    cramers_v = np.sqrt(chi2 / (n * denom)) if n > 0 and denom > 0 else np.nan
                    st.write(f"**Test du χ² d’indépendance :** χ² = {chi2:.4f}, ddl = {dof}, p = {pval:.4g}")
                    st.write(f"**V de Cramér :** {cramers_v:.4f}")
                    if (expected < 5).any():
                        st.warning("Certaines fréquences théoriques sont inférieures à 5 : interprétez le χ² avec prudence.")

    # -------------------- MULTIVARIÉE --------------------
    with tab_multi:
        st.subheader("Analyse multivariée")
        if len(numeric_cols) >= 2:
            st.markdown("**Matrice de corrélation des variables quantitatives**")
            chosen_num = st.multiselect("Variables quantitatives à inclure", numeric_cols,
                                        default=numeric_cols[:min(10, len(numeric_cols))], key="eda_multi_num")
            method_corr = st.radio("Méthode de corrélation", ["Spearman", "Pearson"], horizontal=True, key="eda_corr_method")
            if len(chosen_num) >= 2:
                corr = df_eda[chosen_num].corr(method=method_corr.lower(), numeric_only=True)
                fig = px.imshow(corr, text_auto=".2f", aspect="auto", zmin=-1, zmax=1,
                                color_continuous_scale="RdBu_r", title=f"Corrélations — {method_corr}")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(corr.round(3), use_container_width=True)
            else:
                st.info("Sélectionnez au moins deux variables quantitatives.")
        else:
            st.info("La base ne contient pas assez de variables quantitatives pour une matrice de corrélation.")

        st.markdown("**Analyse croisée de trois variables catégorielles**")
        if len(categorical_cols) >= 3:
            c1, c2, c3 = st.columns(3)
            with c1: v1 = st.selectbox("Variable principale", categorical_cols, key="eda_multi_cat1")
            with c2: v2 = st.selectbox("Variable de comparaison", categorical_cols, index=min(1, len(categorical_cols)-1), key="eda_multi_cat2")
            with c3: v3 = st.selectbox("Variable de stratification", categorical_cols, index=min(2, len(categorical_cols)-1), key="eda_multi_cat3")
            if len({v1, v2, v3}) < 3:
                st.warning("Sélectionnez trois variables différentes.")
            else:
                d3 = df_eda[[v1, v2, v3]].dropna().copy().astype(str)
                if not d3.empty:
                    tab3 = pd.crosstab([d3[v1], d3[v3]], d3[v2], normalize="index").mul(100).round(2)
                    st.dataframe(tab3, use_container_width=True)
                    long3 = tab3.reset_index().melt(id_vars=[v1, v3], var_name=v2, value_name="Pourcentage")
                    fig = px.bar(long3, x=v1, y="Pourcentage", color=v2, facet_col=v3,
                                 barmode="group", title=f"{v2} selon {v1}, stratifié par {v3}")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Il faut au moins trois variables catégorielles pour cette analyse croisée.")

    # -------------------- TESTS AUTOMATIQUES --------------------
    with tab_tests:
        st.subheader("Tests statistiques automatiques")
        st.markdown("Sélectionnez les variables ; l’application choisit le test selon leur type.")
        tx1, tx2 = st.columns(2)
        with tx1:
            test_x = st.selectbox("Variable explicative", all_cols, index=all_cols.index("acces_elec") if "acces_elec" in all_cols else 0, key="eda_auto_x")
        with tx2:
            test_y_default = "travail" if "travail" in all_cols and test_x != "travail" else ("entrepreneuriat" if "entrepreneuriat" in all_cols and test_x != "entrepreneuriat" else all_cols[-1])
            test_y = st.selectbox("Variable à étudier", all_cols, index=all_cols.index(test_y_default), key="eda_auto_y")
        if test_x == test_y:
            st.warning("Choisissez deux variables différentes.")
        else:
            dtest = df_eda[[test_x, test_y]].dropna().copy()
            x_is_num, y_is_num = test_x in numeric_cols, test_y in numeric_cols
            st.write(f"Observations complètes : **{len(dtest):,}**")
            if len(dtest) < 3:
                st.warning("Nombre d’observations insuffisant pour effectuer le test.")
            elif x_is_num and y_is_num:
                if dtest[test_x].nunique() < 2 or dtest[test_y].nunique() < 2:
                    st.warning("Une des variables est constante ; la corrélation ne peut pas être calculée.")
                else:
                    rho, pval = stats.spearmanr(dtest[test_x], dtest[test_y])
                    st.write(f"**Test automatique : corrélation de Spearman** — ρ = {rho:.4f}, p = {pval:.4g}")
            elif x_is_num != y_is_num:
                cat, num = (test_y, test_x) if x_is_num else (test_x, test_y)
                dtest[cat] = dtest[cat].astype(str)
                groups = [g[num].dropna().to_numpy() for _, g in dtest.groupby(cat) if len(g[num].dropna()) > 0]
                if len(groups) == 2 and all(len(g) >= 2 for g in groups):
                    stat, pval = stats.mannwhitneyu(groups[0], groups[1], alternative="two-sided")
                    st.write(f"**Test automatique : Mann–Whitney** — U = {stat:.4g}, p = {pval:.4g}")
                elif len(groups) >= 3 and all(len(g) > 0 for g in groups):
                    stat, pval = stats.kruskal(*groups)
                    st.write(f"**Test automatique : Kruskal–Wallis** — H = {stat:.4g}, p = {pval:.4g}")
                else:
                    st.warning("Groupes insuffisants pour effectuer le test.")
            else:
                dtest[test_x] = dtest[test_x].astype(str)
                dtest[test_y] = dtest[test_y].astype(str)
                ct = pd.crosstab(dtest[test_x], dtest[test_y])
                if ct.shape[0] >= 2 and ct.shape[1] >= 2:
                    chi2, pval, dof, expected = chi2_contingency(ct)
                    st.write(f"**Test automatique : χ² d’indépendance** — χ² = {chi2:.4f}, ddl = {dof}, p = {pval:.4g}")
                    if (expected < 5).any():
                        st.warning("Certaines fréquences théoriques sont faibles ; le test du χ² doit être interprété avec prudence.")
                else:
                    st.warning("Le tableau croisé doit contenir au moins deux modalités par variable.")

            st.caption("Règle de lecture : si p < 0,05, le résultat est statistiquement significatif au seuil de 5 %. Cela ne prouve pas une relation causale. Pour des données d’enquête, tenez compte du plan de sondage et des pondérations si elles sont disponibles.")



# ============================================================
# ÉTAPE 4 — MACHINE LEARNING
# ============================================================
elif page == "🤖 Machine Learning (Étape 4)":
    st.title("🤖 Étape 4 — Machine Learning")
    st.markdown(
        "Cette étape compare des modèles de classification pour **l’emploi** et "
        "**l’entrepreneuriat**, puis propose un clustering K-Means exploratoire. "
        "Les résultats décrivent des performances prédictives et ne démontrent pas une causalité."
    )

    if "data_clean" in st.session_state and isinstance(st.session_state.data_clean, pd.DataFrame):
        df_ml = st.session_state.data_clean.copy()
    elif "data" in st.session_state and isinstance(st.session_state.data, pd.DataFrame):
        df_ml = st.session_state.data.copy()
        st.warning("La base nettoyée n’est pas disponible : l’application utilise la base fusionnée. Vérifiez le nettoyage avant l’analyse.")
    else:
        df_ml = None

    if df_ml is None or df_ml.empty:
        st.warning("Aucune base disponible. Passez d’abord par l’étape 1 pour importer et fusionner les fichiers, puis par l’étape 2 pour nettoyer les données.")
    else:
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import OneHotEncoder, StandardScaler
            from sklearn.compose import ColumnTransformer
            from sklearn.pipeline import Pipeline
            from sklearn.impute import SimpleImputer
            from sklearn.metrics import (
                accuracy_score, precision_score, recall_score, f1_score,
                confusion_matrix, classification_report, roc_auc_score,
                average_precision_score, roc_curve, precision_recall_curve
            )
            from sklearn.linear_model import LogisticRegression
            from sklearn.svm import LinearSVC
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.cluster import MiniBatchKMeans
            from sklearn.decomposition import TruncatedSVD
            import plotly.express as px
            import plotly.graph_objects as go
        except ImportError as e:
            st.error(f"Bibliothèque manquante : {e}. Installez les dépendances avec : pip install scikit-learn plotly xgboost")
            st.stop()

        ml_tab, km_tab, guide_tab = st.tabs(["🧠 Modèles supervisés", "🧩 K-Means", "📘 Guide d’interprétation"])

        with ml_tab:
            st.subheader("Comparaison des modèles de classification")
            targets = [c for c in ["travail", "entrepreneuriat"] if c in df_ml.columns]
            if not targets:
                st.error("Les colonnes cibles 'travail' et 'entrepreneuriat' sont introuvables dans la base.")
            else:
                c1, c2, c3 = st.columns(3)
                with c1:
                    target = st.selectbox("Cible à prédire", targets, key="ml_target")
                with c2:
                    test_size_pct = st.slider("Part du jeu de test (%)", 15, 40, 25, key="ml_test_size")
                with c3:
                    random_seed = st.number_input("Graine aléatoire", min_value=0, max_value=99999, value=42, key="ml_seed")

                excluded = {"travail", "entrepreneuriat", "ID"}
                candidate_features = [c for c in df_ml.columns if c not in excluded]
                default_features = [c for c in candidate_features if c not in ["strate"]]
                selected_features = st.multiselect(
                    "Variables explicatives (les deux cibles sont exclues automatiquement pour éviter la fuite de données)",
                    candidate_features,
                    default=default_features,
                    key="ml_features"
                )
                model_choices = st.multiselect(
                    "Modèles à comparer",
                    ["Régression logistique", "SVM linéaire", "Random Forest", "XGBoost"],
                    default=["Régression logistique", "SVM linéaire", "Random Forest", "XGBoost"],
                    key="ml_models"
                )
                run_ml = st.button("🚀 Entraîner et comparer les modèles", type="primary", key="run_ml_models")

                if run_ml:
                    if not selected_features:
                        st.error("Sélectionnez au moins une variable explicative.")
                    else:
                        # Les valeurs manquantes de la cible sont exclues uniquement de ce modèle.
                        model_df = df_ml[selected_features + [target]].copy()
                        model_df = model_df.dropna(subset=[target]).copy()
                        model_df[target] = model_df[target].astype(str).str.strip()
                        # Fidèle au notebook mem.ipynb : les cibles binaires sont Oui / Non.
                        # Les valeurs inconnues ou autres modalités ne sont pas recodées arbitrairement.
                        model_df = model_df[model_df[target].isin(["Non", "Oui"])].copy()
                        if model_df[target].nunique() != 2:
                            st.error(f"La cible '{target}' doit avoir exactement deux classes observées pour ces métriques ROC-AUC/PR-AUC. Classes détectées : {model_df[target].unique().tolist()}")
                        elif len(model_df) < 30:
                            st.error("Trop peu d’observations complètes pour entraîner et évaluer les modèles de manière raisonnable.")
                        else:
                            X = model_df[selected_features].copy()
                            y_text = model_df[target].astype(str)
                            # Codage explicite : Non = 0, Oui = 1.
                            # Ainsi, ROC-AUC et PR-AUC évaluent toujours la classe Oui.
                            y = y_text.map({"Non": 0, "Oui": 1}).astype(int).to_numpy()
                            class_names = ["Non", "Oui"]
                            counts = y_text.value_counts().reindex(["Non", "Oui"], fill_value=0)
                            st.write(f"Observations utilisées pour **{target}** : **{len(model_df):,}**. Les observations dont la cible est manquante ne sont pas transformées en 'Non'.")
                            st.write("Répartition de la cible :")
                            st.dataframe(counts.rename_axis("Classe").reset_index(name="Effectif"), use_container_width=True, hide_index=True)

                            numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
                            categorical_features = [c for c in selected_features if c not in numeric_features]
                            try:
                                encoder = OneHotEncoder(handle_unknown="ignore", min_frequency=2)
                            except TypeError:
                                encoder = OneHotEncoder(handle_unknown="ignore")
                            transformers = []
                            if numeric_features:
                                numeric_pipe = Pipeline([
                                    ("imputer", SimpleImputer(strategy="median")),
                                    ("scaler", StandardScaler())
                                ])
                                transformers.append(("num", numeric_pipe, numeric_features))
                            if categorical_features:
                                categorical_pipe = Pipeline([
                                    ("imputer", SimpleImputer(strategy="most_frequent")),
                                    ("onehot", encoder)
                                ])
                                transformers.append(("cat", categorical_pipe, categorical_features))
                            preprocess = ColumnTransformer(transformers=transformers, remainder="drop")

                            class_counts = np.bincount(y)
                            if class_counts.min() < 2:
                                st.error("Une classe contient moins de deux observations : impossible de réaliser une séparation stratifiée fiable.")
                            else:
                                try:
                                    X_train, X_test, y_train, y_test = train_test_split(
                                        X, y, test_size=test_size_pct / 100,
                                        random_state=int(random_seed), stratify=y
                                    )
                                    model_specs = {
                                        "Régression logistique": LogisticRegression(
                                            max_iter=1500, class_weight="balanced", solver="liblinear"
                                        ),
                                        "SVM linéaire": LinearSVC(
                                            class_weight="balanced", random_state=int(random_seed), max_iter=5000
                                        ),
                                        "Random Forest": RandomForestClassifier(
                                            n_estimators=200, class_weight="balanced_subsample",
                                            random_state=int(random_seed), n_jobs=-1, min_samples_leaf=2
                                        )
                                    }
                                    if "XGBoost" in model_choices:
                                        try:
                                            from xgboost import XGBClassifier
                                            neg, pos = np.bincount(y_train, minlength=2)
                                            model_specs["XGBoost"] = XGBClassifier(
                                                n_estimators=200, max_depth=4, learning_rate=0.05,
                                                subsample=0.8, colsample_bytree=0.7,
                                                min_child_weight=3, gamma=0.1,
                                                scale_pos_weight=float((neg / max(pos, 1)) * 1.5),
                                                eval_metric="logloss", random_state=int(random_seed),
                                                n_jobs=2, tree_method="hist"
                                            )
                                        except ImportError:
                                            st.warning("XGBoost n’est pas installé ; ce modèle sera ignoré. Installez-le avec : pip install xgboost")
                                    results = []
                                    fitted_models = {}
                                    predictions = {}
                                    for model_name in model_choices:
                                        if model_name not in model_specs:
                                            continue
                                        with st.spinner(f"Entraînement : {model_name}…"):
                                            pipe = Pipeline([
                                                ("preprocess", preprocess),
                                                ("model", model_specs[model_name])
                                            ])
                                            pipe.fit(X_train, y_train)
                                            pred = pipe.predict(X_test).astype(int)
                                            estimator = pipe.named_steps["model"]
                                            if hasattr(estimator, "predict_proba"):
                                                scores = pipe.predict_proba(X_test)[:, 1]
                                            elif hasattr(estimator, "decision_function"):
                                                scores = pipe.decision_function(X_test)
                                            else:
                                                scores = pred
                                            try:
                                                auc_roc = roc_auc_score(y_test, scores)
                                                auc_pr = average_precision_score(y_test, scores)
                                            except Exception:
                                                auc_roc, auc_pr = np.nan, np.nan
                                            results.append({
                                                "Modèle": model_name,
                                                "Accuracy": accuracy_score(y_test, pred),
                                                "Précision (classe positive)": precision_score(y_test, pred, zero_division=0),
                                                "Rappel (classe positive)": recall_score(y_test, pred, zero_division=0),
                                                "F1-score (classe positive)": f1_score(y_test, pred, zero_division=0),
                                                "ROC-AUC": auc_roc,
                                                "PR-AUC (Average Precision)": auc_pr
                                            })
                                            fitted_models[model_name] = pipe
                                            predictions[model_name] = {"pred": pred, "scores": scores}
                                    if results:
                                        result_df = pd.DataFrame(results).sort_values("PR-AUC (Average Precision)", ascending=False, na_position="last")
                                        st.session_state["ml_results_" + target] = result_df
                                        st.session_state["ml_fitted_" + target] = fitted_models
                                        st.session_state["ml_predictions_" + target] = predictions
                                        st.session_state["ml_y_test_" + target] = y_test
                                        st.session_state["ml_class_names_" + target] = class_names
                                        st.session_state["ml_X_test_" + target] = X_test
                                        st.success("Entraînement terminé.")
                                        st.dataframe(result_df.style.format({c: "{:.3f}" for c in result_df.columns if c != "Modèle"}), use_container_width=True, hide_index=True)
                                        st.caption("Codage utilisé : Non = 0 et Oui = 1. Les pondérations de classes sont appliquées pendant l’apprentissage ; le jeu de test conserve la distribution observée. Pour l’entrepreneuriat, ne choisissez pas uniquement selon l’accuracy : examinez surtout le rappel, le F1-score et la PR-AUC.")

                                        metric_cols = [c for c in ["ROC-AUC", "PR-AUC (Average Precision)"] if c in result_df.columns]
                                        if metric_cols:
                                            plot_df = result_df.melt(id_vars="Modèle", value_vars=metric_cols, var_name="Métrique", value_name="Score")
                                            fig_metrics = px.bar(plot_df, x="Modèle", y="Score", color="Métrique", barmode="group", range_y=[0, 1], title="Comparaison des métriques")
                                            st.plotly_chart(fig_metrics, use_container_width=True)

                                        model_to_inspect = st.selectbox("Modèle à examiner en détail", list(fitted_models.keys()), key="ml_inspect_" + target)
                                        detail_pipe = fitted_models[model_to_inspect]
                                        detail_pred = predictions[model_to_inspect]["pred"]
                                        detail_scores = predictions[model_to_inspect]["scores"]
                                        cm = confusion_matrix(y_test, detail_pred, labels=[0, 1])
                                        cm_fig = px.imshow(cm, text_auto=True, x=[f"Prédit : {class_names[0]}", f"Prédit : {class_names[1]}"], y=[f"Réel : {class_names[0]}", f"Réel : {class_names[1]}"], color_continuous_scale="Blues", title=f"Matrice de confusion — {model_to_inspect}")
                                        st.plotly_chart(cm_fig, use_container_width=True)
                                        with st.expander("Rapport de classification détaillé"):
                                            st.text(classification_report(y_test, detail_pred, labels=[0, 1], target_names=class_names, zero_division=0))

                                        fpr, tpr, _ = roc_curve(y_test, detail_scores)
                                        roc_fig = go.Figure()
                                        roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"ROC-AUC = {roc_auc_score(y_test, detail_scores):.3f}"))
                                        roc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Référence aléatoire", line=dict(dash="dash")))
                                        roc_fig.update_layout(title="Courbe ROC", xaxis_title="Taux de faux positifs", yaxis_title="Taux de vrais positifs", xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
                                        st.plotly_chart(roc_fig, use_container_width=True)
                                        prec_curve, rec_curve, _ = precision_recall_curve(y_test, detail_scores)
                                        pr_fig = go.Figure()
                                        pr_fig.add_trace(go.Scatter(x=rec_curve, y=prec_curve, mode="lines", name=f"PR-AUC = {average_precision_score(y_test, detail_scores):.3f}"))
                                        pr_fig.update_layout(title="Courbe précision-rappel", xaxis_title="Rappel", yaxis_title="Précision", xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
                                        st.plotly_chart(pr_fig, use_container_width=True)

                                        st.subheader("Importance des variables")
                                        feature_names = detail_pipe.named_steps["preprocess"].get_feature_names_out()
                                        fitted_est = detail_pipe.named_steps["model"]
                                        importance = None
                                        if hasattr(fitted_est, "feature_importances_"):
                                            importance = fitted_est.feature_importances_
                                        elif hasattr(fitted_est, "coef_"):
                                            importance = np.abs(np.ravel(fitted_est.coef_))
                                        if importance is not None and len(importance) == len(feature_names):
                                            imp_df = pd.DataFrame({"Variable transformée": feature_names, "Importance": importance}).sort_values("Importance", ascending=False).head(20)
                                            imp_fig = px.bar(imp_df.sort_values("Importance"), x="Importance", y="Variable transformée", orientation="h", title="Top 20 des variables les plus influentes")
                                            st.plotly_chart(imp_fig, use_container_width=True)
                                            st.caption("Pour la régression logistique et le SVM, l’importance affichée est la valeur absolue du coefficient : elle indique l’intensité, pas le sens de l’association. Pour les arbres, il s’agit de l’importance calculée par le modèle.")
                                        else:
                                            st.info("Ce modèle ne fournit pas une importance des variables directement disponible.")
                                except Exception as e:
                                    st.error(f"Une erreur est survenue pendant l’entraînement : {e}")
                                    st.info("Vérifiez que les variables sélectionnées sont bien renseignées et que les classes de la cible sont suffisamment représentées.")

        with km_tab:
            st.subheader("K-Means — segmentation exploratoire des individus")
            st.write("K-Means ne prédit pas l’emploi ou l’entrepreneuriat : il regroupe les individus selon la similarité de leurs caractéristiques.")
            km_candidates = [c for c in df_ml.columns if c not in ["ID", "travail", "entrepreneuriat"]]
            km_defaults = [c for c in km_candidates if c in ["acces_elec", "age", "sexe", "milieu_residence", "formation", "diplome", "dep_elec", "dep_gaz", "dep_bois"]]
            km_features = st.multiselect("Variables pour la segmentation", km_candidates, default=km_defaults or km_candidates[:min(5, len(km_candidates))], key="km_features")
            k_clusters = st.slider("Nombre de groupes K", 2, 8, 3, key="km_k")
            km_sample = st.slider("Nombre maximal d’individus à analyser (pour limiter le temps de calcul)", 1000, min(10000, max(1000, len(df_ml))), min(5000, max(1000, len(df_ml))), step=500, key="km_sample")
            if st.button("🔍 Lancer K-Means", type="primary", key="run_kmeans"):
                if len(km_features) < 2:
                    st.error("Sélectionnez au moins deux variables pour former les groupes.")
                else:
                    km_data = df_ml[km_features].copy().replace([np.inf, -np.inf], np.nan)
                    if len(km_data) > km_sample:
                        km_data = km_data.sample(n=km_sample, random_state=42)
                    km_num = km_data.select_dtypes(include=[np.number]).columns.tolist()
                    km_cat = [c for c in km_features if c not in km_num]
                    km_trans = []
                    if km_num:
                        km_trans.append(("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), km_num))
                    if km_cat:
                        try:
                            km_encoder = OneHotEncoder(handle_unknown="ignore", min_frequency=2)
                        except TypeError:
                            km_encoder = OneHotEncoder(handle_unknown="ignore")
                        km_trans.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", km_encoder)]), km_cat))
                    try:
                        km_prep = ColumnTransformer(km_trans)
                        km_matrix = km_prep.fit_transform(km_data)
                        # MiniBatchKMeans réduit le temps de calcul sur les matrices creuses.
                        km_model = MiniBatchKMeans(n_clusters=k_clusters, random_state=42, n_init=10, batch_size=512)
                        labels = km_model.fit_predict(km_matrix)
                        km_result = km_data.copy()
                        km_result["Cluster"] = labels.astype(str)
                        st.success("Segmentation terminée.")
                        cluster_counts = km_result["Cluster"].value_counts().sort_index().rename_axis("Cluster").reset_index(name="Effectif")
                        st.dataframe(cluster_counts, use_container_width=True, hide_index=True)
                        if len(km_num) >= 1:
                            profile = km_result.groupby("Cluster")[km_num].mean(numeric_only=True).round(2)
                            st.subheader("Profil moyen des clusters — variables numériques")
                            st.dataframe(profile, use_container_width=True)
                        for cat_col in km_cat[:3]:
                            st.subheader(f"Répartition de {cat_col} par cluster")
                            tab = pd.crosstab(km_result["Cluster"], km_result[cat_col], normalize="index") * 100
                            st.plotly_chart(px.bar(tab.reset_index().melt(id_vars="Cluster", var_name=cat_col, value_name="Pourcentage"), x="Cluster", y="Pourcentage", color=cat_col, barmode="stack", title=f"{cat_col} — pourcentage par cluster"), use_container_width=True)
                        st.caption("Les clusters sont des groupes statistiques exploratoires. Leur interprétation dépend des variables choisies, de leur codage et du nombre K retenu ; ils ne représentent pas nécessairement des catégories naturelles.")
                    except Exception as e:
                        st.error(f"Impossible d’effectuer K-Means avec cette sélection : {e}")

        with guide_tab:
            st.subheader("Comment interpréter les résultats")
            st.markdown("""
- **Accuracy** : proportion totale de prédictions correctes ; elle peut être trompeuse lorsque la cible est très déséquilibrée.
- **Précision** : parmi les individus prédits positifs, part réellement positive.
- **Rappel** : parmi les vrais positifs, part détectée par le modèle.
- **F1-score** : compromis entre précision et rappel.
- **ROC-AUC** : capacité à classer les positifs devant les négatifs sur différents seuils.
- **PR-AUC / Average Precision** : particulièrement utile lorsque la classe positive est rare ; sa valeur de référence dépend de la prévalence de cette classe.
- **Matrice de confusion** : distingue vrais négatifs, faux positifs, faux négatifs et vrais positifs.
- **Importance des variables** : décrit comment le modèle utilise les variables ; ce n’est pas une preuve d’effet causal.
- **K-Means** : méthode non supervisée qui forme des groupes, sans utiliser les étiquettes emploi/entrepreneuriat.

Pour le mémoire, indiquez toujours la cible, les variables explicatives, la taille de l’échantillon après exclusion des cibles manquantes, le découpage entraînement/test et les métriques obtenues. Pour l’entrepreneuriat, dont la classe positive peut être très minoritaire, commentez surtout le rappel, le F1-score et la PR-AUC en plus de l’accuracy.
            """)


# ============================================================
# ÉTAPE 5 — PRÉDICTION INTERACTIVE
# ============================================================
elif page == "🔮 Prédiction interactive (Étape 5)":
    st.title("🔮 Étape 5 — Prédiction interactive")
    st.write(
        "Utilisez un formulaire pour obtenir une prédiction de la situation d’emploi "
        "ou de l’entrepreneuriat, ainsi que les probabilités estimées par un modèle "
        "entraîné sur les données disponibles. Ces résultats sont indicatifs et ne "
        "constituent ni une certitude individuelle ni une preuve de causalité."
    )

    if isinstance(st.session_state.get("data_clean"), pd.DataFrame):
        df_pred = st.session_state.data_clean.copy()
    elif isinstance(st.session_state.get("data"), pd.DataFrame):
        df_pred = st.session_state.data.copy()
        st.warning("La base nettoyée n’est pas disponible : la base fusionnée est utilisée.")
    else:
        df_pred = None

    if df_pred is None or df_pred.empty:
        st.warning("Aucune base disponible. Commencez par l’étape 1, puis effectuez le nettoyage à l’étape 2.")
    else:
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
        from sklearn.svm import SVC

        cible_options = [c for c in ["travail", "entrepreneuriat"] if c in df_pred.columns]
        if not cible_options:
            st.error("Les colonnes 'travail' et 'entrepreneuriat' sont absentes de la base.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                cible_pred = st.selectbox("Que souhaitez-vous prédire ?", cible_options, key="step5_target")
            with c2:
                modele_pred = st.selectbox(
                    "Modèle de prédiction",
                    ["Régression logistique", "SVM", "Random Forest", "XGBoost"],
                    key="step5_model"
                )

            variables_exclues = {"ID", "travail", "entrepreneuriat"}
            candidats = [c for c in df_pred.columns if c not in variables_exclues]
            valeurs_defaut = [c for c in candidats if c in [
                "acces_elec", "age", "sexe", "milieu_residence", "formation", "diplome",
                "type_elec", "source_energie_cuisine", "dep_elec_log", "dep_gaz_log",
                "dep_bois_log", "Impots_taxes_log", "transfertsArgents_log"
            ]]
            if not valeurs_defaut:
                valeurs_defaut = candidats[:min(8, len(candidats))]
            variables_pred = st.multiselect(
                "Variables à utiliser pour entraîner le modèle et alimenter le formulaire",
                options=candidats,
                default=valeurs_defaut,
                key="step5_features",
                help="Les deux cibles et l’identifiant sont exclus pour éviter une fuite de données. Utilisez des variables disponibles au moment où la prédiction serait faite."
            )

            if st.button("⚙️ Entraîner le modèle pour la prédiction", type="primary", key="step5_train"):
                try:
                    train_df = df_pred[variables_pred + [cible_pred]].copy()
                    train_df[cible_pred] = train_df[cible_pred].astype("string").str.strip()
                    train_df = train_df[train_df[cible_pred].isin(["Oui", "Non"])].dropna(subset=[cible_pred])
                    if not variables_pred:
                        st.error("Sélectionnez au moins une variable explicative.")
                    elif train_df[cible_pred].nunique() != 2:
                        st.error(f"La cible {cible_pred} doit contenir les deux modalités 'Oui' et 'Non'. Modalités observées : {train_df[cible_pred].value_counts().to_dict()}")
                    elif len(train_df) < 30:
                        st.error("Le nombre d’observations est insuffisant pour entraîner un modèle fiable.")
                    else:
                        X_train_pred = train_df[variables_pred].replace([np.inf, -np.inf], np.nan)
                        y_train_pred = train_df[cible_pred].map({"Non": 0, "Oui": 1}).astype(int)
                        numeric_cols = X_train_pred.select_dtypes(include=[np.number]).columns.tolist()
                        categorical_cols = [c for c in variables_pred if c not in numeric_cols]
                        try:
                            encoder_pred = OneHotEncoder(handle_unknown="ignore", min_frequency=2)
                        except TypeError:
                            encoder_pred = OneHotEncoder(handle_unknown="ignore")
                        transformers_pred = []
                        if numeric_cols:
                            transformers_pred.append(("num", Pipeline([
                                ("imputer", SimpleImputer(strategy="median")),
                                ("scaler", StandardScaler())
                            ]), numeric_cols))
                        if categorical_cols:
                            transformers_pred.append(("cat", Pipeline([
                                ("imputer", SimpleImputer(strategy="most_frequent")),
                                ("onehot", encoder_pred)
                            ]), categorical_cols))
                        preprocess_pred = ColumnTransformer(transformers=transformers_pred, remainder="drop")

                        if modele_pred == "Régression logistique":
                            classifier_pred = LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42)
                        elif modele_pred == "SVM":
                            classifier_pred = SVC(kernel="linear", probability=True, class_weight="balanced", random_state=42)
                        elif modele_pred == "Random Forest":
                            classifier_pred = RandomForestClassifier(
                                n_estimators=250, class_weight="balanced_subsample", random_state=42,
                                n_jobs=-1, min_samples_leaf=2
                            )
                        else:
                            try:
                                from xgboost import XGBClassifier
                                positives = int((y_train_pred == 1).sum())
                                negatives = int((y_train_pred == 0).sum())
                                classifier_pred = XGBClassifier(
                                    n_estimators=250, max_depth=4, learning_rate=0.05,
                                    subsample=0.8, colsample_bytree=0.8,
                                    scale_pos_weight=max(1.0, negatives / max(positives, 1)),
                                    eval_metric="logloss", random_state=42, n_jobs=2
                                )
                            except ImportError:
                                st.error("XGBoost n’est pas installé. Lancez : pip install xgboost")
                                classifier_pred = None

                        if classifier_pred is not None:
                            pipe_pred = Pipeline([("preprocess", preprocess_pred), ("model", classifier_pred)])
                            pipe_pred.fit(X_train_pred, y_train_pred)
                            st.session_state["step5_fitted_model"] = pipe_pred
                            st.session_state["step5_fitted_target"] = cible_pred
                            st.session_state["step5_fitted_model_name"] = modele_pred
                            st.session_state["step5_fitted_features"] = list(variables_pred)
                            st.session_state["step5_training_n"] = len(train_df)
                            st.session_state["step5_training_prevalence"] = float(y_train_pred.mean())
                            st.success(f"Modèle entraîné : {modele_pred} — cible : {cible_pred} — {len(train_df):,} observations avec cible connue.")
                except Exception as e:
                    st.error(f"Impossible d’entraîner le modèle : {e}")

            fitted = st.session_state.get("step5_fitted_model")
            fitted_target = st.session_state.get("step5_fitted_target")
            fitted_features = st.session_state.get("step5_fitted_features", [])
            if fitted is not None and fitted_target == cible_pred and fitted_features == list(variables_pred):
                st.divider()
                st.subheader("📝 Formulaire de prédiction")
                st.caption("Renseignez les caractéristiques d’un profil. Les choix catégoriels proviennent de la base utilisée pour l’entraînement.")
                with st.form("step5_prediction_form"):
                    input_values = {}
                    cols_form = st.columns(2)
                    for idx, col in enumerate(fitted_features):
                        series = df_pred[col]
                        with cols_form[idx % 2]:
                            if pd.api.types.is_numeric_dtype(series):
                                clean_num = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
                                default_num = float(clean_num.median()) if not clean_num.empty else 0.0
                                if col == "age":
                                    input_values[col] = st.number_input(col, min_value=0.0, max_value=120.0, value=float(min(120, max(0, default_num))), step=1.0, key=f"step5_num_{col}")
                                else:
                                    input_values[col] = st.number_input(col, value=default_num, key=f"step5_num_{col}")
                            else:
                                options = series.dropna().astype(str).value_counts().index.tolist()
                                if not options:
                                    options = ["Non_renseigne"]
                                # Limite l’interface aux modalités les plus fréquentes si la variable a beaucoup de valeurs distinctes.
                                options = options[:100]
                                input_values[col] = st.selectbox(col, options=options, key=f"step5_cat_{col}")
                    submitted = st.form_submit_button("🔮 Prédire le résultat", type="primary")

                if submitted:
                    new_row = pd.DataFrame([{c: input_values[c] for c in fitted_features}])
                    try:
                        proba = fitted.predict_proba(new_row)[0]
                        pred_class = int(fitted.predict(new_row)[0])
                        proba_non = float(proba[0])
                        proba_oui = float(proba[1])
                        label_pred = "Oui" if pred_class == 1 else "Non"
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Prédiction", label_pred)
                        col_b.metric("Probabilité estimée — Non", f"{proba_non:.1%}")
                        col_c.metric("Probabilité estimée — Oui", f"{proba_oui:.1%}")
                        st.progress(proba_oui, text=f"Probabilité estimée de '{cible_pred} = Oui' : {proba_oui:.1%}")
                        if proba_oui >= 0.70:
                            st.info(f"Le modèle attribue une probabilité relativement élevée à la modalité 'Oui' ({proba_oui:.1%}).")
                        elif proba_oui >= 0.40:
                            st.info(f"Le résultat est intermédiaire : la probabilité estimée de 'Oui' est de {proba_oui:.1%}. La prédiction dépend du seuil de décision par défaut.")
                        else:
                            st.info(f"Le modèle estime une probabilité plus faible pour la modalité 'Oui' ({proba_oui:.1%}).")
                        st.caption(
                            f"Modèle : {st.session_state.get('step5_fitted_model_name')} | "
                            f"Cible : {cible_pred} | Observations d’entraînement : {st.session_state.get('step5_training_n', '—'):,}. "
                            "Les probabilités sont des estimations du modèle, pas des garanties. La pondération des classes peut affecter leur calibration."
                        )
                        with st.expander("Voir le profil envoyé au modèle"):
                            st.dataframe(new_row, use_container_width=True, hide_index=True)
                    except Exception as e:
                        st.error(f"La prédiction a échoué : {e}")
            elif fitted is not None:
                st.warning("Les paramètres de la prédiction ont changé. Réentraînez le modèle pour utiliser cette cible et ces variables.")

            st.markdown("### 📘 Comment interpréter le résultat ?")
            st.markdown(
                "- **Prédiction = Oui/Non** : classe retenue par le modèle au seuil de décision standard.\n"
                "- **Probabilité estimée** : score attribué par le modèle à chaque classe ; elle n’est pas une certitude.\n"
                "- **Variables choisies** : seules les caractéristiques du formulaire sont transmises au modèle.\n"
                "- **Entrepreneuriat** : les observations où la cible est manquante sont exclues de l’entraînement, jamais recodées automatiquement en 'Non'.\n"
                "- **Déséquilibre des classes** : l’entraînement applique une pondération des classes (ou `scale_pos_weight` pour XGBoost). Cela aide à tenir compte de la classe rare, mais les probabilités peuvent nécessiter une calibration dédiée.\n"
                "- **Limite scientifique** : la prédiction n’établit pas que l’accès à l’électricité cause l’emploi ou l’entrepreneuriat."
            )


# ============================================================
# ÉTAPE 6 — EXPORT COMPLET
# ============================================================

elif page == "📦 Export complet (Étape 6)":
    st.title("📦 Étape 6 — Export des résultats et du rapport")
    st.write(
        "Cette page rassemble les exports de la base nettoyée, des résultats "
        "statistiques et des modèles, des graphiques et d’un rapport d’analyse."
    )

    df_export = None
    if isinstance(st.session_state.get("data_clean"), pd.DataFrame):
        df_export = st.session_state.data_clean.copy()
        source_export = "Base nettoyée (Étape 2)"
    elif isinstance(st.session_state.get("data"), pd.DataFrame):
        df_export = st.session_state.data.copy()
        source_export = "Base fusionnée (Étape 1)"

    if df_export is None:
        st.warning("Importez et fusionnez les fichiers à l’étape 1 pour commencer les exports.")
    else:
        st.caption(f"Source utilisée : {source_export} · {len(df_export):,} lignes · {len(df_export.columns):,} colonnes")
        st.info("Les exports incluent les résultats disponibles dans cette session. Lancez les analyses des étapes 3 et 4 avant l’export si vous souhaitez inclure leurs résultats de modèles.")

        # Préparer les tableaux de résultats disponibles en mémoire
        resultats_modeles = {}
        for cible in ["travail", "entrepreneuriat"]:
            result_key = "ml_results_" + cible
            result_df = st.session_state.get(result_key)
            if isinstance(result_df, pd.DataFrame) and not result_df.empty:
                resultats_modeles[cible] = result_df.copy()

        # Préparer les tableaux descriptifs, données manquantes et fréquences des cibles
        descriptif = df_export.describe(include="all").transpose().reset_index().rename(columns={"index": "Variable"})
        manquants = pd.DataFrame({
            "Variable": df_export.columns,
            "Valeurs manquantes": df_export.isna().sum().values,
            "Pourcentage manquant (%)": (df_export.isna().mean().values * 100).round(2),
        }).sort_values("Valeurs manquantes", ascending=False)
        frequences = {}
        for cible in ["travail", "entrepreneuriat"]:
            if cible in df_export.columns:
                frequences[cible] = df_export[cible].astype("string").fillna("Valeur manquante").value_counts(dropna=False).rename_axis("Modalité").reset_index(name="Effectif")

        figures = {}
        try:
            import plotly.express as px
            import plotly.graph_objects as go

            for cible, tab_freq in frequences.items():
                figures[f"distribution_{cible}"] = px.bar(
                    tab_freq, x="Modalité", y="Effectif", text="Effectif",
                    title=f"Distribution de la variable {cible}",
                    color="Modalité"
                )
            if "acces_elec" in df_export.columns:
                for cible in ["travail", "entrepreneuriat"]:
                    if cible in df_export.columns:
                        tab = pd.crosstab(
                            df_export["acces_elec"].fillna("Valeur manquante").astype(str),
                            df_export[cible].fillna("Valeur manquante").astype(str),
                            normalize="index"
                        ).mul(100).reset_index().melt(
                            id_vars="acces_elec", var_name="Modalité", value_name="Pourcentage"
                        )
                        figures[f"acces_electricite_{cible}"] = px.bar(
                            tab, x="acces_elec", y="Pourcentage", color="Modalité", barmode="group",
                            title=f"{cible} selon l’accès à l’électricité",
                            labels={"acces_elec": "Accès à l’électricité", "Pourcentage": "Pourcentage (%)"}
                        )
        except Exception as e:
            st.warning(f"Les graphiques d’export n’ont pas pu être générés : {e}")

        # Créer les données binaires pour téléchargement
        csv_clean = df_export.to_csv(index=False).encode("utf-8-sig")
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_export.to_excel(writer, sheet_name="Donnees_nettoyees", index=False)
            descriptif.to_excel(writer, sheet_name="Statistiques_descriptives", index=False)
            manquants.to_excel(writer, sheet_name="Valeurs_manquantes", index=False)
            for cible, tab in frequences.items():
                tab.to_excel(writer, sheet_name=f"Frequences_{cible}"[:31], index=False)
            for cible, tab in resultats_modeles.items():
                tab.to_excel(writer, sheet_name=f"Modeles_{cible}"[:31], index=False)
        excel_clean = excel_buffer.getvalue()

        # Construire un rapport HTML lisible et autonome
        def _html_table(frame, max_rows=100):
            return frame.head(max_rows).to_html(index=False, border=0, classes="data-table", justify="left", na_rep="—")

        sections_html = [
            "<h1>Rapport d’analyse — Accès à l’électricité, emploi et entrepreneuriat au Sénégal</h1>",
            f"<p><b>Date de génération :</b> {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}<br>",
            f"<b>Base exportée :</b> {source_export}<br><b>Observations :</b> {len(df_export):,}<br><b>Variables :</b> {len(df_export.columns):,}</p>",
            "<h2>1. Présentation de la base</h2>",
            f"<p>La base utilisée contient {len(df_export):,} observations et {len(df_export.columns):,} variables. Les résultats décrivent les données disponibles au moment de l’export.</p>",
            "<h2>2. Valeurs manquantes</h2>", _html_table(manquants),
            "<h2>3. Statistiques descriptives</h2>", _html_table(descriptif),
        ]
        for cible, tab in frequences.items():
            sections_html.extend([f"<h2>4. Distribution de {cible}</h2>", _html_table(tab)])
        if resultats_modeles:
            sections_html.append("<h2>5. Résultats des modèles de Machine Learning</h2>")
            for cible, tab in resultats_modeles.items():
                sections_html.extend([f"<h3>Cible : {cible}</h3>", _html_table(tab)])
        else:
            sections_html.append("<h2>5. Résultats des modèles</h2><p>Aucun tableau de comparaison des modèles n’a été enregistré dans cette session. Exécutez l’étape 4 puis relancez l’export.</p>")
        sections_html.extend([
            "<h2>6. Graphiques</h2>",
            "<p>Les graphiques présentent les distributions des variables cibles et, lorsque les colonnes sont disponibles, leur répartition selon l’accès à l’électricité.</p>"
        ])
        graph_html_report = []
        for i, (fig_name, fig) in enumerate(figures.items()):
            try:
                graph_html_report.append(fig.to_html(full_html=False, include_plotlyjs=(i == 0)))
            except Exception:
                pass
        if graph_html_report:
            sections_html.extend(graph_html_report)
        else:
            sections_html.append("<p>Aucun graphique n’a pu être généré à partir des variables disponibles.</p>")
        sections_html.extend([
            "<h2>7. Limites d’interprétation</h2>",
            "<ul><li>Les statistiques descriptives et associations ne démontrent pas, à elles seules, une relation de causalité.</li>",
            "<li>Les performances des modèles dépendent des données, des variables et du découpage apprentissage/test.</li>",
            "<li>Les valeurs manquantes sont présentées comme observées dans la base ; elles ne doivent pas être interprétées automatiquement comme une modalité « Non ».</li></ul>",
            "<p><i>Rapport généré automatiquement par la plateforme d’analyse statistique.</i></p>"
        ])
        report_html = "<!doctype html><html lang='fr'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Rapport d’analyse</title><style>body{font-family:Arial,sans-serif;max-width:1100px;margin:35px auto;padding:0 20px;color:#222;line-height:1.5}h1,h2{color:#174a6e}.data-table{border-collapse:collapse;width:100%;font-size:13px;margin:12px 0 24px}.data-table th,.data-table td{border:1px solid #ddd;padding:6px;text-align:left}.data-table th{background:#eef3f7}img,svg{max-width:100%}</style></head><body>" + "\n".join(sections_html) + "</body></html>"

        st.subheader("1. Données nettoyées")
        col_csv, col_excel = st.columns(2)
        with col_csv:
            st.download_button(
                "⬇️ Télécharger les données nettoyées (CSV)", csv_clean,
                "donnees_nettoyees.csv", "text/csv", use_container_width=True
            )
        with col_excel:
            st.download_button(
                "⬇️ Télécharger les données et tableaux (Excel)", excel_clean,
                "export_analyse.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.subheader("2. Résultats statistiques et Machine Learning")
        if resultats_modeles:
            for cible, tab in resultats_modeles.items():
                st.markdown(f"**Résultats enregistrés — {cible}**")
                st.dataframe(tab, use_container_width=True, hide_index=True)
                st.download_button(
                    f"⬇️ Résultats {cible} (CSV)", tab.to_csv(index=False).encode("utf-8-sig"),
                    f"resultats_modeles_{cible}.csv", "text/csv", key=f"step6_results_{cible}"
                )
        else:
            st.info("Aucun résultat de modèle n’est encore enregistré. Lancez les modèles dans « Machine Learning (Étape 4) » puis revenez ici.")
        st.markdown("**Valeurs manquantes et descriptifs inclus dans le fichier Excel.**")

        st.subheader("3. Graphiques exportables")
        if figures:
            for fig_name, fig in figures.items():
                st.plotly_chart(fig, use_container_width=True)
                try:
                    graph_html = fig.to_html(full_html=True, include_plotlyjs=True).encode("utf-8")
                    st.download_button(
                        f"⬇️ Télécharger le graphique : {fig.layout.title.text or fig_name}",
                        graph_html, f"{fig_name}.html", "text/html", key=f"step6_graph_{fig_name}"
                    )
                except Exception as e:
                    st.caption(f"Export individuel indisponible pour {fig_name} : {e}")
        else:
            st.info("Les graphiques seront proposés lorsque les colonnes nécessaires seront disponibles et Plotly installé.")

        st.subheader("4. Rapport d’analyse")
        st.write("Le rapport HTML comprend la description de la base, les valeurs manquantes, les statistiques descriptives, les distributions des cibles, les résultats de modèles disponibles et les limites d’interprétation.")
        st.download_button(
            "⬇️ Télécharger le rapport d’analyse (HTML)",
            report_html.encode("utf-8"), "rapport_analyse.html", "text/html", use_container_width=True
        )

        # Export groupé ZIP : données, rapport, graphiques et résultats des modèles
        zip_buffer = io.BytesIO()
        with __import__("zipfile").ZipFile(zip_buffer, mode="w", compression=__import__("zipfile").ZIP_DEFLATED) as zf:
            zf.writestr("donnees/donnees_nettoyees.csv", csv_clean)
            zf.writestr("donnees/export_analyse.xlsx", excel_clean)
            zf.writestr("rapport/rapport_analyse.html", report_html.encode("utf-8"))
            zf.writestr("tableaux/statistiques_descriptives.csv", descriptif.to_csv(index=False).encode("utf-8-sig"))
            zf.writestr("tableaux/valeurs_manquantes.csv", manquants.to_csv(index=False).encode("utf-8-sig"))
            for cible, tab in frequences.items():
                zf.writestr(f"tableaux/frequences_{cible}.csv", tab.to_csv(index=False).encode("utf-8-sig"))
            for cible, tab in resultats_modeles.items():
                zf.writestr(f"resultats/resultats_modeles_{cible}.csv", tab.to_csv(index=False).encode("utf-8-sig"))
            for fig_name, fig in figures.items():
                try:
                    zf.writestr(f"graphiques/{fig_name}.html", fig.to_html(full_html=True, include_plotlyjs=True).encode("utf-8"))
                except Exception:
                    continue
            zf.writestr("LISEZ_MOI.txt", (
                "Export de la plateforme d’analyse statistique.\n"
                "Le dossier donnees contient la base utilisée et un classeur Excel.\n"
                "Le dossier tableaux contient les descriptifs et fréquences.\n"
                "Le dossier resultats contient les tableaux de modèles disponibles dans la session.\n"
                "Le dossier graphiques contient les graphiques HTML interactifs.\n"
                "Le dossier rapport contient le rapport d’analyse HTML.\n"
                "Attention : association et prédiction ne signifient pas causalité.\n"
            ).encode("utf-8"))

        st.divider()
        st.subheader("5. Tout télécharger en une fois")
        st.download_button(
            "📦 Télécharger le dossier complet (ZIP)", zip_buffer.getvalue(),
            "export_complet_etude_electricite_emploi_entrepreneuriat.zip",
            "application/zip", type="primary", use_container_width=True
        )
        st.caption("Le ZIP regroupe la base nettoyée, les tableaux, les graphiques interactifs, les résultats de modèles disponibles et le rapport HTML. Les résultats présents dépendent des analyses exécutées dans cette session.")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Plateforme d’analyse statistique et de Machine Learning "
    "— Étapes 1 à 6 : importation, nettoyage, analyse exploratoire, Machine Learning, prédiction et export"
)
