# AI News Wiki

Feed acumulativo de noticias de IA desde Techmeme, Hacker News, Lobsters, Latent.Space y Stratechery.

Inspirado en el patrón [LLM Wiki de Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): fuentes crudas e inmutables, wiki Markdown acumulativa y un esquema `AGENTS.md` para mantenerla.

## Estado

La primera versión funcional está preparada. Incluye ingesta RSS/API, filtro auditable por términos de IA, snapshots JSON, informes diarios, índice, log y una GitHub Action manual sin costes recurrentes.

## Ejecutar

```bash
scripts/run_pass.sh
```

Ese entrypoint ejecuta ingesta, refresca la capa derivada y regenera el sitio estático de `site/`.

## Páginas derivadas

La ingesta (`src/update_feed.py`) solo genera snapshots crudos e informes diarios. Un pase de agente periódico mantiene las páginas derivadas de la wiki:

- `wiki/topics/`: una página por tema recurrente (modelos, agentes, regulación, hardware...), actualizada con las noticias acumuladas sobre ese tema.
- `wiki/entities/`: una página por empresa, producto o persona relevante, con su actividad reciente.
- `wiki/trends/`: análisis de tendencias a partir del histórico de `wiki/daily/`.
- `wiki/concepts/`: conceptos que conectan historias y entidades.
- `wiki/comparisons/`: comparativas vivas, con evidencia por lado.
- `wiki/weekly/`: síntesis semanal y señales a vigilar.
- `wiki/hubs/`: rutas editoriales que agrupan conceptos, temas, entidades y comparativas.
- `site/`: web estática navegable y buscable, generada desde todo lo anterior.

En cada pase el agente ejecuta `scripts/run_pass.sh`, revisa lo nuevo y puede ampliar la interpretación curada. El script mantiene los bloques de evidencia, la síntesis semanal, conceptos, comparativas, hubs, `wiki/index.md` y la web en `site/`; después se commitean `raw wiki site`. El pase corre cada 6 horas desde un agente externo; la Action de GitHub queda solo como botón manual de respaldo.

> Stratechery: solo usa su feed público. El RSS personalizado requiere cuenta Passport; una cuenta gratuita incluye artículos semanales y la suscripción de pago añade el Daily Update. El proyecto no incluye credenciales ni evita el muro de pago.
