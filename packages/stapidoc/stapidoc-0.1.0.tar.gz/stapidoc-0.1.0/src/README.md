# stapidoc

v0.1.0  
©2023 Jonas Santoso

**sta**tic **p**age **i**nline **d**ecoder **o**f **c**hoice

## Install

```shell
pip install stapidoc
```

## Usage

```shell
stapidoc input_file
```

Resulting document is written to `stdout`.

Given a static HTML document ('source'), *stapidoc* creates another HTML document which contains the source as a [percent](https://datatracker.ietf.org/doc/html/rfc3986.html#section-2.1)‑and‑base64‑encoded string, along with an inline script that decodes this string and plugs the source's DOM on‑the‑fly upon loading.

The source's `<link>` elements are plugged into the resulting DOM's `<head>` separately in order for linked resources to load.

Tacit assumptions:
  - The source document is entirely static. There are no `<script>` elements in either head or body.
  - The source document uses UTF-8 encoding.
