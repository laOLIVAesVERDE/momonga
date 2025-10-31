#!/usr/bin/env python3
"""
NHK みんなでプラス コメントスクレイパー
URLを引数にしてコメントをJSON形式で取得します
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs


class NHKCommentScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def parse_age_gender(self, text: str) -> tuple[Optional[str], Optional[str]]:
        """年齢と性別を解析"""
        age = None
        gender = None
        
        if text:
            # 年齢の抽出（例: "20代", "30代", "19歳以下", "40代"など）
            age_match = re.search(r'(\d+代|19歳以下|70歳以上)', text)
            if age_match:
                age = age_match.group(1)
            
            # 性別の抽出
            if '男性' in text:
                gender = '男性'
            elif '女性' in text:
                gender = '女性'
        
        return age, gender

    def parse_comment(self, comment_element) -> Optional[Dict]:
        """コメント要素（<dl>タグ）を解析してディクショナリを返す"""
        try:
            # コメントタイプ（感想、体験談、悩みなど）
            label_elem = comment_element.find('div', class_='c-comment__label')
            comment_type = label_elem.get_text(strip=True) if label_elem else None
            
            # 名前
            name_elem = comment_element.find('div', class_='c-comment__name')
            name = name_elem.get_text(strip=True) if name_elem else None
            
            # 年齢と性別
            meta_elem = comment_element.find('div', class_='c-comment__meta')
            age = None
            gender = None
            if meta_elem:
                age, gender = self.parse_age_gender(meta_elem.get_text(strip=True))
            
            # 日付
            date_elem = comment_element.find('div', class_='c-comment__date')
            date = date_elem.get_text(strip=True) if date_elem else None
            
            # コメント本文
            body_elem = comment_element.find('dd', class_='c-comment__body')
            content = body_elem.get_text(strip=True) if body_elem else None
            
            if not name and not content:
                return None
            
            return {
                'type': comment_type,
                'name': name,
                'age': age,
                'gender': gender,
                'date': date,
                'content': content
            }
        except Exception as e:
            print(f"コメントの解析中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_page_comments(self, url: str) -> List[Dict]:
        """指定されたページのコメントを取得"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # コメントリストを取得（<dl class="c-comment">タグ）
            comment_elements = soup.find_all('dl', class_='c-comment')
            
            comments = []
            for comment_elem in comment_elements:
                comment_data = self.parse_comment(comment_elem)
                if comment_data:
                    comments.append(comment_data)
            
            return comments
        except Exception as e:
            print(f"ページの取得中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_total_comment_count(self, soup) -> int:
        """総コメント数を取得"""
        try:
            # 「みんなのコメント（318件）」のような見出しを探す
            headings = soup.find_all('h2')
            for heading in headings:
                text = heading.get_text()
                # 「みんなのコメント（XXX件）」のパターンをマッチ
                match = re.search(r'みんなのコメント[（(](\d+)件[)）]', text)
                if match:
                    return int(match.group(1))
            return 0
        except Exception as e:
            print(f"総コメント数の取得中にエラーが発生しました: {e}")
            return 0

    def get_pagination_urls(self, url: str) -> List[str]:
        """ページネーションのURLリストを取得"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 総コメント数を取得
            total_comments = self.get_total_comment_count(soup)
            
            if total_comments > 0:
                # 1ページあたり10件として総ページ数を計算
                comments_per_page = 10
                total_pages = (total_comments + comments_per_page - 1) // comments_per_page  # 切り上げ
                
                print(f"総コメント数: {total_comments}件")
                print(f"総ページ数: {total_pages}ページ")
                
                # 全ページのURLを生成
                urls = [url]  # 1ページ目
                
                # URLパターンを解析
                # index.html → index0002.html, index0003.html ...
                base_path = url.replace('index.html', '')
                
                for page_num in range(2, total_pages + 1):
                    page_url = f"{base_path}index{page_num:04d}.html"
                    urls.append(page_url)
                
                return urls
            else:
                # 総コメント数が取得できない場合は、従来の方法でページネーションを取得
                print("総コメント数が取得できませんでした。表示されているページのみ取得します。")
                
                pagination = None
                for nav in soup.find_all('nav'):
                    nav_links = nav.find_all('a')
                    if any(link.get_text(strip=True).isdigit() for link in nav_links):
                        pagination = nav
                        break
                
                if not pagination:
                    return [url]
                
                urls = set()
                urls.add(url)
                
                page_links = pagination.find_all('a')
                for link in page_links:
                    href = link.get('href')
                    link_text = link.get_text(strip=True)
                    if href and href not in ['#', ''] and (link_text.isdigit() or link_text == '次へ'):
                        full_url = urljoin(url, href)
                        urls.add(full_url)
                
                return sorted(list(urls))
            
        except Exception as e:
            print(f"ページネーションの取得中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return [url]

    def scrape_all_comments(self) -> List[Dict]:
        """全ページのコメントを取得"""
        print(f"コメントの取得を開始します: {self.base_url}")
        
        # ページネーションURLを取得
        page_urls = self.get_pagination_urls(self.base_url)
        print(f"取得対象ページ数: {len(page_urls)}ページ")
        
        all_comments = []
        
        for i, page_url in enumerate(page_urls, 1):
            print(f"ページ {i}/{len(page_urls)} を処理中...")
            comments = self.get_page_comments(page_url)
            all_comments.extend(comments)
            print(f"  {len(comments)} 件のコメントを取得")
            
            # サーバーへの負荷を軽減するため、各ページ取得後に少し待機
            # 最後のページの後は待機不要
            if i < len(page_urls):
                time.sleep(0.5)  # 0.5秒待機
        
        print(f"\n合計 {len(all_comments)} 件のコメントを取得しました")
        return all_comments


def main():
    parser = argparse.ArgumentParser(
        description='NHK みんなでプラス コメントスクレイパー'
    )
    parser.add_argument(
        'url',
        help='コメントページのURL'
    )
    parser.add_argument(
        '-o', '--output',
        default='comments.json',
        help='出力ファイル名 (デフォルト: comments.json)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='整形されたJSONを出力'
    )
    
    args = parser.parse_args()
    
    # スクレイパーを初期化
    scraper = NHKCommentScraper(args.url)
    
    # コメントを取得
    comments = scraper.scrape_all_comments()
    
    # JSONファイルに保存
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        else:
            json.dump(comments, f, ensure_ascii=False)
    
    print(f"\nコメントを {args.output} に保存しました")
    
    # 統計情報を表示
    if comments:
        print("\n=== 統計情報 ===")
        print(f"総コメント数: {len(comments)}")
        
        types = {}
        for comment in comments:
            comment_type = comment.get('type', '不明')
            types[comment_type] = types.get(comment_type, 0) + 1
        
        print("\nコメントタイプ別:")
        for ctype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ctype}: {count}件")


if __name__ == '__main__':
    main()
