export interface Article {
    id: string;
    title: string;
    date: string;
    url: string;
    content: string;
    comments?: Comment[];
}

export interface Comment {
    type: string | null;
    name: string;
    age: string | null;
    gender: string | null;
    date: string;
    content: string;
}

export interface ArticleListItem {
    id: string;
    title: string;
    date: string;
    url: string;
    comments: Comment[];
}
