# コントリビューションガイドライン

このドキュメントでは、Python template の保守運用に関する詳細を説明します。

## 依存パッケージの更新

依存パッケージの更新は以下の手順で行います：

1. `requirements.in`を手動で更新する
   - 直接依存しているパッケージのみを記述
   - バージョン指定は`~=`を使用（例：`flake8~=1.2.3`）
   - [PyPI](https://pypi.org/)で利用可能なパッケージのみを記述
   - `pip freeze > requirements.in`や`pip freeze >> requirements.in`による更新は禁止

2. ロックファイルを生成する
```bash
./scripts/generate_lockfile.sh
```

3. テストとLintを実行し、問題ないことを確認する
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

1. mainブランチをチェックアウト
```bash
git checkout main
```

2. リリース用ブランチの作成
```bash
git checkout -b release/vx.x.x
```

3. リモートリポジトリにプッシュ
```bash
git commit .
git push origin release/vx.x.x
```

4. プルリクエストの作成とCIの確認

5. リリースの作成
   - GitHubのリリースページから新規リリースを作成
   - タグを`vx.x.x`形式で設定
   - リリースノートを記入
   - "Publish release"をクリック

6. プルリクエストをmainブランチにマージ

## コントリビューションのガイドライン

### プルリクエストの作成

1. 新しい機能や修正用のブランチを作成
```bash
git checkout -b your-feature-name
```

2. 変更をコミット
- コミットメッセージは明確で簡潔に
- 関連するIssue番号を参照

3. プルリクエストの作成
- 変更内容の詳細な説明
- 関連するIssueのリンク
- テスト結果の確認

### コードレビューのガイドライン

1. コードの品質
- CIのチェックがパスした状態の維持
- 適切なドキュメンテーション
- テストカバレッジの維持

2. パフォーマンス
- 不要な依存関係の追加を避ける
- リソース使用量の最適化

3. セキュリティ
- 依存パッケージの脆弱性チェック
- 機密情報の取り扱い

## 問題の報告

1. Issueの作成
- 問題の詳細な説明
- 再現手順
- 期待される動作
- 実際の動作
- 環境情報

2. バグ修正
- 最小限の再現コード
- 修正案の提案

## メンテナンス

### 定期的なメンテナンスタスク

1. 依存パッケージの更新
- セキュリティパッチの適用
- 互換性の確認
- Pythonのバージョンアップ

2. ドキュメントの更新
- READMEの最新化

3. テストの更新
- 既存テストの見直し
