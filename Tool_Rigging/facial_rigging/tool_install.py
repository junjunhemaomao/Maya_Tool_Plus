# -*- coding: utf-8 -*-

from maya import cmds
from maya import mel
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
GITHUB_ICON_URL = GITHUB_BASE_RAW + "/facial_rigging.png"

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

def _copy_atomic(src, dst):
    tmp_path = dst + ".tmp"
    shutil.copyfile(src, tmp_path)
    shutil.move(tmp_path, dst)


def _install_dir():
    base = cmds.internalVar(userScriptDir=True)
    return os.path.join(base, "Maya_Tool_Plus", "facial_rigging")

def _icons_dir():
    try:
        d = cmds.internalVar(userIconDir=True)
        if not d:
            raise RuntimeError("empty userIconDir")
        return d
    except Exception:
        pref = cmds.internalVar(userPrefDir=True) or ""
        if not pref:
            # 最后兜底：使用用户脚本目录下的 icons
            base = cmds.internalVar(userScriptDir=True) or ""
            return os.path.join(base, "icons")
        return os.path.join(pref, "icons")


def _normalize_path(p):
    return (p or "").replace("\\", "/")


def _install_icon(local_banner):
    if not local_banner or not os.path.exists(local_banner):
        return None
    icon_dir = _icons_dir()
    _ensure_dir(icon_dir)
    dst = os.path.join(icon_dir, os.path.basename(local_banner))
    try:
        shutil.copy2(local_banner, dst)
    except Exception:
        dst = local_banner
    return dst


def _shelf_top():
    try:
        return mel.eval("$tmp=$gShelfTopLevel")
    except Exception:
        try:
            return mel.eval("global string $gShelfTopLevel; $gShelfTopLevel")
        except Exception:
            return None


def _ensure_shelf_tab(label):
    top = _shelf_top()
    if not top or not cmds.tabLayout(top, exists=True):
        return None
    existing = cmds.tabLayout(top, q=True, ca=True) or []
    if label in existing and cmds.shelfLayout(label, exists=True):
        return label
    try:
        mel.eval('addNewShelfTab "{0}"'.format(label))
    except Exception:
        pass
    selected = cmds.tabLayout(top, q=True, st=True)
    if selected and cmds.shelfLayout(selected, exists=True):
        return selected
    return None


def _ensure_shelf_button(shelf, icon_path):
    if not shelf or not cmds.shelfLayout(shelf, exists=True):
        return None
    children = cmds.shelfLayout(shelf, q=True, ca=True) or []
    for c in children:
        try:
            if cmds.shelfButton(c, q=True, annotation=True) == "Maya_Tool_Plus Facial Rigging":
                if icon_path:
                    try:
                        cmds.shelfButton(c, e=True, image1=_normalize_path(icon_path))
                    except Exception:
                        pass
                return c
        except Exception:
            pass
    cmd = (
        "import os,sys,importlib.util;"
        "from maya import cmds;"
        "p=os.path.join(cmds.internalVar(userScriptDir=True),'Maya_Tool_Plus','facial_rigging','facial_rigging.py');"
        "name='maya_tool_plus_facial_rigging';"
        "spec=importlib.util.spec_from_file_location(name,p);"
        "mod=importlib.util.module_from_spec(spec);"
        "sys.modules[name]=mod;"
        "spec.loader.exec_module(mod);"
        "mod.showUI()"
    )
    btn = cmds.shelfButton(
        parent=shelf,
        label="FacialRigging",
        annotation="Maya_Tool_Plus Facial Rigging",
        image1=_normalize_path(icon_path) if icon_path else "commandButton.png",
        command=cmd,
        sourceType="python",
    )
    try:
        mel.eval("saveAllShelves($gShelfTopLevel)")
    except Exception:
        pass
    return btn



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
    local_icon = os.path.join(target_dir, "facial_rigging.png")

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

    try:
        _write_atomic(local_script, _fetch(GITHUB_SCRIPT_URL))
    except Exception:
        repo_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "facial_rigging.py")
        if os.path.exists(repo_script):
            _copy_atomic(repo_script, local_script)
        else:
            raise
    try:
        _write_atomic(local_version, _fetch(GITHUB_VERSION_URL))
    except Exception:
        repo_version = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt")
        if os.path.exists(repo_version):
            _copy_atomic(repo_version, local_version)
    try:
        _write_atomic(local_banner, _fetch(GITHUB_BANNER_URL))
    except Exception:
        repo_banner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GameFaceRigTool.png")
        if os.path.exists(repo_banner):
            _copy_atomic(repo_banner, local_banner)
    try:
        _write_atomic(local_icon, _fetch(GITHUB_ICON_URL))
    except Exception:
        repo_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "facial_rigging.png")
        if os.path.exists(repo_icon):
            _copy_atomic(repo_icon, local_icon)

    if target_dir not in sys.path:
        sys.path.insert(0, target_dir)

    icon_path = _install_icon(local_icon)
    shelf = _ensure_shelf_tab("MayaToolPlus")
    if shelf:
        _ensure_shelf_button(shelf, icon_path)

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


def onMayaDroppedPythonFile(*_args):
    _main()


if __name__ == "__main__":
    _main()
