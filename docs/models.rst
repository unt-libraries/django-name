
======
Models
======

Name
----
Name objects have a variety configurable options. 

Fields
''''''

``Name Type`` - One of `Personal`, `Organization`, `Software`, `Building`, or `Event`

``Biography`` - Markdown enable biography of the personal the Name record represents.

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
''''''''''''''
The Identifier contains an type, (see `Identifier Type`), and value which is often represented as a permalink. For instance, the link to the person's Twitter profile would be an Identifier.

Notes
''''''
Additional notes regarding the person or the Name record. 

Notes can be any of the following type:

- `Biographical/Historical`
- `Deletion Information`
- `Nonpublic`
- `Source`
- `Other`

Locations
''''''''''
Locations are represented by a pair of geographic coordinates, than enable some mapping features within the app. A Name's location may be either `current` or `former`, and a Name may only have one `current` location at any given time.

Misc Options
''''''''''''''

Name records are capable of being merged with other Name records. Once merged with another record, any attempts to retrieve information about the merged record with redirect users to the Name record the was the target of the merge.


Identifier type
---------------

Placeholder for information about the ``Identifier Type`` model.
