#!/usr/bin/env python3
"""
NHK みんなでプラス コメント一括スクレイパー
複数の記事のコメントを一括で取得します
"""

import json
import os
import time
from nhk_comment_scraper import NHKCommentScraper


def scrape_article_range(start_id: int, end_id: int, output_dir: str = "output", base_category: str = "0026"):
    """
    指定された範囲の記事IDのコメントを取得
    
    Args:
        start_id: 開始記事ID（例: 1）
        end_id: 終了記事ID（例: 300）
        output_dir: 出力ディレクトリ
        base_category: カテゴリID（デフォルト: 0026）
    """
    # カテゴリごとのサブディレクトリを作成
    category_output_dir = os.path.join(output_dir, base_category)
    os.makedirs(category_output_dir, exist_ok=True)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    print(f"=" * 60)
    print(f"コメント一括取得を開始します")
    print(f"対象: {base_category}_{start_id:03d} から {base_category}_{end_id:03d}")
    print(f"カテゴリ: {base_category}")
    print(f"出力先: {category_output_dir}/")
    print(f"=" * 60)
    print()
    
    for article_id in range(start_id, end_id + 1):
        article_num = f"{article_id:03d}"
        topic_id = f"{base_category}_{article_num}"
        
        # URL生成
        url = f"https://www.nhk.or.jp/minplus/{base_category}/comments/{topic_id}/index.html"
        
        # 出力ファイル名
        output_file = os.path.join(category_output_dir, f"{topic_id}.json")
        
        print(f"[{article_id}/{end_id}] {topic_id} を処理中...")
        print(f"  URL: {url}")
        
        try:
            # スクレイパーを初期化
            scraper = NHKCommentScraper(url)
            
            # まず最初のページにアクセスして存在確認
            import requests
            response = scraper.session.get(url)
            
            if response.status_code == 404:
                print(f"  ⚠️  ページが見つかりません（404）- スキップします")
                skip_count += 1
                print()
                continue
            elif response.status_code != 200:
                print(f"  ⚠️  エラー（HTTP {response.status_code}）- スキップします")
                skip_count += 1
                print()
                continue
            
            # コメントを取得
            comments = scraper.scrape_all_comments()
            
            if len(comments) == 0:
                print(f"  ⚠️  コメントが0件 - スキップします")
                skip_count += 1
                print()
                continue
            
            # JSONファイルに保存
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=2)
            
            print(f"  ✅ 成功: {len(comments)}件のコメントを保存しました")
            print(f"  📄 保存先: {output_file}")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ エラーが発生しました: {e}")
            error_count += 1
        
        print()
        
        # サーバーへの負荷を軽減するため、少し待機
        if article_id < end_id:
            time.sleep(1)  # 1秒待機
    
    # 結果サマリー
    print()
    print("=" * 60)
    print("一括取得が完了しました")
    print("=" * 60)
    print(f"カテゴリ: {base_category}")
    print(f"✅ 成功: {success_count}件")
    print(f"⚠️  スキップ: {skip_count}件")
    print(f"❌ エラー: {error_count}件")
    print(f"📁 出力先: {category_output_dir}/")
    print("=" * 60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NHK みんなでプラス コメント一括スクレイパー'
    )
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='開始記事ID（デフォルト: 1）'
    )
    parser.add_argument(
        '--end',
        type=int,
        default=300,
        help='終了記事ID（デフォルト: 300）'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='出力ディレクトリ（デフォルト: output）'
    )
    parser.add_argument(
        '--category',
        default='0026',
        help='カテゴリID（デフォルト: 0026）'
    )
    
    args = parser.parse_args()
    
    scrape_article_range(
        start_id=args.start,
        end_id=args.end,
        output_dir=args.output_dir,
        base_category=args.category
    )
