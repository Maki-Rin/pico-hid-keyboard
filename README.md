# pico-hid-keyboard

Raspberry Pi Pico (RP2040) を **USB HID キーボード**として動かす PlatformIO プロジェクトです。
ボタンを押すと、設定した文字列や特殊キーを PC に送信します。

---

## 必要なもの

### ハードウェア

| 品名 | 個数 | 備考 |
|------|------|------|
| Raspberry Pi Pico (RP2040) | 1 | Pico W 不可（USB HID 非対応） |
| USB Micro-B ケーブル | 1 | データ転送対応のもの |
| タクトスイッチ | 3 | 増減可能 |
| ジャンパーワイヤー | 適量 | |
| ブレッドボード | 1 | オプション、直接ハンダでも可 |

### ソフトウェア

- [PlatformIO](https://platformio.org/) (CLI または VSCode 拡張)

---

## セットアップ手順

### 1. PlatformIO のインストール

**VSCode を使う場合（推奨）**

1. [VSCode](https://code.visualstudio.com/) をインストール
2. 拡張機能タブで `PlatformIO IDE` を検索してインストール
3. VSCode を再起動

**CLI を使う場合**

```bash
pip install platformio
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/Maki-Rin/pico-hid-keyboard.git
cd pico-hid-keyboard
```

VSCode の場合は `File > Open Folder` でクローンしたフォルダを開く。

### 3. ビルド

初回ビルド時にプラットフォームと依存ライブラリが自動ダウンロードされます（数分かかります）。

```bash
pio run
```

VSCode の場合はサイドバーの PlatformIO アイコン → **Build** ボタン。

### 4. Pico を BOOTSEL モードで接続

1. Pico の **BOOTSEL ボタンを押したまま** USB を PC に挿す
2. **RPI-RP2** というドライブがマウントされたことを確認
3. BOOTSEL ボタンを離す

> **BOOTSEL ボタンの場所**
> Pico 基板の表面、USB コネクタの反対側にある小さなボタンです。

### 5. 書き込み

```bash
pio run --target upload
```

VSCode の場合は PlatformIO サイドバー → **Upload** ボタン。

書き込みが完了すると Pico が自動再起動し、HID キーボードとして動作します。

---

## 回路配線

### 配線図

```
Raspberry Pi Pico
                    ┌─────────────────┐
               GP3 ─┤  5              │
                    │                 │
               GP5 ─┤  7              │
                    │                 │
               GP7 ─┤ 10              │
                    │                 │
              GND  ─┤ 3 (または 38)   │
                    └─────────────────┘

各ボタンの接続:
  GPIO ピン ──┤ SW ├── GND
```

| GPIO | 物理ピン番号 | 役割 |
|------|------------|------|
| GP3  | 5          | ボタン 1 |
| GP5  | 7          | ボタン 2 |
| GP7  | 10         | ボタン 3 |

> `INPUT_PULLUP` を使用しているため、外部プルアップ抵抗は不要です。
> ボタンの一方を GPIO ピンに、もう一方を GND に接続するだけです。

### Pico ピン配置（参考）

```
             USB
        ┌────┴────┐
  GP0  1│         │40 VBUS
  GP1  2│         │39 VSYS
  GND  3│         │38 GND
  GP2  4│         │37 3V3_EN
  GP3  5│  RP2040 │36 3V3
  GP4  6│         │35 ADC_VREF
  GP5  7│         │34 GP28
  GND  8│         │33 GND
  GP6  9│         │32 GP27
  GP7 10│         │31 GP26
        └─────────┘
```

---

## カスタマイズ

`src/main.cpp` の上部にある設定箇所を変更します。

### ボタン数・ピンの変更

```cpp
// ボタンを接続した GPIO 番号（何個でも増減可能）
const uint8_t BUTTON_PINS[] = {3, 5, 7};
```

例：5 個のボタンを GP2, GP3, GP4, GP5, GP6 に接続する場合

```cpp
const uint8_t BUTTON_PINS[] = {2, 3, 4, 5, 6};
```

### マクロ文字列の変更

```cpp
const char *MACROS[] = {
    "Hello, World!\n",  // ボタン 1 を押すと入力される文字列
    "macro2\n",         // ボタン 2
    "macro3\n",         // ボタン 3
};
```

- `\n` は Enter キーを表します
- `BUTTON_PINS` と **同じ個数** にしてください

### 特殊キーの送信

文字列ではなくショートカットキーを送る場合は `Keyboard.press()` を使います。

```cpp
// Ctrl+C の例
Keyboard.press(KEY_LEFT_CTRL);
Keyboard.press('c');
delay(100);
Keyboard.releaseAll();
```

```cpp
// Win キー + D（デスクトップ表示）の例
Keyboard.press(KEY_LEFT_GUI);
Keyboard.press('d');
delay(100);
Keyboard.releaseAll();
```

**主な特殊キー定数**

| 定数 | キー |
|------|------|
| `KEY_LEFT_CTRL` | Left Ctrl |
| `KEY_RIGHT_CTRL` | Right Ctrl |
| `KEY_LEFT_SHIFT` | Left Shift |
| `KEY_LEFT_ALT` | Left Alt |
| `KEY_LEFT_GUI` | Left Win / Cmd |
| `KEY_RETURN` | Enter |
| `KEY_BACKSPACE` | Backspace |
| `KEY_DELETE` | Delete |
| `KEY_TAB` | Tab |
| `KEY_ESC` | Escape |
| `KEY_CAPS_LOCK` | Caps Lock |
| `KEY_F1` 〜 `KEY_F24` | F キー |
| `KEY_UP_ARROW` | ↑ |
| `KEY_DOWN_ARROW` | ↓ |
| `KEY_LEFT_ARROW` | ← |
| `KEY_RIGHT_ARROW` | → |
| `KEY_HOME` | Home |
| `KEY_END` | End |
| `KEY_PAGE_UP` | Page Up |
| `KEY_PAGE_DOWN` | Page Down |
| `KEY_INSERT` | Insert |
| `KEY_PRINT_SCREEN` | Print Screen |

---

## トラブルシューティング

### ビルドが失敗する

- `platformio.ini` に `board_build.core = earlephilhower` が記載されているか確認
- プラットフォームを最新化してみる：
  ```bash
  pio pkg update
  ```
- キャッシュをクリアして再ビルド：
  ```bash
  pio run --target clean
  pio run
  ```

### RPI-RP2 ドライブが表示されない（BOOTSEL モードに入れない）

- BOOTSEL ボタンを**押したまま** USB を挿しているか確認
- USB ケーブルが充電専用ではなくデータ転送対応か確認（充電専用は NG）
- 別の USB ポートや別のケーブルを試す

### 書き込みに失敗する（picotool エラー）

macOS で `picotool` が見つからない場合：

```bash
brew install picotool
```

Linux で権限エラーが出る場合：

```bash
sudo usermod -a -G dialout $USER
# ログアウト・ログインして反映させる
```

### PC にキーボードとして認識されない

- 書き込み後に Pico が再起動しているか確認（LED が点灯すれば動作中）
- USB ケーブルを抜き差しして再接続
- デバイスマネージャー（Windows）または `system_profiler SPUSBDataType`（macOS）でデバイス一覧を確認

### キーが連打される・チャタリングが起きる

`src/main.cpp` の `delay(10)` の値を増やす：

```cpp
delay(50);  // 10 → 50 など
```

または、ソフトウェアデバウンス処理を追加する。

---

## 参考リンク

- [earlephilhower/arduino-pico](https://github.com/earlephilhower/arduino-pico) — 使用している Arduino コア
- [maxgerhardt/platform-raspberrypi](https://github.com/maxgerhardt/platform-raspberrypi) — PlatformIO 用プラットフォーム
- [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — ピン配置の詳細
- [Arduino Keyboard Reference](https://www.arduino.cc/reference/en/language/functions/usb/keyboard/) — Keyboard ライブラリのリファレンス

---

## ライセンス

MIT License
