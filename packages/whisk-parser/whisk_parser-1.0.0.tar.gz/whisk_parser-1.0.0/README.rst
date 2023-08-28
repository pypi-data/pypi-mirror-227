==============

Whisk Parser

==============

Parse emails from Vosk API and Whisper.

++++++++++++

Installation

++++++++++++

Please make sure that you have **updated pip** to the latest version before installing whisk-parser.

You can install the module using Python Package Index using the below command.

.. code-block:: python

  pip install whisk_parser

+++++

Usage

+++++

First you have to import the module using the below code.

.. code-block:: python

    import whisk_parser as wp

Then you can use the **parse_email** method to convert a string to a valid email.

.. code-block:: python

    >>> print(wp.parse_email('my email is john at gmail.com'))
    my email is john@gmail.com

    >>> print(wp.parse_email('my email is john underscore doe at gmail.com'))
    my email is john_doe@gmail.com

    >>> print(wp.parse_email('The aggregate and underlying individual governance indicators are available at www.govindicators.org.'))
    The aggregate and underlying individual governance indicators are available at www.govindicators.org.



++++++++++++

Contributors

++++++++++++

- Luis Alfredo Reyes (`runesc <https://github.com/runesc>`__)
