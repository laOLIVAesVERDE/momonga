#!/usr/bin/env python3
"""
記事本文とコメントをマージするスクリプト

articles/output/*.json と comments_scraper/output/*.json を連結して
プロジェクトルートの articles/ フォルダに保存します
"""

import json
import os
import glob
import argparse
from pathlib import Path


def merge_article_with_comments(
    articles_dir: str = "articles/output",
    comments_dir: str = "comments_scraper/output",
    output_dir: str = "../articles",
    category: str = "0026"
):
    """
    記事本文とコメントをマージ
    
    Args:
        articles_dir: 記事本文JSONディレクトリ
        comments_dir: コメントJSONディレクトリ
        output_dir: 出力先ディレクトリ（プロジェクトルートのarticles）
        category: カテゴリID（デフォルト: 0026）
    """
    # カテゴリごとのディレクトリパス
    articles_category_dir = os.path.join(articles_dir, category)
    comments_category_dir = os.path.join(comments_dir, category)
    
    # 出力ディレクトリを作成（カテゴリごとにフォルダを分ける）
    category_output_dir = os.path.join(output_dir, category)
    os.makedirs(category_output_dir, exist_ok=True)
    
    # 記事本文のJSONファイルを取得
    article_files = glob.glob(os.path.join(articles_category_dir, f"{category}_*.json"))
    article_files.sort()
    
    success_count = 0
    error_count = 0
    
    print("=" * 60)
    print("記事本文とコメントのマージを開始します")
    print(f"カテゴリ: {category}")
    print(f"記事本文: {articles_category_dir}")
    print(f"コメント: {comments_category_dir}")
    print(f"出力先: {category_output_dir}")
    print("=" * 60)
    print()
    
    for article_file in article_files:
        try:
            # ファイル名から記事IDを取得（例: 0026_001.json -> 001）
            filename = os.path.basename(article_file)
            # {category}_001.json -> 001
            article_num = filename.replace(f"{category}_", "").replace(".json", "")
            
            print(f"処理中: article_{article_num}.json")
            
            # 記事本文を読み込み
            with open(article_file, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
            
            # 対応するコメントファイルを探す
            comment_file = os.path.join(comments_category_dir, f"{category}_{article_num}.json")
            
            # コメントを読み込み（ファイルがない場合は空配列）
            if os.path.exists(comment_file):
                with open(comment_file, 'r', encoding='utf-8') as f:
                    comments_data = json.load(f)
                print(f"  ✅ コメント: {len(comments_data)}件")
            else:
                comments_data = []
                print(f"  ⚠️  コメントファイルなし - 空配列を使用")
            
            # マージ
            merged_data = {
                "title": article_data.get("title", ""),
                "date": article_data.get("date", ""),
                "url": article_data.get("url", ""),
                "content": article_data.get("content", ""),
                "comments": comments_data
            }
            
            # 出力ファイル名
            output_file = os.path.join(category_output_dir, f"article_{article_num}.json")
            
            # 保存
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=4)
            
            print(f"  📄 保存: {output_file}")
            print(f"     タイトル: {article_data.get('title', '')[:50]}...")
            print(f"     本文: {len(article_data.get('content', ''))}文字")
            print()
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            print()
            error_count += 1
    
    # 結果サマリー
    print("=" * 60)
    print("マージが完了しました")
    print("=" * 60)
    print(f"カテゴリ: {category}")
    print(f"✅ 成功: {success_count}件")
    print(f"❌ エラー: {error_count}件")
    print(f"📁 出力先: {category_output_dir}/")
    print("=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='記事本文とコメントをマージ'
    )
    parser.add_argument(
        '--articles-dir',
        default='articles/output',
        help='記事本文JSONディレクトリ（デフォルト: articles/output）'
    )
    parser.add_argument(
        '--comments-dir',
        default='comments_scraper/output',
        help='コメントJSONディレクトリ（デフォルト: comments_scraper/output）'
    )
    parser.add_argument(
        '--output-dir',
        default='../articles',
        help='出力先ディレクトリ（デフォルト: ../articles）'
    )
    parser.add_argument(
        '--category',
        default='0026',
        help='カテゴリID（デフォルト: 0026）'
    )
    
    args = parser.parse_args()
    
    merge_article_with_comments(
        articles_dir=args.articles_dir,
        comments_dir=args.comments_dir,
        output_dir=args.output_dir,
        category=args.category
    )
