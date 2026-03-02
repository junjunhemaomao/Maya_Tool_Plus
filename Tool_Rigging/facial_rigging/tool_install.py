# -*- coding: utf-8 -*-

from maya import cmds
import os
import ssl
import sys
import shutil
import urllib.request
import urllib.error
import importlib.util


GITHUB_BASE_RAW = "https://raw.githubusercontent.com/junjunhemaomao/Maya_Tool_Plus/main/Tool_Rigging/facial_rigging"
GITHUB_SCRIPT_URL = GITHUB_BASE_RAW + "/facial_rigging.py"
GITHUB_VERSION_URL = GITHUB_BASE_RAW + "/version.txt"
GITHUB_BANNER_URL = GITHUB_BASE_RAW + "/GameFaceRigTool.png"

TIMEOUT = 30


def _ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Maya-Facial-Rigging-Installer"})
    with urllib.request.urlopen(req, context=_ctx(), timeout=TIMEOUT) as resp:
        if resp.getcode() != 200:
            raise RuntimeError("HTTP " + str(resp.getcode()))
        return resp.read()


def _ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def _write_atomic(path, data):
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(data)
    shutil.move(tmp_path, path)


def _install_dir():
    base = cmds.internalVar(userScriptDir=True)
    return os.path.join(base, "Maya_Tool_Plus", "facial_rigging")


def _load_and_show(script_path):
    module_name = "maya_tool_plus_facial_rigging"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if not spec or not spec.loader:
        raise RuntimeError("Load spec failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    if hasattr(module, "showUI"):
        module.showUI()
        return True
    raise RuntimeError("showUI not found")


def install_or_update():
    target_dir = _install_dir()
    _ensure_dir(target_dir)

    local_script = os.path.join(target_dir, "facial_rigging.py")
    local_version = os.path.join(target_dir, "version.txt")
    local_banner = os.path.join(target_dir, "GameFaceRigTool.png")

    latest = None
    try:
        latest = _fetch(GITHUB_VERSION_URL).decode("utf-8").strip()
    except Exception:
        latest = None

    msg_lines = ["将安装到：", target_dir]
    if latest:
        msg_lines.append("远程版本：" + latest)
    msg = "\n".join(msg_lines)

    choice = cmds.confirmDialog(
        title="Facial Rigging 安装/更新",
        message=msg,
        button=["安装/更新", "取消"],
        defaultButton="安装/更新",
        cancelButton="取消",
        dismissString="取消",
    )
    if choice != "安装/更新":
        return False

    _write_atomic(local_script, _fetch(GITHUB_SCRIPT_URL))
    try:
        _write_atomic(local_version, _fetch(GITHUB_VERSION_URL))
    except Exception:
        pass
    try:
        _write_atomic(local_banner, _fetch(GITHUB_BANNER_URL))
    except Exception:
        pass

    if target_dir not in sys.path:
        sys.path.insert(0, target_dir)

    _load_and_show(local_script)
    cmds.inViewMessage(amg="Facial Rigging 已安装/更新", pos="midCenter", fade=True)
    return True


def _main():
    try:
        install_or_update()
    except urllib.error.URLError as e:
        cmds.confirmDialog(title="网络错误", message=str(e), button=["OK"])
    except Exception as e:
        cmds.confirmDialog(title="安装失败", message=str(e), button=["OK"])


_main()

