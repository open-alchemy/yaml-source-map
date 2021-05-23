# YamlSourceMap

Calculate JSON Pointers to each value within a YAML document along with the
line, column and character position for the start and end of that value.

For example:

```bash
python -m pip install yaml_source_map
```

```Python
from yaml_source_map import calculate


print(calculate('foo: bar'))
```

The above prints:

```Python
{
    "": Entry(
        value_start=Location(line=0, column=0, position=0),
        value_end=Location(line=0, column=8, position=8),
        key_start=None,
        key_end=None,
    ),
    "/foo": Entry(
        value_start=Location(line=0, column=5, position=5),
        value_end=Location(line=0, column=8, position=8),
        key_start=Location(line=0, column=0, position=0),
        key_end=Location(line=0, column=3, position=3),
    ),
}
```

The following features have been implemented:

- support for primitive types (`strings`, `numbers`, `booleans` and `null`),
- support for structural types (`sequence` and `mapping`).
