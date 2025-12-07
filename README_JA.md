[![README in English](https://img.shields.io/badge/English-d9d9d9)](./README.md)
[![日本語版 README](https://img.shields.io/badge/日本語-d9d9d9)](./README_JA.md)

<p style="display: inline">
  <img src="https://img.shields.io/badge/-Ubuntu_22.04_LTS-555555.svg?style=flat&logo=ubuntu">  
  <img src="https://img.shields.io/badge/-Gazebo Fortress-orange.svg?style=flat&logo=gazebo&logoColor=white">
  <img src="https://img.shields.io/badge/-ROS2 Humble-%2322314E?style=flat&logo=ROS&logoColor=white">
  <img src="https://img.shields.io/badge/-Python 3.10-3776AB.svg?logo=python&style=flat&logoColor=white">
  <img src="https://img.shields.io/badge/License-Apache--2.0-60C060.svg?style=flat">
</p>

## 目次
1. [**Bot-Q TMSとは？**](#bot-q-tmsとは)
2. [**前提条件**](#前提条件)
3. [**インストール**](#インストール)
    1. [リポジトリのクローン](#リポジトリのクローン)
    2. [依存パッケージのインストール](#依存パッケージのインストール)
4. [**使い方**](#使い方)
    1. [ビルド & ソース](#ビルド--ソース)
    2. [シミュレーションの起動 (Gazebo)](#シミュレーションの起動-gazebo)
    3. [実機の起動](#実機の起動)
    4. [モデルの可視化](#モデルの可視化)
5. [**トピックとインターフェース**](#トピックとインターフェース)
6. [**ライセンス**](#ライセンス)

---

## Bot-Q TMSとは？
Bot-Q TMSは、ケーブルやフィラメントの引き出し・押し込みのため設計されたドッキングステーションです。3自由度のスプール/エクストルーダー機構を備えています。

このリポジトリでは、Gazebo (`ros_gz`) でのシミュレーションおよび `ros2_control` (Dynamixel) を介した実機制御に必要な ROS 2 パッケージを提供します。

## 前提条件
このリポジトリを使用するには、以下の環境を用意する必要があります。

|  Package  |         Version         |
| --------- | ----------------------- |
|   Ubuntu  | 22.04 (Jammy Jellyfish) |
|   Gazebo  | Fortress                |
|    ROS    | Humble Hawksbill        |
|   Python  | 3.10 <=                 |

## インストール

### リポジトリのクローン
まだ、ROS 2のワークスペースがない場合は作成します。
```bash
mkdir -p ~/bot_q_tms_ws/src
cd ~/bot_q_tms_ws/src
```

本パッケージをワークスペースにクローンします。
```bash
git clone https://github.com/sd-robotics/bot-q_tms.git
```

### 依存パッケージのインストール
必要な ROS 2 パッケージと依存関係をインストールします。

```bash
cd ~/bot_q_tms_ws/src/bot-q_tms
bash install.sh
```

## 使い方

### ビルド & ソース
パッケージのビルドとワークスペースのソースを行います。
```bash
cd ~/bot_q_tms_ws
colcon build --symlink-install
source install/setup.bash
```

### シミュレーションの起動 (Gazebo)
Gazeboシミュレーション環境でロボットとRVizによる可視化を起動するには、以下のコマンドを実行します。

```bash
ros2 launch bot_q_tms_bringup gz_minimal.launch.py
```

これにより、Gazeboの空のワールドにロボット（キャリア機構を含む）がスポーンし、必要なトピックがブリッジされます。

### 実機の起動
物理ロボット（Dynamixelハードウェアインターフェース）用のドライバを起動するには、以下のコマンドを実行します。

```bash
ros2 launch bot_q_tms_bringup real_minimal.launch.py
```

### モデルの可視化
物理シミュレーションを実行せずに、URDFモデルとジョイントの状態のみを可視化したい場合は、以下を実行します。

```bash
ros2 launch bot_q_tms_description display.launch.py use_gui:=True
```

## トピックとインターフェース

### センサ
シミュレーションおよび実機は、以下のセンサデータをパブリッシュします。

| センサ種類 | トピック名 | 概要 |
|---|---|---|
| **Joints** | `/bot_q_tms/joint_states` | ジョイントの現在位置と速度。 |

### 制御
このロボットは `ros2_control` を使用しています。

| コントローラ | タイプ | 概要 |
|---|---|---|
| `velocity_controller` | `JointGroupVelocityController` | スプール、ガイダー、エクストルーダーのギアを制御します。 |

## ライセンス
このリポジトリは Apache License 2.0 の下でライセンスされています。詳細は [LICENSE](./LICENSE) ファイルを参照してください。
