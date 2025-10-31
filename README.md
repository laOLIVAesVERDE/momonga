# 記事一覧アプリ

React + TypeScript + Material-UIを使用した記事一覧と詳細画面を表示するアプリケーションです。

## 機能

- 記事一覧の表示
- 記事詳細画面の表示
- レスポンシブデザイン
- Material-UIによる美しいUI

## 技術スタック

- React 18
- TypeScript
- Material-UI (MUI)
- Vite

## セットアップ

1. 依存関係をインストール:
```bash
npm install
```

2. 開発サーバーを起動:
```bash
npm run dev
```

3. ブラウザで `http://localhost:3000` にアクセス

## ビルド

```bash
npm run build
```

## プロジェクト構造

```
src/
├── components/
│   ├── ArticleList.tsx      # 記事一覧コンポーネント
│   └── ArticleDetail.tsx   # 記事詳細コンポーネント
├── types/
│   └── Article.ts          # 型定義
├── App.tsx                 # メインアプリケーション
└── main.tsx               # エントリーポイント
```

## 記事データ

記事データは `articles/` フォルダ内のJSONファイルから読み込まれます。
現在は `article_001.json` と `article_002.json` が含まれています。

