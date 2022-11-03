---
name: uk_index
title: Composite UK IMD Index
description: "Composite index that combines four national IMD indexes\n"
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
  - test_composite_uk_imd
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
    2.0.0: Updated release of datset fixing incorrect comparison of NI SOAs.
    1.0.0: Initial release of dataset.
    2.1.0: 'New resource(s) added: la_labels'
    2.1.1: 'Minor change in data for resource(s): la_labels,uk_imd_e,uk_imd_n,uk_imd_s,uk_imd_w'
    3.0.0: Tidied up and added LA/Constituency level deprivation scores
resources:
- title: Local Authority deprivation
  description: Deprivation scores calculated for local authorities from UK (E) index.
  custom:
    row_count: 409
  path: la_imd.csv
  name: la_imd
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: local-authority-code
      type: string
      description: 3/4 letter local authority code.
      constraints:
        unique: true
      example: DRS
    - name: official-name
      type: string
      description: Full name of local authority.
      constraints:
        unique: true
      example: Derry City and Strabane District Council
    - name: la-deprivation-score
      type: number
      description: Composite score calculated for the local authority geography.
      constraints:
        unique: true
      example: 62.310842986626255
    - name: label
      type: string
      description: Quintile label - Quintiles are calclated for lower-tiers, and higher
        geographies are slotted in depending on score.
      constraints:
        unique: false
        enum:
        - 1st IMD quintile
        - 2nd IMD quintile
        - 3rd IMD quintile
        - 4th IMD quintile
        - 5th IMD quintile
      example: 1st IMD quintile
    - name: desc
      type: string
      description: Fuller description of quintile label
      constraints:
        unique: false
        enum:
        - Councils in most deprived quintile (20%)
        - Councils in second most deprived quintile (20%)
        - Councils in middle deprivation quintile (20%)
        - Councils in second least deprived quintile (20%)
        - Councils in least deprived quintile (20%)
      example: Councils in most deprived quintile (20%)
    - name: low-deprivation
      type: number
      description: Proportion of LA population living in a low deprivation losa (quintile
        4,5)
      constraints:
        unique: false
      example: 0.0
    - name: medium-deprivation
      type: number
      description: Proportion of LA population living in a medium deprivation losa
        (quintile 2,3)
      constraints:
        unique: true
      example: 0.1400214166732767
    - name: high-deprivation
      type: number
      description: Proportion of LA population living in a high deprivation lsoa (quintile
        1)
      constraints:
        unique: false
      example: 0.8599785833267233
    - name: density
      type: number
      description: Population density (people per km2)
      constraints:
        unique: true
      example: 120.79056754596324
    - name: la-imd-pop-quintile
      type: integer
      description: Local authorities grouped into five quintiles. Quintile 1 is councils
        with highest deprivation that account for 1/5 of population (not 1/5 of councils).
        Higher level authorites are slotted into based on scores.
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
      example: 1
    - name: la-imd-pop-decile
      type: integer
      description: Local authorities grouped into 10 decile. Decile 1 is councils
        with highest deprivation that account for 1/10 of population (not 1/10 of
        councils). Higher level authorites are slotted into based on scores.
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
  _sheet_order: 1
  hash: dc0cfa31acbb13a85ebcff61de41590f
  download_id: uk-index-la-imd
- title: Westminster Constituency deprivation
  description: Deprivation scores calculated for parliamentary constituencies from
    UK (E) index.
  custom:
    row_count: 650
  path: constituency_imd.csv
  name: constituency_imd
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: gss-code
      type: string
      description: GSS code for 2010-set Westminster Parliamentary constituencies
      constraints:
        unique: true
      example: N06000004
    - name: constituency-name
      type: string
      description: Name of constituency
      constraints:
        unique: true
      example: Belfast West
    - name: pcon-deprivation-score
      type: number
      description: Composite score calculated for the constituency geography.
      constraints:
        unique: true
      example: 71.9006169718264
    - name: label
      type: string
      description: IMD Quintile of constituency
      constraints:
        unique: false
        enum:
        - 1st IMD quintile
        - 2nd IMD quintile
        - 3rd IMD quintile
        - 4th IMD quintile
        - 5th IMD quintile
      example: 1st IMD quintile
    - name: desc
      type: string
      description: Fuller description of label
      constraints:
        unique: false
        enum:
        - Constituencies in most deprived quintile (20%)
        - Constituencies in second most deprived quintile (20%)
        - Constituencies in middle deprivation quintile (20%)
        - Constituencies in second least deprived quintile (20%)
        - Constituencies in least deprived quintile (20%)
      example: Constituencies in most deprived quintile (20%)
    - name: low-deprivation
      type: number
      description: Proportion of constituency population living in a low deprivation
        losa (quintile 4,5)
      constraints:
        unique: false
      example: 0.0
    - name: medium-deprivation
      type: number
      description: Proportion of constituency population living in a low deprivation
        losa (quintile 2,3 )
      constraints:
        unique: true
      example: 0.0461904007603358
    - name: high-deprivation
      type: number
      description: Proportion of constituency population living in a high deprivation
        lsoa (quintile 1)
      constraints:
        unique: false
      example: 0.953809599239664
    - name: pcon-imd-pop-quintile
      type: integer
      description: Constituencies grouped into five quintiles. Quintile 1 is constituencies
        with highest deprivation that account for 1/5 of population (not 1/5 of constituencies)
      constraints:
        unique: false
        enum:
        - 1
        - 2
        - 3
        - 4
        - 5
      example: 1
    - name: pcon-imd-pop-decile
      type: integer
      description: Constituencies grouped into ten deciles. Decile 1 is constituencies
        with highest deprivation that account for 1/10 of population (not 1/5 of constituencies)
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
  _sheet_order: 2
  hash: ee0f3bf77ce51ef068a11fe0b1f3e9da
  download_id: uk-index-constituency-imd
- title: UK_IMD_E
  description: England-anchored composite UK Index. English IMD rank ordering will
    be preserved.
  custom:
    row_count: 42619
  path: UK_IMD_E.csv
  name: uk_imd_e
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of UK Nation (N, E, S, W)
      constraints:
        unique: false
        enum:
        - N
        - E
        - S
        - W
      example: N
    - name: lsoa
      type: string
      description: UK small statistical area (LSOA, DZ, SOA)
      constraints:
        unique: true
      example: 95ZZ06W1
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the individual index
      constraints:
        unique: false
      example: 75.19204448526636
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 25.8
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 53.0
    - name: UK_IMD_E_score
      type: number
      description: The composite score for the UK wide composite, with other nations
        re-predicted based on English model.
      constraints:
        unique: false
      example: 123.00849692191194
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
      description: Based on bands of original English index, fit other nations into
        same bands.
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
    - name: UK_IMD_E_rank
      type: number
      description: Rank ordering of all LSOA by this index. One is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: UK_IMD_E_pop_decile
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
    - name: UK_IMD_E_pop_quintile
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
  hash: 0f1216618a5b986a5beaf4a385c7c028
  download_id: uk-index-uk-imd-e
- title: UK_IMD_N
  description: Northern Ireland anchored composite UK Index. Northern Ireland IMD
    rank ordering will be preserved.
  custom:
    row_count: 42619
  path: UK_IMD_N.csv
  name: uk_imd_n
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of UK Nation (N, E, S, W)
      constraints:
        unique: false
        enum:
        - N
        - S
        - E
        - W
      example: N
    - name: lsoa
      type: string
      description: UK small statistical area (LSOA, DZ, SOA)
      constraints:
        unique: true
      example: 95ZZ06W1
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 75.19204448526636
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 25.8
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 53.0
    - name: UK_IMD_N_score
      type: number
      description: The composite score for the UK wide composite, with other nations
        re-predicted based on Northern Ireland model.
      constraints:
        unique: false
      example: 75.19204448526636
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
    - name: N_expanded_decile
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
    - name: UK_IMD_N_rank
      type: number
      description: Rank ordering of all LSOA by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: UK_IMD_N_pop_decile
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
    - name: UK_IMD_N_pop_quintile
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
  hash: 9650db4ef4ca23a9e224d4fe61ff75e8
  download_id: uk-index-uk-imd-n
- title: UK_IMD_S
  description: Scotland-anchored composite UK Index. Scotland IMD rank ordering will
    be preserved.
  custom:
    row_count: 42619
  path: UK_IMD_S.csv
  name: uk_imd_s
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of UK Nation (N, E, S, W)
      constraints:
        unique: false
        enum:
        - N
        - E
        - S
        - W
      example: N
    - name: lsoa
      type: string
      description: UK small statistical area (LSOA, DZ, SOA)
      constraints:
        unique: true
      example: 95GG35S2
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 68.03145551017063
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 18.8
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 59.4
    - name: UK_IMD_S_score
      type: number
      description: The composite score for the UK wide composite, with other nations
        re-predicted based on Scottish model.
      constraints:
        unique: false
      example: 128.81086921571062
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
    - name: UK_IMD_S_rank
      type: number
      description: Rank ordering of all LSOA by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: UK_IMD_S_pop_decile
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
    - name: UK_IMD_S_pop_quintile
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
  hash: 7d1d5d7cc0649cc12c0612b7b711055c
  download_id: uk-index-uk-imd-s
- title: UM_IMD_W
  description: Wales-anchored composite UK Index. Wales IMD rank ordering will be
    preserved.
  custom:
    row_count: 42619
  path: UK_IMD_W.csv
  name: uk_imd_w
  profile: tabular-data-resource
  scheme: file
  format: csv
  hashing: md5
  encoding: utf-8
  schema:
    fields:
    - name: nation
      type: string
      description: One letter string of UK Nation (N, E, S, W)
      constraints:
        unique: false
        enum:
        - N
        - E
        - S
        - W
      example: N
    - name: lsoa
      type: string
      description: UK small statistical area (LSOA, DZ, SOA)
      constraints:
        unique: true
      example: 95ZZ06W1
    - name: overall_local_score
      type: number
      description: The overall IMD score for this area in the indiviudal index
      constraints:
        unique: false
      example: 75.19204448526636
    - name: income_score
      type: number
      description: The Income subdomain score in the individual index
      constraints:
        unique: false
      example: 25.8
    - name: employment_score
      type: number
      description: The Employment subdomain score in the individual index
      constraints:
        unique: false
      example: 53.0
    - name: UK_IMD_W_score
      type: number
      description: The composite score for the UK wide composite, with other nations
        re-predicted based on Wales model.
      constraints:
        unique: false
      example: 133.27419581040678
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
    - name: UK_IMD_W_rank
      type: number
      description: Rank ordering of all LSOA by this index. Rank 1 is most deprived.
      constraints:
        unique: false
      example: 1.0
    - name: UK_IMD_W_pop_decile
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
    - name: UK_IMD_W_pop_quintile
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
      example: 1
  hash: c0d0acd7836ee8e263987b1b4f6d80e3
  download_id: uk-index-uk-imd-w
full_version: 3.0.0
permalink: /datasets/uk_index/latest
---
