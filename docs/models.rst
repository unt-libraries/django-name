
======
Models
======

- :ref:`name-model-ref`
- :ref:`identifier-type-model-ref`

.. _name-model-ref:

Name
----
Name objects have a variety of configurable options. 

Fields
''''''

``name`` - The canonical form of the name.

``name_type`` - One of `Personal`, `Organization`, `Software`, `Building`, or `Event`

``biography`` - Markdown enabled biography of the entity that the Name record represents.

``begin`` - The starting date for the Name record. This will be different for each Name Type, for instance, this field would be the birth date for a `Personal` name and the erected date for a `Building` name.

``end`` - Similar to ``begin``

``disambiguation`` - Clarification to whom or what the record pertains.

.. _variant-model-ref:

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
The Identifier contains a type, (see :ref:`identifier-type-model-ref`), and value which is often represented as a permalink. For instance, the link to the person's Twitter profile would be an Identifier.

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
Locations are represented by a geographic coordinate, which enable some mapping features within the app when present. A Name's location may be either ``current`` or ``former``, and a Name may only have one ``current`` location at any given time.

Misc Options
''''''''''''

Name records are capable of being merged with other Name records. Once merged with another record, any attempts to retrieve information about the merged record will redirect users to the Name record the was the target of the merge.


.. _identifier-type-model-ref:

Identifier Type
---------------

These are customizable types for the Name :ref:`variant-model-ref`. 

Fields
''''''

``label`` - How the Identifier should be displayed.

``icon_path`` - Relative path to the icon.

``homepage`` - URL to the homepage of the service or website.

There are 13 ``Identifier Types`` that are provided on install. Those types are

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
- VIAF
- Wikipedia
