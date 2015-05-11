
======
Models
======

- :ref:`name-model-ref`
- :ref:`identifier-type-model-ref`

.. _name-model-ref:

Name
----
Name objects have a variety configurable options. 

Fields
''''''

``Name`` - The canonical form of the name.

``Name Type`` - One of `Personal`, `Organization`, `Software`, `Building`, or `Event`

``Biography`` - Markdown enabled biography of the personal the Name record represents.

``Begin`` - The starting date for the Name record. This will be different for each Name Type, for instance, this field would be the birth date for a `Personal` name, and the erected date for a `Building` name.

``End`` - Similar to ``Begin``

``Disambiguation`` - Clarification to whom or what the record pertains.


Variants
''''''''
Variants are additional ways that the Name can be displayed.

Options include:

- `Acronym` 
- `Abbreviation`
- `Expansion`
- `Translation`
- `Other`

Identifiers
'''''''''''
The Identifier contains an type, (see :ref:`identifier-type-model-ref`), and value which is often represented as a permalink. For instance, the link to the person's Twitter profile would be an Identifier.

Notes
'''''
Additional notes regarding the person or the Name record. 

Notes can be any of the following type:

- `Biographical/Historical`
- `Deletion Information`
- `Nonpublic`
- `Source`
- `Other`

Locations
'''''''''
Locations are represented by a pair of geographic coordinates, than enable some mapping features within the app. A Name's location may be either `current` or `former`, and a Name may only have one `current` location at any given time.

Misc Options
''''''''''''

Name records are capable of being merged with other Name records. Once merged with another record, any attempts to retrieve information about the merged record with redirect users to the Name record the was the target of the merge.


.. _identifier-type-model-ref:

Identifier Type
---------------

These are customizable types for the Name Variants. 

Fields
''''''

``Label`` - How the Identifier should be displayed.

``Icon Path`` - Relative path to the icon.

``Homepage`` - URL to the homepage of the service or website.

There are 14 ``Identifier Types`` that are provided on install. Those types are

- Academia
- Facebook
- Google Scholar
- Homepage
- Linkedin
- LOC
- ORD ID
- ResearchGate
- Scopus
- Tumblr
- Twitter
- UNT Faculty
- VIAF
- Wikipedia
