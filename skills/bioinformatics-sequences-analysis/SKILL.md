---
name: bioinformatics-sequences-analysis
description: "Use when analyzing bio sequences. Genomics, alignment."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [bioinformatics, genomics, proteomics, biotech, alignment]
    related_skills: [genomics-data-processing, drug-discovery-pipeline]
---

# Bioinformatics Sequences Analysis

## Overview
Systematically process biological sequences (DNA, RNA, proteins) using industry-standard tools. Covers FASTA/FASTQ/SAM/BAM/VCF formats, quality control, alignment, assembly, annotation, and statistical analysis. Produces reproducible analysis pipelines.

## When to Use
- "Analyze DNA/RNA/protein sequences"
- "Run BLAST search and interpret results"
- "Perform genome assembly from raw reads"
- "Do phylogenetic tree construction"

## File Formats
| Format | Content | Tools |
|--------|---------|-------|
| FASTA | Sequences with headers | biopython, samtools |
| FASTQ | Sequences + quality scores | fastp, fastqc |
| SAM/BAM | Aligned reads | samtools, picard |
| VCF | Variants | bcftools, gatk |

## Core Pipeline
1. Quality check (FastQC)
2. Trimming (fastp)
3. Alignment (BWA/STAR/minimap2)
4. Post-processing (samtools/picard)
5. Quantification/Annotation

## Common Pitfalls
1. Wrong aligner for data type — use splice-aware for RNA-seq
2. Skipping QC — wastes compute on bad data
3. Not indexing BAM files — samtools fails
4. Ignoring reference genome version mismatch

## Verification Checklist
- [ ] FASTQ validated with BioPython
- [ ] Quality passes thresholds
- [ ] Alignment rate >80%
- [ ] Output properly indexed
- [ ] Results reproducible