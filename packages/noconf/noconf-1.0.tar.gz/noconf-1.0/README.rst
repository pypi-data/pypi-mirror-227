======
noconf
======

Key features
============

1. **Flexible configuration**: noconf allows you to configure your
   Python applications using configuration files that use Python
   syntax.

2. **Multiple configuration files**: noconf allows you to split your
   configuration across multiple files, making it easier to manage and
   update your configuration as your application grows.

3. **Configuration referencing**: noconf allows you to reference other
   parts of your configuration from within your configuration,
   avoiding duplication and keeping your configuration DRY (Don't
   Repeat Yourself).

4. **Component-based programming**: noconf enables you to initialize
   classes using your configuration, making it easy to compose complex
   systems out of smaller, reusable components. This promotes code
   reuse and maintainability.

Usage
=====

At a minimum, noconf allows us to read configuration that's stored in
files with Python syntax, where the file contains exactly one top
level dictionary.

Let's first write a very simple config file:

>>> config1_fname = folder / "config1.py"
>>> config1_fname.write_text("""
... {'key1': 'value1', 'key2': ['value2']}
... """)
40

>>> from noconf import load
>>> load(config1_fname)
{'key1': 'value1', 'key2': ['value2']}

We can also chain configuration files, that is, load multiple
configuration files and merge them, where contents of the files later
in the list of files to load will take precedence:

>>> config2_fname = folder / "config2.py"
>>> config2_fname.write_text("""
... {'key1': 'new', 'key3': {'__copy__': 'key2'}}
... """)
47
>>> load((config1_fname, config2_fname))  # a tuple of config files
{'key1': 'new', 'key2': ['value2'], 'key3': ['value2']}

Notice that in the above example, we also used a `'__copy__'` feature,
which allows us to refer to other parts in the configuration, and to
avoid duplication.

We can also instantiate classes directly from the configuration.
Let's create a configuration file that instantiates a Python logging
FileHandler class.  We're also going to configure the FileHandler with
a filename that's passed as an environment variable.  We use the
special `environ` variable in noconf to access environment variables:

>>> setenv("LOGFILE", str(folder / "mylogfile.txt"))

>>> config3_fname = folder / "config3.py"
>>> config3_fname.write_text("""
... {
...     'handlers': [
...         {
...             '!': 'logging.FileHandler',
...             'filename': environ['LOGFILE'],
...         },
...     ],
... }
... """)
135
>>> config = load(config3_fname)
>>> filehandler = config['handlers'][0]

>>> from pathlib import Path
>>> Path(filehandler.baseFilename).parts[-1]
'mylogfile.txt'
