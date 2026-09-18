"""Build the source registry (sources/source_registry.csv + data/tables/source_registry.md): every raw file with size,
SHA-256, the URL it came from and how it was retrieved."""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sources" / "raw"
MIN = ROOT / "sources" / "ministry"

URLS = {
    "ehu_20260706_notak_po.pdf": ("https://www.ehu.eus/documents/d/campusa/20260706-notak-po", "EHU presentation 6 Jul 2026", "curl (search agent)"),
    "ehu_informe_pau_2025.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/informe-pau_2025-1-", "EHU annual summary 2025", "curl (search agent)"),
    "ehu_informe_eau_2024.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/informe-eau_2024-1-", "EHU annual summary 2024", "curl (search agent)"),
    "ehu_gv_resultados_escolares_2024_2025.pdf": ("https://www.euskadi.eus/contenidos/informacion/eskola_emaitzak_ikuskaritza/es_def/adjuntos/resultados-escolares-Todo-2024-2025.pdf", "Gobierno Vasco, Resultados escolares 2024-25", "curl (search agent)"),
    "ehu_fisica_examen_ord_2026.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-examen-ord-2026", "EHU Física ordinary paper 2026", "curl (search agent)"),
    "ehu_fisica_solucionario_ord_2026.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-solucionario-ord-2026", "EHU Física ordinary marking scheme 2026", "curl (search agent)"),
    "ehu_guia_acceso_26_27_cast.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/guia-acceso-upv-ehu-26-27-cast-pr3-dig", "EHU access guide 2026-27", "curl (search agent)"),
    "cat_dossier_resultats_PAU_2026.pdf": ("https://govern.cat/govern/docs/2026/06/23/12/39/Dossier_resultats%20PAU%202026.pdf", "Govern dossier PAU ordinària 2026", "curl (search agent)"),
    "cat_dossier_resultats_PAU_2025.pdf": ("https://govern.cat/govern/docs/2025/06/25/13/42/3957aa0b-4b06-4ec5-8132-4910a83a5845.pdf", "Govern dossier PAU 2025", "curl (search agent)"),
    "cat_pau_estadistiques_2025.pdf": ("https://universitats.gencat.cat/web/.content/01_acces_i_admissio/pau/documents/informes_i_estad/pau_estadistiques_2025.pdf", "Recull estadístic PAU 2025", "curl (search agent)"),
    "cat_Mitjanes_FG_FE_PAU_Centre_SSTT_2021-2024.xlsx": ("https://universitats.gencat.cat/", "Means by centre and SSTT 2021-2024 (unused)", "curl (search agent)"),
    "ara_pauresulasig2025.xlsx": ("https://academico.unizar.es/sites/academico/files/archivos/acceso/estad/pauresulasig2025.xlsx", "UNIZAR results by subject 2025", "curl (search agent)"),
    "ara_pauresulasig2025.pdf": ("https://academico.unizar.es/sites/academico/files/archivos/acceso/estad/pauresulasig2025.pdf", "UNIZAR results by subject 2025 (PDF)", "curl (search agent)"),
    "nav_Informe_PAU_2024-25.pdf": ("https://www2.unavarra.es/gesadj/Estudios/acceso_matricula/PAU/Informe_PAU_2024-25.pdf", "UPNA Informe PAU 2024-25", "curl (search agent)"),
    "and_junta_noticia_667462_pevau2026_ordinaria.html": ("https://www.juntadeandalucia.es/organismos/universidadinvestigacioneinnovacion/servicios/actualidad/noticias/detalle/667462.html", "Junta de Andalucía PEvAU 2026 subject means", "curl (search agent)"),
    "and_uma_ponencia_fisica_2025-26.pdf": ("https://www.uma.es/media/files/PRESENTACI%C3%93N_PONENCIA_UMA_25-26.pdf", "UMA Física ponencia 2025-26", "curl (search agent)"),
    "and_us_ponencia_fisica_pau_2025-26_reunion_20251110.pdf": ("https://www.us.es/pevau/coordinacion", "US Física ponencia meeting 10 Nov 2025", "curl (search agent)"),
    "and_uca_reunion_pau_2025_fisica.pdf": ("https://webacceso.uca.es/", "UCA Física coordination 2025", "curl (search agent)"),
    "mur_umu_informe_general_pau2025.pdf": ("https://www.um.es/documents/d/estudios/co-pau2026-1-doc-3-informe-general-pau2025", "UMU/COPAU Informe General PAU2025", "curl (search agent)"),
    "can_acta1_coord_fisica_pau2026_20251009.pdf": ("https://www.gobiernodecanarias.org/cmsgob1/export/sites/educacion/web/bachillerato/_galerias/descargas/pau-2026/20251009_acta-primera-reunion-coordinacion-fisica-pau-26.pdf", "Canarias Física coordination minutes 1 (Oct 2025)", "curl (search agent)"),
    "can_acta2_coord_fisica_pau2026_20260327.pdf": ("https://www.gobiernodecanarias.org/", "Canarias Física coordination minutes 2 (Mar 2026)", "curl (search agent)"),
    "gal_ciug_35_estatisticas_valoracions_2024.pdf": ("https://ciug.gal/PDF/Grupos_Traballo_2024/35_estatisticas_valoracions.pdf", "CiUG Física working group 2020-2023", "curl with repaired TLS chain (search agent)"),
    "gal_ciug_pau.html": ("https://ciug.gal/pau", "CiUG PAU landing page snapshot", "curl"), "gal_ciug_grupos_traballo.html": ("https://ciug.gal/grupos-de-traballo", "CiUG working groups page (empty, 18 Sep 2026)", "curl"),
    "gal_ciug_modelos2027.html": ("https://ciug.gal/", "CiUG 2027 model papers page", "curl"), "gal_ciug_home.html": ("https://ciug.gal/", "CiUG home snapshot", "curl"),
    "cnt_Resultados_por_Materia_PAU_Ordinaria_2025_Web.pdf": ("https://web.unican.es/admision/Documents/Acceso/Resultados%20por%20Materia%20PAU%20Ordinaria%202025_Web.pdf", "UC results by subject, ordinary 2025", "curl (search agent)"),
    "cnt_Resultados_por_Materia_PAU_Extraordinaria_2025_Web.pdf": ("https://web.unican.es/admision/Documents/Acceso/Resultados%20por%20Materia%20PAU%20Extraordinaria%202025_Web.pdf", "UC results by subject, extraordinary 2025", "curl (search agent)"),
    "cyl_uva_resultados-acceso-2025.pdf": ("https://pruebasdeacceso.uva.es/9.resultadosestadisticos/", "UVa results 2025 (no subject table)", "curl (search agent)"),
    "mad_presentacion_resultados_pau_2026.pdf": ("https://www.comunidad.madrid/docs/2026-06/presentacion-resultados-pau-2026_vd.pdf", "Comunidad de Madrid PAU 2026 presentation", "curl (search agent); charts read visually"),
    "mad_uam_pau2026_acta_fisica.pdf": ("https://www.uam.es/uam/en/estudios/comisiones-materia", "UAM Física commission minutes PAU 2026", "curl (search agent)"),
    "mad_uam_pau_presentacion_fisica_2026.pdf": ("https://www.uam.es/uam/en/estudios/comisiones-materia", "UAM Física commission presentation PAU 2026 (charts without labels)", "curl (search agent)"),
    "val_junio_2026.pdf": ("https://universitats.gva.es/documents/389338055/411099714/Estad%C3%ADsticas+PAU+JUNIO+2026.pdf/fa5f4fab-69e8-24b0-dc47-1e883d98e74c", "GVA Estadísticas PAU JUNIO 2026", "downloaded from the user's computer (robots-blocked for the cloud fetcher)"),
    "val_julio_2026.pdf": ("https://universitats.gva.es/documents/389338055/411099714/Estad%C3%ADsticas+PAU+JULIO+2026.pdf/9184b01a-513e-4397-3b65-b4d3ae8a8503", "GVA Estadísticas PAU JULIO 2026", "downloaded from the user's computer"),
    "val_junio_2025.pdf": ("https://universitats.gva.es/documents/389338055/393836351/Estad%C3%ADsticas+PAU+JUNIO+2025.pdf/572b8427-623f-c64a-a6f9-2e219b72416b", "GVA Estadísticas PAU JUNIO 2025", "downloaded from the user's computer"),
    "rio_EvolucionJUN.pdf": ("https://www.unirioja.es/estudiantes/acceso_admision/EBAU/pdf/EvolucionJUN.pdf", "UR evolution by subject, June (2022 edition)", "downloaded from the user's computer (HTTP 429 for the cloud fetcher); charts read visually"),
    "rio_EvolucionJLO.pdf": ("https://www.unirioja.es/estudiantes/acceso_admision/EBAU/pdf/EvolucionJLO.pdf", "UR evolution by subject, July", "downloaded from the user's computer"),
    "rio_EstadisticaJUN.pdf": ("https://www.unirioja.es/estudiantes/acceso_admision/EBAU/pdf/EstadisticaJUN.pdf", "UR global results, June", "downloaded from the user's computer"),
    "rio_EstadisticasJLO.pdf": ("https://www.unirioja.es/estudiantes/acceso_admision/EBAU/pdf/EstadisticasJLO.pdf", "UR global results, July", "downloaded from the user's computer"),
    "lit_faura2022desigualdad.pdf": ("https://revistas.um.es/rie/article/view/424841", "Faura-Martínez et al. 2022 (RIE)", "curl (search agent)"),
    "lit_woitschach2018correctores.pdf": ("https://reunido.uniovi.es/index.php/Rema/article/view/12607", "Woitschach et al. 2018 (REMA)", "curl (search agent)"),
    "px_pau_gen_materias_nota_fase_ca.px": ("https://estadisticas.ciencia.gob.es/jaxiPx/files/_px/es/px/Universitaria/PAU/PAU/l0/px_pau_gen_materias_nota_fase_ca.px", "Ministry EPAU: subject means (copy from the July package)", "project copy"),
    "px_pau_gen_materias_matric_fase_ca.px": ("https://estadisticas.ciencia.gob.es/jaxiPx/files/_px/es/px/Universitaria/PAU/PAU/l0/px_pau_gen_materias_matric_fase_ca.px", "Ministry EPAU: enrolled/presented/passed (copy from the July package)", "project copy"),
    "px_pau_gen_materias_distr_fase_ca.px": ("https://estadisticas.ciencia.gob.es/jaxiPx/files/_px/es/px/Universitaria/PAU/PAU/l0/px_pau_gen_materias_distr_fase_ca.px", "Ministry EPAU: grade distribution (copy of the 18 Sep 2026 download in analysis_2026-09-18)", "project copy"),
}
DASH = [
    ("UCLM Power BI 'Estadística de Aprobados y Nota Media por Materia/Centro/Campus'", "https://www.uclm.es/perfiles/preuniversitario/orientadores/estadisticaspruebasacceso", "read in the built-in browser; values transcribed to data/found_clm_powerbi.csv"),
    ("ULL Power BI 'Calificaciones en la PAU por asignatura'", "https://www.ull.es/estadisticas/pau/", "read in the built-in browser; values transcribed to data/found_canarias_ull_powerbi.csv and found_canarias_ull_history.csv"),
    ("ULPGC Power BI 'Informe 2: Asignaturas (detallado y por sexo)'", "https://www.ulpgc.es/direccion-acceso/informes-ebau-powerbi-2021", "read in the built-in browser; values transcribed to data/found_canarias_ulpgc_powerbi.csv"),
    ("Uniovi press releases 12 Jun and 16 Jul 2026", "https://www.uniovi.es/actualidad/noticias/", "read by the search agent; values in data/regional_fisica_found.csv"),
    ("Canal Extremadura 11 Jun 2026 (UEx release)", "https://www.canalextremadura.es/noticias/extremadura/el-967-de-los-alumnos-presentados-aprueba-la-pau", "press; value in data/regional_fisica_found.csv"),
]

rows = []
for folder in (RAW, MIN):
    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        url, desc, how = URLS.get(f.name, ("", "", "curl (search agent)"))
        rows.append(dict(file=f"{folder.name}/{f.name}", bytes=f.stat().st_size, sha256=h, description=desc, url=url, retrieval=how))
df = pd.DataFrame(rows)
df.to_csv(ROOT / "sources" / "source_registry.csv", index=False)
md = ["| File | kB | Description | Retrieval | SHA-256 (first 12) |", "|---|---:|---|---|---|"]
for r in rows:
    link = f"[{r['file']}]({r['url']})" if r["url"] else r["file"]
    md.append(f"| {link} | {r['bytes']/1024:.0f} | {r['description']} | {r['retrieval']} | `{r['sha256'][:12]}` |")
md.append("")
md.append("| Dashboard / page (no file) | URL | Retrieval |")
md.append("|---|---|---|")
for d, u, how in DASH:
    md.append(f"| {d} | <{u}> | {how} |")
(ROOT / "data" / "tables" / "source_registry.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(len(rows), "files registered")
