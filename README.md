# Kurotori Avatar Exporter

[English Version](README_en.md)

## 概要

Kurotori Avatar Exporter は、Blenderからアバター（キャラクターモデル）をFBX形式で効率的にエクスポートするためのアドオンです。特定のワークフロー（kurotori workflow）向けに設計されており、複数のエクスポート設定（ジョブ）を管理し、バッチ処理のようにエクスポートを実行できます。

Blender 4.2.0 以降が必要です。

## 主な機能

*   **エクスポートジョブの管理:**
    *   複数のエクスポート設定（ジョブ）を追加、削除、名前変更できます。
    *   ジョブごとに出力先ディレクトリを指定できます。
*   **エクスポート対象の設定:**
    *   基準となるアーマチュアオブジェクトを指定します。
    *   エクスポートに含めるメッシュオブジェクトを複数選択できます。
    *   エクスポートに含めるボーンを選択してリスト化できます（指定したボーンのみ `use_deform=True` としてエクスポートされます）。
*   **エクスポートオプション:**
    *   エクスポート時にシェイプキーの値をすべて0にリセットするオプションがあります。
*   **FBXエクスポート実行:**
    *   設定に基づいてFBXファイルをエクスポートします。
    *   以下のオプションが自動的に適用されます:
        *   表示されているオブジェクトのみエクスポート
        *   オブジェクトタイプ: アーマチュア、メッシュ
        *   スケール適用: FBX\_SCALE\_ALL
        *   デフォームボーンのみ
        *   リーフボーンを追加しない
        *   アニメーションをエクスポートしない

## インストール方法

1.  Blender を開き、`編集` > `プリファレンス` > `アドオン` に移動します。
2.  `拡張機能リポジトリ` (Get Extensions) をクリックし、`リポジトリ` (Repositories) タブを開きます。
3.  `[+]` ボタンをクリックし、`リモートリポジトリを追加` (Add Remote Repository) を選択します。
4.  URL として以下の値を貼り付けます:
    ```
    https://kurotori4423.github.io/AvatarExporter/index.json
    ```
5.  `OK` をクリックしてリポジトリを追加します。
6.  追加されたリポジトリを選択し、`拡張機能を更新` (Update Extensions) をクリックします (初回は不要な場合があります)。
7.  `コミュニティ` (Community) タブなどで「Kurotori Avatar Exporter」を見つけ、`インストール` (Install) ボタンをクリックします。
8.  インストール後、アドオン名の左側にあるチェックボックスを有効にします。

## 使用方法

1.  **パネルの表示:** 3Dビューポートのサイドバー（Nキー）を開き、「Avatar Exporter」タブを選択します。
2.  **ジョブの追加:** `Add Job` ボタンをクリックして新しいエクスポートジョブを作成します。
3.  **ジョブ設定:**
    *   ジョブ名の隣にあるテキストボックスでジョブ名を変更できます。
    *   `Output Dir`: FBXファイルの出力先フォルダを指定します。ファイル名はジョブ名に基づいて自動生成されます (`ジョブ名.fbx`)。
    *   `Reset ShapeKey`: チェックを入れると、エクスポート時にメッシュの全シェイプキーの値が0になります。
    *   `Armature`: エクスポートの基準となるアーマチュアオブジェクトを選択します。
    *   **Include Bone List:**
        *   `Armature` を設定すると表示されます。
        *   アーマチュアをポーズモードまたは編集モードで選択し、エクスポートに含めたいボーンを選択した状態で `Set Active Bone` ボタンをクリックします。リストに選択したボーンが追加されます。
        *   `Clear List` ボタンでリストを空にします。
        *   リストに含まれるボーンのみがデフォームボーンとしてエクスポートされます。
    *   **Export Mesh List:**
        *   エクスポートしたいメッシュオブジェクトを3Dビューで選択し、`Set Export Mesh` ボタンをクリックします。リストに選択したメッシュが追加されます。
4.  **エクスポート実行:**
    *   設定が完了したら、ジョブ名の右側にある `Export` (エクスポートアイコン) ボタンをクリックします。
    *   指定した出力先に `ジョブ名.fbx` という名前でファイルがエクスポートされます。

## ライセンス

MIT License

## 作者

kurotori4423@gmail.com
