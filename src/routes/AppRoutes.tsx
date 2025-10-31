import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ArticleList from '../components/ArticleList';
import ArticleDetail from '../components/ArticleDetail';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ArticleList />} />
      <Route path="/article/:id" element={<ArticleDetail />} />
    </Routes>
  );
};

export default AppRoutes;
