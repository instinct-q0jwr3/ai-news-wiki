# AI News Wiki

Feed acumulativo de noticias de IA desde Techmeme, Hacker News, Lobsters, Latent.Space y Stratechery.

Inspirado en el patrón [LLM Wiki de Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): fuentes crudas e inmutables, wiki Markdown acumulativa y un esquema `AGENTS.md` para mantenerla.

## Estado

La primera versión funcional está preparada. Incluye ingesta RSS/API, filtro auditable por términos de IA, snapshots JSON, informes diarios, índice, log y una GitHub Action manual sin costes recurrentes.

## Ejecutar

```bash
python3 src/update_feed.py
```

> Stratechery: solo usa su feed público. El RSS personalizado requiere cuenta Passport; una cuenta gratuita incluye artículos semanales y la suscripción de pago añade el Daily Update. El proyecto no incluye credenciales ni evita el muro de pago.
