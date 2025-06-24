import React from "react";

interface ArticlePreviewProps {
  label?: string; // 상단 라벨 (예: "추천", "광고", "아티클")
  thumbnail?: string; // 이미지 URL
  title: string; // 제목
  description: string; // 설명/요약
  actions?: {
    label: string;
    onClick: () => void;
  }[];
}

export function ArticlePreview({
  label,
  thumbnail,
  title,
  description,
  actions = [],
}: ArticlePreviewProps) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-4 w-full max-w-xs mx-auto flex flex-col items-center">
      {label && (
        <div className="text-xs text-blue-500 font-semibold mb-2 self-start">
          {label}
        </div>
      )}
      {thumbnail ? (
        <img
          src={thumbnail}
          alt={title}
          className="w-24 h-24 object-cover rounded-full mb-3 border border-gray-200"
        />
      ) : (
        <div className="w-24 h-24 flex items-center justify-center bg-gray-100 rounded-full mb-3 text-gray-400 text-3xl">
          <span>📰</span>
        </div>
      )}
      <div className="w-full">
        <div className="font-bold text-base text-gray-900 mb-1 text-center">
          {title}
        </div>
        <div className="text-xs text-gray-500 mb-4 text-center whitespace-pre-line">
          {description}
        </div>
      </div>
      <div className="flex flex-col gap-2 w-full mt-auto">
        {actions.map((action, idx) => (
          <button
            key={idx}
            onClick={action.onClick}
            className="w-full py-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 font-medium text-sm transition-colors border border-blue-100"
          >
            {action.label}
          </button>
        ))}
      </div>
    </div>
  );
}
