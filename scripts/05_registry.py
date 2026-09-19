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

CAN25 = "https://www.gobiernodecanarias.org/cmsgob1/export/sites/educacion/web/bachillerato/_galerias/descargas/pau-2025/examenes-PAU-junio-2025/"
CAN26 = "https://www.gobiernodecanarias.org/cmsgob1/export/sites/educacion/web/bachillerato/_galerias/descargas/pau-2026/examenes-PAU-junio-2026/"
CAT25 = "https://universitats.gencat.cat/web/.content/06_pau/models-examen-anys-anteriors/examens-2025/fisica/ord/"
CAT26 = "https://universitats.gencat.cat/web/.content/06_pau/examens-correccions/2026/fisica/ord/"
FQP = "https://gitlab.com/fiquipedia/drive.fiquipedia/-/raw/main/PAUxComunidades/fisica/"
AND = "https://www.juntadeandalucia.es/economiaconocimientoempresasyuniversidad/sguit/examanes_anios_anteriores/selectividad/"
UCLM = "https://www.uclm.es/perfiles/preuniversitario/acceso/pau/modelosycriteriosdecorreccion/modelospropuestos"
EXAM_URLS = {
    "pv_2025_ord.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisika-azterketa-ohikoa-2025", "curl (search agent)"),
    "pv_2025_ord_crit.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisika-ebazpena-ohikoa-2025", "curl (search agent)"),
    "pv_2025_ord_es.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-examen-ord-2025", "curl (search agent)"),
    "pv_2025_ord_crit_es.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-solucionario-ord-2025", "curl (search agent)"),
    "pv_2026_ord.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-examen-ord-2026", "copy of raw/ehu_fisica_examen_ord_2026.pdf"),
    "pv_2026_ord_crit.pdf": ("https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-solucionario-ord-2026", "copy of raw/ehu_fisica_solucionario_ord_2026.pdf"),
    "cat_2025_ord.pdf": (CAT25 + "pau_fisi25jl.pdf", "curl (search agent)"),
    "cat_2025_ord_crit.pdf": (CAT25 + "pau_fisi25jp.pdf", "curl (search agent)"),
    "cat_2026_ord.pdf": (CAT26 + "pau_fisi26jl.pdf", "curl (search agent)"),
    "cat_2026_ord_crit.pdf": ("https://img.beteve.cat/wp-content/uploads/2026/06/correccions-fisica-pau-selectivitat-2026-a.pdf", "Betevé mirror of the official criteria (gencat pau_fisi26jt.pdf returns 404)"),
    "mad_2025_ord.pdf": ("https://www.ucm.es/file/fisica-18", "curl (search agent); criteria and solutions inside the same PDF"),
    "mad_2026_ord.pdf": ("https://www.ucm.es/file/fisica-25", "curl (search agent); criteria and solutions inside the same PDF"),
    "ast_2025_ord.pdf": ("https://www.uniovi.es/documents/39158/109af28d-1286-5ce4-c932-4645b90d10b6", "curl (search agent)"),
    "ast_2025_ord_crit.pdf": ("https://www.uniovi.es/documents/39158/c71b8148-f18f-0cce-9205-e7f374a142d9", "curl (search agent)"),
    "ast_2026_ord.pdf": ("https://www.uniovi.es/documents/39158/6362fc30-ac9a-ecf1-4602-59b1a6df9249", "curl (search agent)"),
    "ast_2026_ord_crit.pdf": ("https://www.uniovi.es/documents/39158/bcb31598-f190-b118-6156-fc818b17818f", "curl (search agent)"),
    "and_2025.zip": (AND + "sel_2025_fisica.zip", "curl (search agent)"),
    "and_2026.zip": (AND + "sel_2026_fisica.zip", "curl (search agent)"),
    "and_2025_ord.pdf": (AND + "sel_2025_fisica.zip", "extracted from the zip (model A)"),
    "and_2025_ord_B.pdf": (AND + "sel_2025_fisica.zip", "extracted from the zip (model B)"),
    "and_2025_ord_crit.pdf": (AND + "sel_2025_fisica.zip", "extracted from the zip"),
    "and_2025_ord_B_crit.pdf": (AND + "sel_2025_fisica.zip", "extracted from the zip"),
    "and_2026_ord.pdf": (AND + "sel_2026_fisica.zip", "extracted from the zip"),
    "and_2026_ord_crit.pdf": (AND + "sel_2026_fisica.zip", "extracted from the zip"),
    "can_2025_ord.pdf": (CAN25 + "examen-fisica-pau-junio-25.pdf", "curl (search agent)"),
    "can_2025_ord_crit.pdf": (CAN25 + "criterios-correccion-fisica-pau-junio-25.pdf", "curl (search agent)"),
    "can_2026_ord.pdf": (CAN26 + "examen-fisica-pau-junio-26.pdf", "curl (search agent)"),
    "can_2026_ord_crit.pdf": (CAN26 + "criterios-correccion-fisica-pau-junio-26.pdf", "curl (search agent)"),
    "ext_2025_ord.pdf": ("https://drive.google.com/file/d/1f8EIOj_6VpVvZPZjHIjZSV5NatVpRM9_SREobaTkiBo", "Educarex teachers' site (Google Drive export)"),
    "ext_2025_ord_crit.pdf": ("https://drive.google.com/file/d/1tYIYGUyxWjy9tVjLzPcQaVL1sNkbHxY1/view", "Educarex teachers' site (Google Drive)"),
    "ext_2026_ord.pdf": (FQP + "extremadura/2026-ord-extremadura-fisica-exam.pdf", "FiQuiPedia GitLab archive of official papers (uex.es behind WAF)"),
    "ext_2026_ord_crit.pdf": (FQP + "extremadura/2026-ord-extremadura-fisica-criterios.pdf", "FiQuiPedia GitLab archive"),
    "val_2025_ord.pdf": (FQP + "valencia/2025-ord-valencia-fisica-exam.pdf", "FiQuiPedia GitLab archive (official file overwritten at gva.es; byte-identical to the angelcuesta.com copy)"),
    "val_2025_ord_crit.pdf": (FQP + "valencia/2025-ord-valencia-fisica-criterios.pdf", "FiQuiPedia GitLab archive"),
    "val_2025_ord_reserva.pdf": (FQP + "valencia/2025-ord2-valencia-fisica-exam.pdf", "FiQuiPedia GitLab archive (reserve paper, not coded)"),
    "val_2025_ord_sol_angelcuesta.pdf": ("https://www.angelcuesta.com/data/Examenes%20PAU/CV/FISICA/", "unofficial worked solutions (not used)"),
    "val_2026_ord.pdf": ("https://universitats.gva.es/documents/389338055/393318629/Examen+FISI+junio+2026.pdf/9a3059a9-7b73-8257-f8f1-b4a08c848c8f", "downloaded from the user's computer (robots-blocked for the cloud fetcher)"),
    "val_2026_ord_crit.pdf": ("https://universitats.gva.es/documents/389338055/393318644/Criterios+FISI+junio+2026.pdf/0aa84d28-1233-301a-a28e-a55bdde7651e", "downloaded from the user's computer"),
    "clm_2025_ord_transcript.md": ("https://www.uclm.es/-/media/Files/A04-Gestion-Academica/PDFEstudiantes/PDFEvAU/ModelosPruebas2425/FISICA.ashx?la=es", "read in the built-in browser (WAF blocks automated download); transcribed, abridged"),
    "clm_2026_ord_transcript.md": ("https://www.uclm.es/-/media/Files/A04-Gestion-Academica/PDFEstudiantes/PDFEvAU/ModelosPruebas2526/Fisica_PAU_2026.ashx?la=es", "read in the built-in browser (WAF blocks automated download); transcribed, abridged"),
}
EXAMS = ROOT / "sources" / "exams"

rows = []
for f in sorted(EXAMS.iterdir()):
    if not f.is_file() or f.suffix not in (".pdf", ".md", ".zip"):
        continue
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    url, how = EXAM_URLS.get(f.name, ("", "curl (search agent)"))
    yr = f.name.split("_")[1]
    kind = "corrector document" if "crit" in f.name else ("transcript" if f.suffix == ".md" else ("zip as published" if f.suffix == ".zip" else "exam paper"))
    rows.append(dict(file=f"exams/{f.name}", bytes=f.stat().st_size, sha256=h,
                     description=f"Física ordinary {yr}, {kind}", url=url, retrieval=how))
# EHU archive 2010–2026: URL recovered from the download log by file size
HIST = ROOT / "sources" / "exams_ehu_hist"
size2url = {}
for line in (HIST / "urls_tried.log").read_text(errors="replace").splitlines():
    parts = line.split()
    if parts and parts[0] == "200":
        nums = [p for p in parts if p.isdigit()]
        urls = [p for p in parts if p.startswith("http")]
        if nums and urls:
            size2url.setdefault(int(nums[-1]), urls[-1])
for f in sorted(HIST.iterdir()):
    if f.suffix != ".pdf":
        continue
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    url = size2url.get(f.stat().st_size, "")
    stem = f.stem
    url = {"ehu_2024_ord": "https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica",
           "ehu_2024_extra": "https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica-1",
           "ehu_orient_2025_modelo_v0": "https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/fisica_mod_pau25-pdf"}.get(stem, url)
    if stem == "ehu_theory_list_official":
        desc = "Official EHU–Departamento de Educación list of 22 theory titles with development guide (pre-2025 'cuestiones teóricas', bilingual)"
        rows.append(dict(file=f"exams_ehu_hist/{f.name}", bytes=f.stat().st_size, sha256=h, description=desc, url="",
                         retrieval="provided by the coordinator (not published online), 19 Sep 2026"))
        continue
    if stem.startswith("ehu_orient"):
        desc = "EHU PAU 2025 model paper / guidance" + (" (Oct 2024 version)" if "v0" in stem else "")
    else:
        yr = stem.split("_")[1]
        sit = "extraordinary" if "extra" in stem else "ordinary"
        kind = "solucionario" if "crit" in stem else "exam paper"
        lang = " (Basque version)" if stem.endswith("_eu") else (" (bilingual)" if "bil" in stem else "")
        desc = f"EHU Física {sit} {yr}, {kind}{lang}"
    rows.append(dict(file=f"exams_ehu_hist/{f.name}", bytes=f.stat().st_size, sha256=h, description=desc, url=url,
                     retrieval="curl (search agent), ehu.eus archive pages"))
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
