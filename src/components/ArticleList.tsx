import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {

    
    
    Box,
    Card,
    CardContent,
    Typography,
    List,
    ListItem,
    ListItemButton,
    ListItemText,
    Chip,
    Container,
    AppBar,
    Toolbar,
} from "@mui/material";
import { useArticles } from "../context/ArticleContext";

const ArticleList: React.FC = () => {
    const { articles, loading, fetchArticles, hasLoaded } = useArticles();
    const navigate = useNavigate();

    useEffect(() => {
        if (!hasLoaded && !loading) {
            fetchArticles();
        }
    }, [hasLoaded, loading, fetchArticles]);

    const handleArticleSelect = (articleId: string) => {
        navigate(`/article/${articleId}`);
    };

    if (loading) {
        return (
            <Box>
                <AppBar position="static" color="primary">
                    <Toolbar>
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{ flexGrow: 1 }}
                        >
                            記事一覧
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
                        記事一覧を読み込み中...
                    </div>
                </Container>
            </Box>
        );
    }
    return (
        <Box>
            <AppBar position="static" color="primary">
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ flexGrow: 1 }}
                    >
                        記事一覧
                    </Typography>
                </Toolbar>
            </AppBar>

            <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
                <Card>
                    <CardContent>
                        <Typography variant="h4" component="h1" gutterBottom>
                            記事一覧
                        </Typography>
                        <Typography
                            variant="body1"
                            color="text.secondary"
                            sx={{ mb: 3 }}
                        >
                            {articles.length}件の記事が見つかりました
                        </Typography>

                        <List>
                            {articles.map((article) => (
                                <ListItem key={article.id} disablePadding>
                                    <ListItemButton
                                        onClick={() =>
                                            handleArticleSelect(article.id)
                                        }
                                        sx={{
                                            border: "1px solid",
                                            borderColor: "divider",
                                            borderRadius: 1,
                                            mb: 1,
                                            "&:hover": {
                                                backgroundColor: "action.hover",
                                            },
                                        }}
                                    >
                                        <ListItemText
                                            primary={
                                                <Typography
                                                    variant="h6"
                                                    component="div"
                                                >
                                                    {article.title}
                                                </Typography>
                                            }
                                            secondary={
                                                <Box sx={{ mt: 1 }}>
                                                    <Chip
                                                        label={article.date}
                                                        size="small"
                                                        color="primary"
                                                        variant="outlined"
                                                        sx={{ mr: 1 }}
                                                    />
                                                    <Typography
                                                        variant="body2"
                                                        color="text.secondary"
                                                        sx={{ mt: 1 }}
                                                    >
                                                        {
                                                            article.comments
                                                                .length
                                                        }
                                                        件のコメント
                                                    </Typography>
                                                </Box>
                                            }
                                        />
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
};

export default ArticleList;
