# なぜこのスクリプトが必要か
# -----------------------------------------------------------------------
# arduino-pico (earlephilhower) の Keyboard.h は内部で tusb-hid.h を
# インクルードしている。tusb-hid はフレームワークに同梱されているが、
# PlatformIO はそのインクルードパスを自動では追加しない。
#
# 以前は platformio.ini の build_flags に
#   -I${platformio.packages_dir}/framework-arduinopico/libraries/tusb-hid/src
# を直接書いていたが、以下の理由で環境によってパスが変わることがある:
#
#   1. platform = git URL (バージョン固定なし) のため、インストール時期によって
#      異なるコミットの framework-arduinopico が入る。
#   2. PlatformIO のバージョンや OS によってパッケージディレクトリの
#      命名規則が変わる場合がある（例: framework-arduinopico@x.y.z）。
#
# このスクリプトでは PlatformIO の API でフレームワークの実際のインストール先を
# 取得し、tusb-hid/src を CPPPATH に追加することで移植性の問題を解決する。
# -----------------------------------------------------------------------

import os
Import("env")

framework_dir = env.PioPlatform().get_package_dir("framework-arduinopico")
tusb_hid_path = os.path.join(framework_dir, "libraries", "tusb-hid", "src")
if os.path.exists(tusb_hid_path):
    env.Append(CPPPATH=[tusb_hid_path])
