# コントリビューションガイドライン

このドキュメントでは、Python template の保守運用に関する詳細を説明します。

## 依存パッケージの更新

依存パッケージの更新は以下の手順で行います：

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
