---
name: gb_index
title: Composite GB IMD Index
description: "Composite index that combines three national IMD indexes (Excluding\
  \ Northern Ireland)\n"
version: latest
licenses:
- name: CC-BY-4.0
  path: https://creativecommons.org/licenses/by/4.0/
  title: Creative Commons Attribution 4.0 International License
contributors:
- title: mySociety
  path: https://mysociety.org
  role: author
custom:
  build: composite_uk_imd.__main__:update_data_and_build
  tests:
  - test_composite_uk_imd_index
  dataset_order: 0
  download_options:
    gate: default
    survey: default
    header_text: default
  composite:
    xlsx:
      include: all
      exclude: none
      render: true
    sqlite:
      include: all
      exclude: none
      render: true
    json:
      include: all
      exclude: none
      render: false
  change_log:
    1.0.0: Initial release of dataset.
    1.0.1: 'Minor change in data for resource(s): gb_imd_e,gb_imd_s,gb_imd_w'
    1.0.2: 'Minor change in data for resource(s): gb_imd_e,gb_imd_s,gb_imd_w'
    1.0.3: 'gb_imd_e: example changed from E01021988 to E01000001'
  formats:
    csv: true
    parquet: true
resources:
- title: GB_IMD_E
  description: England-anchored composite GB Index. England IMD rank ordering will
    be preserved.
  custom:
    row_count: 41729
  path: GB_IMD_E.csv
  name: gb_imd_e
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of GB Nation (E, S, W)
      constraints:
        unique: false
        enum:
        - E
        - W
        - S
      example: E
    - name: lsoa
      type: string
      description: GB small statistical area (LSOA, DZ)
      constraints:
        unique: true
      example: E01000001
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 0.5
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: GB_IMD_E_score
      type: number
      description: The composite score for the GB wide composite, with other nations
        re-predicted based on England model.
      constraints:
        unique: false
      example: 0.541
    - name: original_decile
      type: integer
      description: Deprivation decile in original index.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: E_expanded_decile
      type: integer
      description: Based on bands of original index, fit other nations into same bands.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_E_rank
      type: number
      description: Rank ordering of all LSOA/az by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: GB_IMD_E_pop_decile
      type: integer
      description: LSOAs divided into ten deciles of even population (not LSOA count).
        Decile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_E_pop_quintile
      type: integer
      description: LSOAs divided into five quintiles of even population (not LSOA
        count). Quintile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
      example: 1
  hash: 3c9d2c45254b5610b663f89c8f5127e3
- title: GB_IMD_S
  description: Scotland-anchored composite GB Index. Scotland IMD rank ordering will
    be preserved.
  custom:
    row_count: 41729
  path: GB_IMD_S.csv
  name: gb_imd_s
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of GB Nation (E, S, W)
      constraints:
        unique: false
        enum:
        - E
        - W
        - S
      example: E
    - name: lsoa
      type: string
      description: GB small statistical area (LSOA, DZ)
      constraints:
        unique: true
      example: E01000001
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 0.5
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: GB_IMD_S_score
      type: number
      description: The composite score for the GB wide composite, with other nations
        re-predicted based on Scotland model.
      constraints:
        unique: false
      example: 0.9816448989246505
    - name: original_decile
      type: integer
      description: Deprivation decile in original index.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: S_expanded_decile
      type: integer
      description: Based on bands of original index, fit other nations into same bands.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_S_rank
      type: number
      description: Rank ordering of all LSOA/az by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: GB_IMD_S_pop_decile
      type: integer
      description: LSOAs divided into ten deciles of even population (not LSOA count).
        Decile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_S_pop_quintile
      type: integer
      description: LSOAs divided into five quintiles of even population (not LSOA
        count). Quintile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
      example: 1
  hash: e5c62bd4fda230030caa2a45d596be2b
- title: GB_IMD_W
  description: Wales-anchored composite GB Index. Wales IMD rank ordering will be
    preserved.
  custom:
    row_count: 41729
  path: GB_IMD_W.csv
  name: gb_imd_w
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of GB Nation (E, S, W)
      constraints:
        unique: false
        enum:
        - W
        - E
        - S
      example: E
    - name: lsoa
      type: string
      description: GB small statistical area (LSOA, DZ)
      constraints:
        unique: true
      example: E01000001
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 0.5
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 0.0
    - name: GB_IMD_W_score
      type: number
      description: The composite score for the GB wide composite, with other nations
        re-predicted based on Wales model.
      constraints:
        unique: false
      example: -4.168546562431074
    - name: original_decile
      type: integer
      description: Deprivation decile in original index.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: W_expanded_decile
      type: integer
      description: Based on bands of original index, fit other nations into same bands.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_W_rank
      type: number
      description: Rank ordering of all LSOA/az by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: GB_IMD_W_pop_decile
      type: integer
      description: LSOAs divided into ten deciles of even population (not LSOA count).
        Decile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        - 8
        - 9
        - 10
      example: 1
    - name: GB_IMD_W_pop_quintile
      type: integer
      description: LSOAs divided into five quintiles of even population (not LSOA
        count). Quintile 1 is most deprived.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
      example: 1
  hash: 2ac0723fc09c65162a8aa17d9b4f39f4
full_version: 1.0.3
permalink: /datasets/gb_index/latest
---
