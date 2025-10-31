#!/usr/bin/env python3
"""
NHK みんなでプラス 記事本文スクレイパー
記事のタイトル、日付、URL、本文を取得してJSON形式で保存します
"""

import requests
from bs4 import BeautifulSoup
import json
import argparse
from typing import Dict, Optional


class NHKArticleScraper:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape_article(self) -> Optional[Dict]:
        """記事データを取得"""
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # タイトルを取得
            title = self.get_title(soup)
            
            # 日付を取得
            date = self.get_date(soup)
            
            # 本文を取得
            content = self.get_content(soup)
            
            if not title or not content:
                print("記事データの取得に失敗しました")
                return None
            
            return {
                'title': title,
                'date': date,
                'url': self.url,
                'content': content
            }
            
        except Exception as e:
            print(f"記事の取得中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_title(self, soup) -> Optional[str]:
        """記事タイトルを取得"""
        try:
            # パターン1: article内のh1タグ
            article = soup.find('article')
            if article:
                h1 = article.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
                    if title:
                        return title
            
            # パターン2: main内のh1タグ
            main = soup.find('main')
            if main:
                h1 = main.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
                    if title:
                        return title
            
            # パターン3: 全体からh1タグ
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
                if title:
                    return title
            
            # フォールバック: titleタグから取得
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # " - NHK みんなでプラス"などのサフィックスを削除
                parts = title.split(' - ')
                if len(parts) > 0:
                    return parts[0].strip()
            
            return None
        except Exception as e:
            print(f"タイトルの取得中にエラー: {e}")
            return None

    def get_date(self, soup) -> Optional[str]:
        """公開日を取得"""
        try:
            # 日付を含む要素を探す
            # パターン1: time タグ
            time_tag = soup.find('time')
            if time_tag:
                return time_tag.get_text(strip=True)
            
            # パターン2: 日付っぽいテキストを探す（YYYY年M月D日形式）
            import re
            date_pattern = re.compile(r'\d{4}年\d{1,2}月\d{1,2}日')
            
            # article タグ内を探す
            article = soup.find('article')
            if article:
                date_match = date_pattern.search(article.get_text())
                if date_match:
                    return date_match.group(0)
            
            # main タグ内を探す
            main = soup.find('main')
            if main:
                # mainの最初の方に日付があることが多い
                first_section = main.find(['div', 'section', 'header'])
                if first_section:
                    date_match = date_pattern.search(first_section.get_text())
                    if date_match:
                        return date_match.group(0)
            
            return None
        except Exception as e:
            print(f"日付の取得中にエラー: {e}")
            return None

    def get_content(self, soup) -> Optional[str]:
        """記事本文を取得"""
        try:
            content_parts = []
            
            # main または article タグを探す
            main_content = soup.find('main') or soup.find('article')
            
            if not main_content:
                print("記事本文のコンテナが見つかりませんでした")
                return None
            
            # 見出しと段落を取得
            for element in main_content.find_all(['h2', 'h3', 'h4', 'p', 'blockquote']):
                # 不要な要素をスキップ
                # クラス名で判断
                element_class = element.get('class', [])
                if any(cls in element_class for cls in ['share', 'sns', 'related', 'tag']):
                    continue
                
                text = element.get_text(strip=True)
                
                # 空の要素やナビゲーション要素をスキップ
                if not text or text in ['INDEX', 'シェアする', 'もっと見る']:
                    continue
                
                # 見出しの場合
                if element.name in ['h2', 'h3', 'h4']:
                    content_parts.append(f"\n## {text}\n")
                # 引用の場合
                elif element.name == 'blockquote':
                    content_parts.append(f"\n{text}\n")
                # 段落の場合
                else:
                    content_parts.append(text)
            
            # 結合して返す
            content = '\n\n'.join(content_parts).strip()
            return content if content else None
            
        except Exception as e:
            print(f"本文の取得中にエラー: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    parser = argparse.ArgumentParser(
        description='NHK みんなでプラス 記事本文スクレイパー'
    )
    parser.add_argument(
        'url',
        help='記事ページのURL'
    )
    parser.add_argument(
        '-o', '--output',
        default='article.json',
        help='出力ファイル名 (デフォルト: article.json)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='整形されたJSONを出力'
    )
    
    args = parser.parse_args()
    
    print(f"記事の取得を開始します: {args.url}")
    print()
    
    # スクレイパーを初期化
    scraper = NHKArticleScraper(args.url)
    
    # 記事を取得
    article = scraper.scrape_article()
    
    if not article:
        print("記事の取得に失敗しました")
        return
    
    print("✅ 記事データを取得しました")
    print(f"  タイトル: {article['title']}")
    print(f"  日付: {article['date']}")
    print(f"  本文: {len(article['content'])}文字")
    print()
    
    # JSONファイルに保存
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(article, f, ensure_ascii=False, indent=4)
        else:
            json.dump(article, f, ensure_ascii=False)
    
    print(f"📄 記事を {args.output} に保存しました")


if __name__ == '__main__':
    main()
