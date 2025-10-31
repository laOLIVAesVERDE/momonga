import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
} from '@mui/material';
import { Comment } from '../types/Article';

interface CommentListProps {
  comments: Comment[];
}

const CommentList: React.FC<CommentListProps> = ({ comments }) => {
  const formatContent = (content: string) => {
    return content.split('\n').map((line, index) => (
      <Typography key={index} variant="body2" component="div">
        {line}
      </Typography>
    ));
  };

  const getInitials = (name: string) => {
    return name.charAt(0).toUpperCase();
  };

  const getAgeGenderText = (age: string | null, gender: string | null) => {
    const parts = [];
    if (age) parts.push(age);
    if (gender) parts.push(gender);
    return parts.length > 0 ? parts.join(' ') : null;
  };

  if (comments.length === 0) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            コメント
          </Typography>
          <Typography variant="body2" color="text.secondary">
            コメントはまだありません。
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          コメント ({comments.length}件)
        </Typography>
        <List>
          {comments.map((comment, index) => (
            <React.Fragment key={index}>
              <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: 'primary.main' }}>
                    {getInitials(comment.name)}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Typography variant="subtitle2" component="span">
                        {comment.name}
                      </Typography>
                      {getAgeGenderText(comment.age, comment.gender) && (
                        <Chip
                          label={getAgeGenderText(comment.age, comment.gender)}
                          size="small"
                          variant="outlined"
                          color="primary"
                        />
                      )}
                      <Typography variant="caption" color="text.secondary">
                        {comment.date}
                      </Typography>
                    </Box>
                  }
                  secondary={
                    <Box sx={{ mt: 1 }}>
                      {formatContent(comment.content)}
                    </Box>
                  }
                />
              </ListItem>
              {index < comments.length - 1 && <Divider variant="inset" component="li" />}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default CommentList;

