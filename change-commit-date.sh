#!/bin/bash

# Git コミット日時を変更するスクリプト
# 使用方法: ./change-commit-date.sh "YYYY-MM-DD HH:MM"
# 例: ./change-commit-date.sh "2025-08-03 20:29"

if [ $# -eq 0 ]; then
    echo "使用方法: $0 \"YYYY-MM-DD HH:MM\""
    echo "例: $0 \"2025-08-03 20:29\""
    exit 1
fi

DATE_STRING="$1"
# 入力された日時をISO形式に変換（JST +0900）
ISO_DATE="${DATE_STRING}:00+0900"

echo "コミット日時を ${DATE_STRING} (JST) に変更します..."

# AuthorDateとCommitDateの両方を変更
GIT_COMMITTER_DATE="$ISO_DATE" git commit --amend --date="$ISO_DATE" --no-edit

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ コミット日時の変更が完了しました"
    echo ""
    git log -1 --pretty=fuller
else
    echo "エラー: コミット日時の変更に失敗しました"
    exit 1
fi

