import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
    Box,
    Card,
    CardContent,
    Typography,
    Container,
    AppBar,
    Toolbar,
    IconButton,
    Chip,
    Link,
    Divider,
    Paper,
} from "@mui/material";
import { Article } from "../types/Article";
import CommentList from "./CommentList";
import { loadArticleDetail } from "../data/loadArticle";

const ArticleDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [article, setArticle] = useState<Article | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchArticle = async () => {
            if (!id) return;

            setLoading(true);
            const articleData = await loadArticleDetail(id);
            setArticle(articleData);
            setLoading(false);
        };

        fetchArticle();
    }, [id]);

    const handleBack = () => {
        navigate("/");
    };

    if (loading) {
        return (
            <Box>
                <AppBar position="static" color="primary">
                    <Toolbar>
                        <IconButton
                            edge="start"
                            color="inherit"
                            onClick={handleBack}
                            sx={{ mr: 2 }}
                        >
                            ←
                        </IconButton>
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{ flexGrow: 1 }}
                        >
                            記事詳細
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            height: "50vh",
                            fontSize: "18px",
                        }}
                    >
                        記事詳細を読み込み中...
                    </div>
                </Container>
            </Box>
        );
    }

    if (!article) {
        return (
            <Box>
                <AppBar position="static" color="primary">
                    <Toolbar>
                        <IconButton
                            edge="start"
                            color="inherit"
                            onClick={handleBack}
                            sx={{ mr: 2 }}
                        >
                            ←
                        </IconButton>
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{ flexGrow: 1 }}
                        >
                            記事詳細
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            height: "50vh",
                            fontSize: "18px",
                        }}
                    >
                        記事が見つかりません
                    </div>
                </Container>
            </Box>
        );
    }
    const formatContent = (content: string) => {
        return content.split("\n").map((paragraph, index) => {
            if (paragraph.trim() === "") {
                return <br key={index} />;
            }
            return (
                <Typography
                    key={index}
                    variant="body1"
                    paragraph
                    sx={{ lineHeight: 1.8 }}
                >
                    {paragraph}
                </Typography>
            );
        });
    };

    return (
        <Box>
            <AppBar position="static" color="primary">
                <Toolbar>
                    <IconButton
                        edge="start"
                        color="inherit"
                        onClick={handleBack}
                        sx={{ mr: 2 }}
                    >
                        ←
                    </IconButton>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ flexGrow: 1 }}
                    >
                        記事詳細
                    </Typography>
                </Toolbar>
            </AppBar>

            <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
                <Card>
                    <CardContent>
                        <Typography variant="h4" component="h1" gutterBottom>
                            {article.title}
                        </Typography>

                        <Box sx={{ mb: 3 }}>
                            <Chip
                                label={article.date}
                                color="primary"
                                variant="outlined"
                                sx={{ mr: 2 }}
                            />
                            <Link
                                href={article.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                variant="body2"
                                color="primary"
                            >
                                元記事を開く
                            </Link>
                        </Box>

                        <Divider sx={{ mb: 3 }} />

                        <Paper
                            elevation={0}
                            sx={{
                                p: 3,
                                backgroundColor: "grey.50",
                                borderRadius: 2,
                                mb: 3,
                            }}
                        >
                            <Typography
                                variant="h6"
                                gutterBottom
                                color="primary"
                            >
                                記事内容
                            </Typography>
                            {formatContent(article.content)}
                        </Paper>

                        {article.comments && article.comments.length > 0 && (
                            <CommentList comments={article.comments} />
                        )}
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
};

export default ArticleDetail;
