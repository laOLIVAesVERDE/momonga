#!/usr/bin/env python3
"""
NHK コメントスクレイパーの使用例
プログラムから直接呼び出す場合の例
"""

from nhk_comment_scraper import NHKCommentScraper
import json


def example_basic_usage():
    """基本的な使用例"""
    url = "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html"
    
    # スクレイパーを初期化
    scraper = NHKCommentScraper(url)
    
    # コメントを取得
    comments = scraper.scrape_all_comments()
    
    # 結果を表示
    print(f"\n取得したコメント数: {len(comments)}")
    
    # 最初の3件を表示
    print("\n=== 最初の3件 ===")
    for i, comment in enumerate(comments[:3], 1):
        print(f"\n[{i}] {comment['name']} ({comment['age'] or '年齢不明'} {comment['gender'] or '性別不明'})")
        print(f"日付: {comment['date']}")
        print(f"タイプ: {comment['type']}")
        print(f"内容: {comment['content'][:100]}..." if len(comment['content']) > 100 else f"内容: {comment['content']}")
    
    # JSONファイルに保存
    with open('example_output.json', 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    
    print("\n\nexample_output.json に保存しました")


def example_filter_by_type():
    """コメントタイプでフィルタリングする例"""
    url = "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html"
    
    scraper = NHKCommentScraper(url)
    comments = scraper.scrape_all_comments()
    
    # 体験談のみを抽出
    testimonials = [c for c in comments if c['type'] == '体験談']
    
    print(f"\n体験談の件数: {len(testimonials)}")
    
    # 体験談を別ファイルに保存
    with open('testimonials.json', 'w', encoding='utf-8') as f:
        json.dump(testimonials, f, ensure_ascii=False, indent=2)
    
    print("testimonials.json に保存しました")


def example_gender_statistics():
    """性別統計を取得する例"""
    url = "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html"
    
    scraper = NHKCommentScraper(url)
    comments = scraper.scrape_all_comments()
    
    # 性別統計
    male_count = len([c for c in comments if c['gender'] == '男性'])
    female_count = len([c for c in comments if c['gender'] == '女性'])
    unknown_count = len([c for c in comments if c['gender'] is None])
    
    print(f"\n=== 性別統計 ===")
    print(f"男性: {male_count}件")
    print(f"女性: {female_count}件")
    print(f"不明: {unknown_count}件")
    
    # 年齢統計
    age_stats = {}
    for comment in comments:
        age = comment['age'] or '不明'
        age_stats[age] = age_stats.get(age, 0) + 1
    
    print(f"\n=== 年齢統計 ===")
    for age, count in sorted(age_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{age}: {count}件")


if __name__ == '__main__':
    print("=" * 60)
    print("例1: 基本的な使用方法")
    print("=" * 60)
    example_basic_usage()
    
    print("\n\n" + "=" * 60)
    print("例2: コメントタイプでフィルタリング")
    print("=" * 60)
    example_filter_by_type()
    
    print("\n\n" + "=" * 60)
    print("例3: 統計情報の取得")
    print("=" * 60)
    example_gender_statistics()
