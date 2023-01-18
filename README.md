<h1 align="center">
  pypkg-deb
</h1>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/made%20with-blood,%20sweat,%20&amp%20tears-E760A4.svg" alt="Made with blood, sweat and tears">
  </a>
  <a href="https://github.com/LuzProject/pypkg-deb/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/LuzProject/pypkg-deb.svg" alt="Contributors">
  </a>
  <a href="https://github.com/LuzProject/pypkg-deb/commits/main" target="_blank">
    <img src="https://img.shields.io/github/commit-activity/w/LuzProject/pypkg-deb.svg" alt="Commits">
  </a>
</p>

<p align="center">
    A semi-port of `dpkg-deb` in pure Python.
</p>

## Features
1. Building .deb files
2. Extracting .deb files
3. Listing contents of .deb files

## pypkg-deb -h output

    usage: pypkg-deb [-h] [-b] [-x] [-c] [-v] [-Z Z] [-z Z] path

    positional arguments:
    path            path to operate on

    options:
    -h, --help      show this help message and exit
    -b, --build     build a .deb file from a directory
    -x, --extract   extracts the deb file
    -c, --contents  list the contents of the deb file
    -v, --version   show current version and exit
    -Z Z            specify a compression algorithm (gzip, xz, bzip). ignored unless using "-b"
    -z Z            specify a compression level (1-9); defaults to 9. ignored unless using "-b"

## TODO
1. -I command (list info of package from Control file)
2. -f command (get specific field from Control file)