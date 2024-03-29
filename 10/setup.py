from setuptools import setup, Extension


def main():
    setup(
        name="cjson",
        version="1.0.0",
        description="Python module in C for json parsing and serialization",
        ext_modules=[Extension("cjson", ["cjson.c"])],
    )


if __name__ == "__main__":
    main()
