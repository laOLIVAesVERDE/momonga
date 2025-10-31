import React, { createContext, useContext, useState, ReactNode } from "react";
import { ArticleListItem } from "../types/Article";
import { loadArticleList } from "../data/loadArticle";

interface ArticleContextType {
    articles: ArticleListItem[];
    loading: boolean;
    fetchArticles: (category?: string) => Promise<void>;
    hasLoaded: boolean;
}

const ArticleContext = createContext<ArticleContextType | undefined>(undefined);

export const ArticleProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [articles, setArticles] = useState<ArticleListItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasLoaded, setHasLoaded] = useState(false);

    const fetchArticles = async (category?: string) => {
        setLoading(true);
        try {
            const loadedArticles = await loadArticleList(category);
            setArticles(loadedArticles);
            setHasLoaded(true);
        } catch (error) {
            console.error("記事の読み込みに失敗しました:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ArticleContext.Provider value={{ articles, loading, fetchArticles, hasLoaded }}>
            {children}
        </ArticleContext.Provider>
    );
};

export const useArticles = () => {
    const context = useContext(ArticleContext);
    if (context === undefined) {
        throw new Error("useArticles must be used within an ArticleProvider");
    }
    return context;
};

