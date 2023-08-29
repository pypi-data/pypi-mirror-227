<!--- This is a markdown file.  Comments look like this --->
<table>
  <tr>
    <td colspan=2><strong>
    fleks
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
  <tr>
    <td width=15%><img src=https://github.com/elo-enterprises/fleks/blob/master/img/icon.png?raw=true style="width:250px"></td>
    <td>
    Python application framework
    <br/><br/>
    <a href=https://pypi.python.org/pypi/fleks/><img src="https://img.shields.io/pypi/l/fleks.svg"></a>
    <a href=https://pypi.python.org/pypi/fleks/><img src="https://badge.fury.io/py/fleks.svg"></a>
    <a href="https://github.com/elo-enterprises/fleks/actions/workflows/python-test.yml"><img src="https://github.com/elo-enterprises/fleks/actions/workflows/python-test.yml/badge.svg"></a>    
    </td>
  </tr>
</table>

  * [Overview](#overview)
  * [Features](#features)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Tags &amp; Tagging](#tags--tagging)
    * [Class-Properties](#class-properties)
    * [Typing helpers](#typing-helpers)
    * [Base-classes for Configuration](#base-classes-for-configuration)


---------------------------------------------------------------------------------

## Overview

*(This is experimental; API-stability is not guaranteed.)*

Application framework for python.  


---------------------------------------------------------------------------------

## Features 

* CLI parsing with [click](https://click.palletsprojects.com/en/8.1.x/)
* Console output with [rich](https://rich.readthedocs.io/en/stable/index.html)
* Plugin Framework
* Exit-handlers, conventions for handling logging, etc

---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/fleks/) for available releases.

```bash
pip install fleks
```

---------------------------------------------------------------------------------

## Usage

See also [the unit-tests](tests/units) for some examples of library usage.

### Tags & Tagging

```python

from fleks import tagging

@tagging.tag(key="Value")
class MyClass():
   pass
 tagging.tag(key="Value")(MyClass)

assert tagging.tags[MyClass]['key']=="Value"
```

### Class-Properties

```python
import fleks


class Test:
    @fleks.classproperty
    def testing(kls):
        return 42


assert Test.testing == 42
```

### Typing helpers

```python

>>> from fleks.util import typing
```

### Base-classes for Configuration

```
Placeholder
```

---------------------------------------------------------------------------------
