# What changes when your search index lives on S3?

_type: news-summary · created: 2026-10-17 · updated: 2026-10-20 · confidence: high_

`hacker-news`

## Summary

Infino is building a retrieval engine for agent queries - SQL, vector search, BM25 and combinations - and chose to put the search index on object storage (S3, GCS, Azure Blob) because that is where the data already lives. This post, first in a series, explains what has to change when the index leaves local disk: Lucene-style design assumes cheap random seeks next to the CPU, while every read from object storage is a network round-trip.

The design organizes data into superfiles - Parquet files carrying Infino's full-text and vector indexes - grouped into supertables, each with a manifest listing superfiles, footers, index headers and column statistics, plus a term index mapping terms to the superfiles containing them.

## Highlights

- Part 1 of a series on Infino's architecture for agent-scale retrieval
- Search index lives on object storage, not local disk
- Core challenge: random reads become network round-trips
- Data organized into superfiles: Parquet plus full-text and vector indexes
- Supertables add a manifest with statistics and a term index
- Supports SQL, vector and BM25 queries over the same store

## Source

[Read the original story](https://infino.ai/blog/search-index-on-s3/)

## Related pages

_No related entity or concept page yet._
