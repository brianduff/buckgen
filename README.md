# buckgen

A super simple, not very general, .classpath and .project generator for Buck.

This just calls Buck to get the classpath, then spits out .project and .classpath files that Eclipse or VSCode are happy with. That's it!

## Usage

Specify Buck targets and optionally a sourcepath root to use. E.g. 

```
buckgen.py --sourcepath src program/foo/bar:bar
```
