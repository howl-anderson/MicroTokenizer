def main():
    # build indexes from 'scripts.txt'

    idx = []
    names = []
    cats = []

    import urllib.request
    import re
    import textwrap

    url = "http://www.unicode.org/Public/UNIDATA/Scripts.txt"
    f = urllib.request.urlopen(url)
    for ln in f:
        ln = ln.decode()
        p = re.findall(r"([0-9A-F]+)(?:\.\.([0-9A-F]+))?\W+(\w+)\s*#\s*(\w+)", ln)
        if p:
            a, b, name, cat = p[0]
            if name not in names:
                names.append(name)
            if cat not in cats:
                cats.append(cat)
            idx.append(
                (int(a, 16), int(b or a, 16), names.index(name), cats.index(cat))
            )
    idx.sort()

    print(
        'script_data = {\n"names":%s,\n"cats":%s,\n"idx":[\n%s\n]}'
        % (
            "\n".join(textwrap.wrap(repr(names), 80)),
            "\n".join(textwrap.wrap(repr(cats), 80)),
            "\n".join(
                textwrap.wrap(", ".join("(0x%x,0x%x,%d,%d)" % c for c in idx), 80)
            ),
        )
    )


if __name__ == "__main__":
    main()
