# upddetect

Command line tool for search and detect available security (and not only) updates in various Linux distributions.

Currently it's just early version. Feel free to test it, write issues and contribute!

# Supported packet managers

* pip (package installer for Python, including pip in virtual environments)
* APT (apt-get, apt)

# Install

```
pip install upddetect
```

# Usage

```
usage: upddetect [options]
Options:
-s: detect only security updates
-d: detect only dist updates
-a: detect all updates
-j: work silently, display json when finished
-v: show version
```

# Example

![Screenshot](screens/screen1.png?raw=true "Screenshot")
![Screenshot](screens/screen2.png?raw=true "Screenshot")

It could also be in JSON format for some monitoring or automations,
just use flag ```-j```.

