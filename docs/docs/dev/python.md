# Python

## Poetry

- `poetry config virtualenvs.in-project true` : 設定 Poetry 把 `.venv` 設定在專案資料夾下
- `poetry env use <python binary>` : 根據指定的 `<python binary>` 建立當前專案的虛擬環境，`<python binary>` 給的值如果不是絕對路徑系統會自己去 `$PATH` 裡面找
- `poetry add <package>` : 紀錄安裝 `<package>` 到 `pyproject.toml`，接著用 `pyproject.toml` 去更新 `poetry.lock`，最後用 `poetry.lock` 去更新虛擬環境
- `poetry lock` : 用 `pyproject.toml` 的資料更新 `poetry.lock`
- `poetry install` : 用 `poetry.lock` 的資料更新虛擬環境


---
## Reference
- [Build & Publish Python Packages With Poetry](https://www.freecodecamp.org/news/how-to-build-and-publish-python-packages-with-poetry/)
- [Poetry 入門](https://blog.kyomind.tw/python-poetry/)
- [Format Strings For PyArg_ParseTuple](https://docs.python.org/2.0/ext/parseTuple.html)
- [Python & C](https://medium.com/pyladies-taiwan/如py似c-python-與-c-的共生法則-568add0ba5b8)
- [asyncio 入門](https://www.youtube.com/watch?v=brYsDi-JajI)
- [async with](https://blog.csdn.net/tinyzhao/article/details/52684473)

