# コントリビューションガイドライン

このドキュメントでは、Python template の保守運用に関する詳細を説明します。

## 依存パッケージの更新

### 手動での依存パッケージ更新

手動で依存パッケージを更新する場合は、以下の手順で行います：

1. `requirements.in`を手動で更新します。
   - 直接依存しているパッケージのみを記述します。
   - バージョン指定は`~=`を使用します（例：`flake8~=1.2.3`）。
   - [PyPI](https://pypi.org/)で利用可能なパッケージのみを記述します。
   - `pip freeze > requirements.in`や`pip freeze >> requirements.in`による更新は禁止します。

2. ロックファイルを生成します。
```bash
./scripts/generate_lockfile.sh
```

3. テストとLintを実行し、問題ないことを確認します。
```bash
# テスト
python -m unittest

# Lint
python -m black --check .
python -m isort -c .
python -m pylint src/* tests/* . --recursive=y --enable-all-extensions
python -m flake8 . --show-source --statistics
python -m mypy .
```

### Dependabot による自動更新

このプロジェクトでは、Dependabot が月次で依存パッケージの更新PRを自動作成します。

#### 操作手順

##### 1. 事前確認

dependabotのPRを処理する前に、GitHub UI上で以下を確認：

1. **dependabot PRページ**での確認:
   - **CI結果**: Actions タブで全てのテストが通過していることを確認
   - **Files changed**: 変更内容が依存関係のみであることを確認
   - **requirements.txt**: ロックファイルが適切に更新されていることを確認

2. **更新内容の分類**:
   - PRのタイトルと説明から更新種別を判定
   - セキュリティ関連の記載があるかチェック
   - メジャーバージョンアップが含まれているかチェック

##### 2. dependabotのPRの振り向け先変更

1. **dependabotのPRページ**に移動
2. **"Edit"ボタン**をクリック（PRタイトルの右側）
3. **Base branch**を `main` から `release/v<new-version>` に変更
4. **"Update pull request"**をクリック

##### 3. dependabotのPRをリリースブランチにマージ

1. **CIの完了**を確認（すべてのチェックが緑色）
2. **"Squash and merge"**を選択
3. **コミットメッセージ**を確認・編集：
   ```
   deps: bump <package-name> from <old-version> to <new-version> (#<PR-number>)
   
   - Security fix (該当する場合)
   - Breaking change (該当する場合)
   ```
4. **"Confirm squash and merge"**をクリック

**複数PRをまとめる場合（通常更新・破壊的変更）**

同じリリースブランチに対して、複数のdependabot PRを繰り返し実行：

1. 2つ目のdependabot PRの**Base branch**を同じ `release/v<new-version>` に変更
2. 上記マージ手順を繰り返し実行
3. 必要な数だけ繰り返す

##### 4. リリース手順の実行

dependabotのPRをリリースブランチにマージした後は、「[リリース手順](#リリース手順)」セクションに従って実行してください。

#### 機能リリースとの分離（推奨）

**基本原則**: dependabotによる依存関係更新のリリースと、機能追加・修正のリリースは原則として分離することを強く推奨します。

**分離する理由**:

1. **影響範囲の明確化**: 
   - 問題発生時に原因を特定しやすい
   - 依存関係の問題か機能の問題かを切り分けやすい

2. **ロールバックの容易性**: 
   - 問題のある変更のみを素早くロールバック可能
   - 機能と依存関係を独立して管理

3. **リリースノートの明確性**: 
   - ユーザーにとって何が変更されたかが明確
   - 機能変更と依存関係更新を区別して理解可能

4. **リスク管理**: 
   - 異なる種類の変更を混在させないことでリスクを軽減
   - テストの焦点を明確化

## リリース手順

1. mainブランチをチェックアウトし、コミットしていない変更がない状態にします。
```bash
git checkout main
```

2. リリース用の新しいブランチを作成します。`x.x.x`をリリースしたいバージョン番号に置き換えます。
```bash
git checkout -b release/vx.x.x
```

3. 新しいブランチをリモートリポジトリにプッシュします。
```bash
git push origin release/vx.x.x
```

4. `.github/scripts/currentVersion.js` のバージョンを更新し、コミットします。
```bash
# ファイルを編集してバージョンを更新
git add .github/scripts/currentVersion.js
git commit -m "chore: bump version to vx.x.x"
git push origin release/vx.x.x
```

5. プルリクエストを作成し、すべてのCIが通ることを確認します。

6. 新しいリリースを作成します。

https://github.com/besna-institute/python_template/releases/new から作成します。

以下のように設定し、"Generate release notes"を押します。

![スクリーンショット 2024-04-22 194831](https://github.com/besna-institute/python_template/assets/13166203/77fccdea-6e67-4a44-94bf-d2e829b9c3dd)

リリースノートを記入したら、"Publish release"を押します。

7. プルリクエストを main ブランチにマージします。

## コントリビューションのガイドライン

### プルリクエストの作成

1. 新しい機能や修正用のブランチを作成します。
```bash
git checkout -b your-feature-name
```

2. 変更をコミットします。
- コミットメッセージは明確で簡潔にします。
- 関連するIssue番号を参照します。

3. プルリクエストを作成します。
- 変更内容の詳細な説明を記載します。
- 関連するIssueのリンクを追加します。
- テスト結果の確認を行います。

### コードレビューのガイドライン

1. コードの品質
- CIのチェックがパスした状態を維持します。
- 適切なドキュメンテーションを記載します。
- テストカバレッジを維持します。

2. パフォーマンス
- 不要な依存関係の追加を避けます。
- リソース使用量を最適化します。

3. セキュリティ
- 依存パッケージの脆弱性チェックを行います。
- 機密情報の取り扱いに注意します。

## 問題の報告

1. Issueの作成
- 問題の詳細な説明を記載します。
- 再現手順を明記します。
- 期待される動作を説明します。
- 実際の動作を説明します。
- 環境情報を記載します。

2. バグ修正
- 最小限の再現コードを提供します。
- 修正案を提案します。

## メンテナンス

### 定期的なメンテナンスタスク

1. 依存パッケージの更新
- セキュリティパッチを適用します。
- 互換性を確認します。
- Pythonのバージョンアップを定期的に行います。

2. ドキュメントの更新
- READMEを最新の状態に保ちます。

3. テストの更新
- 既存テストを定期的に見直します。
