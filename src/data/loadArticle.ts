import { ArticleListItem, Article } from "../types/Article";

// 利用可能なカテゴリ
const CATEGORIES = ["0026", "0014", "0011", "0006", "0029"];

export const loadArticleList = async (category?: string): Promise<ArticleListItem[]> => {
    try {
        const articles: ArticleListItem[] = [];

        // カテゴリが指定された場合はそのカテゴリのみ、指定されない場合は全カテゴリ
        const targetCategories = category ? [category] : CATEGORIES;

        for (const cat of targetCategories) {
            // 各カテゴリで1-300まで試行
            for (let i = 1; i <= 300; i++) {
                const articleId = `article_${i.toString().padStart(3, "0")}`;
                try {
                    const response = await fetch(`/articles/${cat}/${articleId}.json`);
                    if (response.ok) {
                        const articleData = await response.json();
                        articles.push({
                            id: `${cat}_${i.toString().padStart(3, "0")}`,
                            title: articleData.title,
                            date: articleData.date,
                            url: articleData.url,
                            comments: articleData.comments || [],
                        });
                    }
                } catch (error) {
                    // 個別の記事でエラーが発生しても続行
                    // 404エラーなどは無視
                }
            }
        }

        // 日付の降順でソート（新しい順）
        articles.sort((a, b) => {
            const dateA = parseJapaneseDate(a.date);
            const dateB = parseJapaneseDate(b.date);
            return dateB.getTime() - dateA.getTime();
        });

        return articles;
    } catch (error) {
        console.error("記事一覧の読み込みに失敗しました:", error);
        return [];
    }
};

// 個別記事の詳細を読み込む
export const loadArticleDetail = async (articleId: string): Promise<Article | null> => {
    try {
        // articleIdの形式: "0026_001" または "article_001"
        // カテゴリとIDを抽出
        let category: string;
        let articleNum: string;
        
        if (articleId.match(/^\d{4}_\d{3}$/)) {
            // "0026_001"形式
            [category, articleNum] = articleId.split('_');
        } else if (articleId.match(/^article_\d{3}$/)) {
            // "article_001"形式（後方互換性のため）
            category = "0026"; // デフォルトカテゴリ
            articleNum = articleId.replace("article_", "");
        } else {
            throw new Error(`Invalid article ID format: ${articleId}`);
        }
        
        const response = await fetch(`/articles/${category}/article_${articleNum}.json`);
        
        if (!response.ok) {
            throw new Error(`記事が見つかりません: ${articleId}`);
        }
        
        const articleData = await response.json();
        
        return {
            id: articleId,
            title: articleData.title,
            date: articleData.date,
            url: articleData.url,
            content: articleData.content,
            comments: articleData.comments || [],
        };
    } catch (error) {
        console.error(`記事の読み込みに失敗しました: ${articleId}`, error);
        throw error;
    }
};

// 日付文字列（例: "2025年9月1日"）をDateオブジェクトに変換
const parseJapaneseDate = (dateStr: string): Date => {
    const match = dateStr.match(/(\d+)年(\d+)月(\d+)日/);
    if (!match) {
        return new Date(0); // パースできない場合は古い日付として扱う
    }
    const [, year, month, day] = match;
    return new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
};
