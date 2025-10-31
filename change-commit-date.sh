#!/bin/bash

# Git コミット日時を変更するスクリプト
# 使用方法: 
#   ./change-commit-date.sh "YYYY-MM-DD HH:MM" [COMMIT_HASH]
# 例: 
#   ./change-commit-date.sh "2025-08-03 20:29"                    # 最新のコミット（HEAD）を変更
#   ./change-commit-date.sh "2025-08-03 20:29" f488473           # 指定したコミットを変更

set -e

if [ $# -eq 0 ]; then
    echo "使用方法: $0 \"YYYY-MM-DD HH:MM\" [COMMIT_HASH]"
    echo ""
    echo "引数:"
    echo "  YYYY-MM-DD HH:MM  変更したい日時（JST）"
    echo "  COMMIT_HASH        変更したいコミットハッシュ（省略時は最新のコミット）"
    echo ""
    echo "例:"
    echo "  $0 \"2025-08-03 20:29\""
    echo "  $0 \"2025-08-03 20:29\" f48847389d9b56f521547c91dc37a5da4016f6f6"
    exit 1
fi

DATE_STRING="$1"
COMMIT_HASH="${2:-HEAD}"

# コミットハッシュが存在するか確認
if ! git rev-parse --verify "$COMMIT_HASH" >/dev/null 2>&1; then
    echo "エラー: コミットハッシュ '$COMMIT_HASH' が見つかりません"
    exit 1
fi

# フルコミットハッシュを取得
FULL_COMMIT_HASH=$(git rev-parse "$COMMIT_HASH")
CURRENT_HEAD=$(git rev-parse HEAD)

# 入力された日時をISO形式に変換（JST +0900）
ISO_DATE="${DATE_STRING}:00+0900"

echo "コミット日時を ${DATE_STRING} (JST) に変更します..."
echo "対象コミット: $FULL_COMMIT_HASH"

# HEADのコミットを変更する場合
if [ "$FULL_COMMIT_HASH" = "$CURRENT_HEAD" ]; then
    echo "最新のコミット（HEAD）を変更します..."
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
else
    # 過去のコミットを変更する場合、interactive rebaseを使用
    echo "過去のコミットを変更するため、interactive rebaseを使用します..."
    
    # 対象コミットが現在のブランチに含まれているか確認
    if ! git merge-base --is-ancestor "$FULL_COMMIT_HASH" HEAD 2>/dev/null; then
        echo "エラー: 指定されたコミットは現在のブランチの履歴に含まれていません"
        exit 1
    fi
    
    # 対象コミットの親コミットを取得
    PARENT_COMMIT=$(git rev-parse "$FULL_COMMIT_HASH^" 2>/dev/null || echo "")
    if [ -z "$PARENT_COMMIT" ]; then
        echo "エラー: ルートコミットは変更できません"
        exit 1
    fi
    
    # 一時的なエディタスクリプトを作成（対象コミットをeditに変更）
    EDITOR_SCRIPT=$(mktemp)
    cat > "$EDITOR_SCRIPT" <<EOFSCRIPT
#!/bin/bash
# 対象のコミットハッシュの行をpickからeditに変更
FULL_HASH="$FULL_COMMIT_HASH"
# macOSとLinuxの両方に対応
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^pick \$FULL_HASH/edit \$FULL_HASH/" "\$1"
else
    sed -i "s/^pick \$FULL_HASH/edit \$FULL_HASH/" "\$1"
fi
EOFSCRIPT
    chmod +x "$EDITOR_SCRIPT"
    
    # 環境変数をエクスポート
    export GIT_SEQUENCE_EDITOR="$EDITOR_SCRIPT"
    export ISO_DATE
    
    # rebaseを開始（非対話的に）
    if git rebase -i "$PARENT_COMMIT" >/dev/null 2>&1; then
        # rebaseが自動的に進み、コミット編集モードに入る
        # 日時を変更してrebaseを続行
        GIT_COMMITTER_DATE="$ISO_DATE" git commit --amend --date="$ISO_DATE" --no-edit
        git rebase --continue >/dev/null 2>&1
        
        echo ""
        echo "✓ コミット日時の変更が完了しました"
        echo ""
        # 変更後のコミットを表示（ハッシュは変わっている可能性があるため、HEADから確認）
        git log -1 --pretty=fuller
    else
        # rebaseが対話的エディタを開いた場合、手動操作が必要
        echo ""
        echo "⚠ rebaseエディタが開かれました"
        echo "以下の手順を実行してください:"
        echo ""
        echo "1. エディタで対象のコミット行の先頭を 'pick' から 'edit' に変更"
        echo "2. エディタを保存して閉じる"
        echo "3. エディタが閉じられたら、以下を実行:"
        echo "   GIT_COMMITTER_DATE=\"$ISO_DATE\" git commit --amend --date=\"$ISO_DATE\" --no-edit"
        echo "   git rebase --continue"
        echo ""
        exit 1
    fi
    
    # 一時ファイルを削除
    rm -f "$EDITOR_SCRIPT"
fi

