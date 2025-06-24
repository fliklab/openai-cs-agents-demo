import React from "react";

interface ArticleItem {
  thumbnail?: string;
  title: string;
  description: string;
}

interface ArticlePreviewListProps {
  articles: ArticleItem[];
  actions: {
    label: string;
    onClick: () => void;
  }[];
}

export function ArticlePreviewList({
  articles,
  actions,
}: ArticlePreviewListProps) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-4 w-full max-w-xs mx-auto flex flex-col">
      <div className="flex flex-col gap-3 mb-4">
        {articles.map((article, idx) => (
          <div key={idx} className="flex items-center gap-3">
            {article.thumbnail ? (
              <img
                src={article.thumbnail}
                alt={article.title}
                className="w-12 h-12 object-cover rounded-md border border-gray-200"
              />
            ) : (
              <div className="w-12 h-12 flex items-center justify-center bg-gray-100 rounded-md text-gray-400 text-xl">
                <span>📰</span>
              </div>
            )}
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-sm text-gray-900 truncate">
                {article.title}
              </div>
              <div className="text-xs text-gray-500 truncate">
                {article.description}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-2 mt-auto">
        {actions.map((action, idx) => (
          <button
            key={idx}
            onClick={action.onClick}
            className="flex-1 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium text-sm transition-colors border border-gray-200"
          >
            {action.label}
          </button>
        ))}
      </div>
    </div>
  );
}
