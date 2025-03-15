NOTE: this dataset only has craters >50km diameter

- Derived/Final Dataset:
    - Hashes:
        - xxh3_64 : 'ea14d77f25f090c4',
        - md5     : '4e63fd2a7f1367d131ee606edcdfb5f7',
        - sha1    : '79113d236836e1d8bb53e517ab3cfc4afad2cac2',
        - sha256  : 'e48808ef670e39e812149e4731634d59964b7b3465b1be38eda920f890125bdc',



- Intermediate/Requisite Datasets:

    - [1] IAU Crater Names
        - Description:
            - Official IAU Crater Nomenclature as of 2024-11-26 (most recent being Melosh on 2024-10-23) totalling 1218 craters.
        - Source:
            - Go to "Gazetteer of Planetary Nomenclature" site: https://planetarynames.wr.usgs.gov/
            - (in left sidebar) Nomenclature > Mars System > Mars > craters: https://planetarynames.wr.usgs.gov/SearchResults?Target=20_Mars&Feature%20Type=9_Crater,%20craters
            - ^ At the bottom of the search page, you should see a link to download a CSV with all results. If you'd like to verify my hash, do not "Refine your search" with additional parameters, add/remove columns, or sort any columns in order to ensure the resulting CSV has a consistent hash.
        - Download (mirror):
            - 'IAU-crater-names_as-of_2024-11-26.csv'
                - link: https://rutgers.box.com/s/xjljza4gw9743dutlpez8m8ccgmkzfnd
                - sha256: 4c08fe5c2477d20ffdd088d45275fb1469fd2970900aa5b9aeff66160285a5ea

    - [2] Crater Ages
        - Description:
            - "Summary table of results for remaining 73 large craters, plus additional locations and sizes of unmappable craters D ⩾ 150 km."
        - Source:
            - DOI: https://doi.org/10.1016/j.icarus.2013.03.019
                - Authors: Robbins, Hynek, Lillis, Bottke
                - Title: "Large impact crater histories of Mars: The effect of different model crater age techniques"
                - Published: 2013 April
            - See download link for "Supplementary Table 3", we parse the `tex` file directly.
        - Download (mirror):
            - 'Table 3.tex'
                - link: https://rutgers.box.com/s/fdk83g5g5pn2kltrqodvwnvmvjbmggzh
                - sha256: f81bf35ba76f0f2e9939d7a338084451145cdc8d9771124ac4e8ec71802ea236
            - PDF for convenience: https://files.catbox.moe/fanjm8.pdf

    - [3] Crater Database (v2020)
        - Description:
            - Global database of Martian impact craters (2020 version).
        - Source:
            - Download site: https://craters.sjrdesign.net/
                - Maintainer: Robbins
            - [Companian paper] DOI: (1) https://doi.org/10.1029/2011JE003966, (2) https://doi.org/10.1029/2011JE003967
                - Authors: Robbins, Hynek
                - Title: "A new global database of Mars impact craters ≥1 km: [...]"
                - Published: 2012 May
        - Download (mirror):
            - 'Catalog_Mars_Release_2020_1kmPlus_FullMorphData.csv'
                - link: https://rutgers.box.com/s/sry0fof5brqu9pz2tfk6xfix7c3w1xyu
                - sha256: 348e5b88912e6e67b71fb4afffc8f76a170524e1308c171f98c805c045813c22
