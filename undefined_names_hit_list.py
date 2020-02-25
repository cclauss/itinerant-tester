#!/usr/bin/env python3

URL_BASE = "https://github.com/internetarchive/openlibrary/blob/master"
lines = []
start = ""
with open("junk.txt") as in_file:
    for line in in_file:
        if len(line.strip()) > 1:
            if line.startswith("./"):
                filepath, _, _, _, undefined_name = line.split()
                undefined_name = undefined_name.replace("'", "`")
                url = "{}{}#L{}".format(URL_BASE, *(filepath.lstrip(".").split(":")))
                start = f"- [ ] [{filepath}]({url}) {undefined_name}"
            else:
                lines.append(f"{start} in `{line.strip()}`")
print(f"{len(lines)} undefined names:")
print("\n".join(sorted(lines)))
