"""Poll the watch-list URLs (predictable paths of the next publications) and report HTTP status + size.
No search engine involved; safe to re-run at any time.  Output: logs/watchlist_poll_<date>.md"""
import datetime, subprocess, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
W = [
 ("Cataluña Recull estadístic PAU 2026", "https://universitats.gencat.cat/web/.content/01_acces_i_admissio/pau/documents/informes_i_estad/pau_estadistiques_2026.pdf"),
 ("Cataluña Recull juny 2026 (alt name)", "https://universitats.gencat.cat/web/.content/01_acces_i_admissio/pau/documents/informes_i_estad/pau_estadistiques_juny_2026.pdf"),
 ("Aragón pauresulasig2026.xlsx", "https://academico.unizar.es/sites/academico/files/archivos/acceso/estad/pauresulasig2026.xlsx"),
 ("Aragón pauresulasig2026.pdf", "https://academico.unizar.es/sites/academico/files/archivos/acceso/estad/pauresulasig2026.pdf"),
 ("Aragón pauresul2026.pdf", "https://academico.unizar.es/sites/academico/files/archivos/acceso/estad/pauresul2026.pdf"),
 ("Navarra Informe_PAU_2025-26.pdf", "https://www2.unavarra.es/gesadj/Estudios/acceso_matricula/PAU/Informe_PAU_2025-26.pdf"),
 ("Cantabria Resultados por Materia Ordinaria 2026", "https://web.unican.es/admision/Documents/Acceso/Resultados%20por%20Materia%20PAU%20Ordinaria%202026_Web.pdf"),
 ("Cantabria Resultados por Materia Extraordinaria 2026", "https://web.unican.es/admision/Documents/Acceso/Resultados%20por%20Materia%20PAU%20Extraordinaria%202026_Web.pdf"),
 ("UMA ponencia Física 26-27", "https://www.uma.es/media/files/PRESENTACI%C3%93N_PONENCIA_UMA_26-27.pdf"),
 ("Canarias acta 1 Física PAU-27 (guess 1)", "https://www.gobiernodecanarias.org/cmsgob1/export/sites/educacion/web/bachillerato/_galerias/descargas/pau-2027/"),
 ("Murcia informe general PAU2026 (guess doc 3)", "https://www.um.es/documents/d/estudios/co-pau2027-1-doc-3-informe-general-pau2026"),
 ("UVa resultados-acceso-2026.pdf", "https://pruebasdeacceso.uva.es/wp-content/uploads/resultados-acceso-2026.pdf"),
 ("EHU estadísticas page", "https://www.ehu.eus/es/web/unibertsitaterako-sarbidea/pruebas-de-acceso/estadisticas-de-la-prueba-de-acceso"),
 ("EHU informe PAU 2026 (guess)", "https://www.ehu.eus/documents/d/unibertsitaterako-sarbidea/informe-pau_2026-1-"),
 ("GV Resultados escolares 2025-2026 (guess)", "https://www.euskadi.eus/contenidos/informacion/eskola_emaitzak_ikuskaritza/es_def/adjuntos/resultados-escolares-Todo-2025-2026.pdf"),
 ("GV Resultados escolares index", "https://www.euskadi.eus/resultados-escolares-inspeccion-de-educacion/web01-a2hikus/es/"),
 ("CiUG grupos de traballo", "https://ciug.gal/grupos-de-traballo"),
 ("Ministry SIIU PAU landing", "https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/PAU.html"),
 ("Madrid statistics page", "https://www.comunidad.madrid/educacion/examenes-pau-estadisticas"),
 ("GVA estadístiques", "https://universitats.gva.es/es/estadistiques"),
 ("UPNA informe page", "https://www.unavarra.es/sites/estudios/acceso-y-admision/informacion-evau-profesorado.html"),
 ("ULPGC informes PAU page", "https://www.ulpgc.es/direccion-acceso/informes-ebau-powerbi-2021"),
]
rows=[]
for name,url in W:
    try:
        out=subprocess.run(["curl","-sS","-o","/dev/null","-L","-A","Mozilla/5.0","--max-time","40","-w","%{http_code} %{size_download} %{content_type}",url],capture_output=True,text=True,timeout=60)
        st=out.stdout.strip() or ("ERR "+out.stderr.strip()[:80])
    except Exception as e:
        st="ERR "+str(e)[:80]
    rows.append((name,url,st)); print(f"{st:40s} {name}")
d=datetime.date.today().isoformat()
p=ROOT/"logs"/f"watchlist_poll_{d}.md"
p.write_text("# Watch-list poll "+d+"\n\n| Target | Status | URL |\n|---|---|---|\n"+"\n".join(f"| {n} | `{s}` | <{u}> |" for n,u,s in rows)+"\n",encoding="utf-8")
print("written",p)
