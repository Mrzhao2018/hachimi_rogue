# 在 VS Code 中自动激活虚拟环境

此工作区已包含 VS Code 工作区设置，目标是在打开集成终端时自动激活 Python 虚拟环境（Windows PowerShell）。

假设
- 虚拟环境位于工作区根目录的 `.venv` 文件夹（即 `.venv\Scripts\python.exe`）。
- 已安装并启用 `ms-python.python`（推荐的扩展，工作区已建议）。

快速步骤（PowerShell）

1. 在工作区根目录创建虚拟环境：

```powershell
python -m venv .venv
```

2. 如果首次激活遇到策略阻止（无法运行 Activate.ps1），可执行（仅当你了解并接受风险时）：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

3. 打开（或重启）VS Code，然后打开终端（PowerShell）。如果设置生效，终端左侧会显示 `(.venv)` 前缀，说明虚拟环境已自动激活。

手动测试激活：

```powershell
# 手动激活
.\.venv\Scripts\Activate.ps1
# 查看 Python 路径
python -c "import sys; print(sys.executable)"
```

如果你的虚拟环境不在 `.venv`，可以在 `.vscode/settings.json` 中把 `python.defaultInterpreterPath` 改为对应路径，例如：

```jsonc
"python.defaultInterpreterPath": "${workspaceFolder}\\myenv\\Scripts\\python.exe"
```

文件说明
- `.vscode/settings.json` — 设置解释器路径并启用终端激活。
- `.vscode/extensions.json` — 建议安装 Python 扩展。
- `README.md` — 本说明。

如需我把虚拟环境文件夹名改为其它默认名（比如 `venv` 或 `env`），或把设置改成基于 workspace 变量自动发现，请告诉我你的偏好，我可以直接修改工作区设置。