root := justfile_directory()
package-fork := x'$TYPST_PKG_FORK'
export TYPST_ROOT := root

[private]
default:
    @just --list --unsorted

# generate assets
assets:
    python3 scripts/bundle.py
    typst compile assets/example.typ assets/example.png
    typst compile assets/icons.typ assets/icons.png

# generate manual
doc: assets

# run test suite
test *args:
    tt run {{ args }}

# update test cases
update *args:
    tt update {{ args }}

# package the library into the specified destination folder
package target:
    ./scripts/package "{{ target }}"

# install the library with the "@local" prefix
install: (package "@local")

# install the library with the "@preview" prefix (for pre-release testing)
install-preview: (package "@preview")

# create a symbolic link to this library in the target repository
link target="@local":
    ./scripts/link "{{ target }}"

link-preview: (link "@preview")

# bump version number
bump VERSION:
    tbump {{ VERSION }}

[private]
[working-directory(x'$TYPST_PKG_FORK')]
prepare-fork:
    git checkout main
    git pull typst main
    git push origin --force

# prepare: (package package-fork)
prepare: prepare-fork (package package-fork)

[private]
remove target:
    ./scripts/uninstall "{{ target }}"

# uninstalls the library from the "@local" prefix
uninstall: (remove "@local")

# uninstalls the library from the "@preview" prefix (for pre-release testing)
uninstall-preview: (remove "@preview")

# unlinks the library from the "@local" prefix
unlink: (remove "@local")

# unlinks the library from the "@preview" prefix
unlink-preview: (remove "@preview")

# run ci suite
ci: test doc
