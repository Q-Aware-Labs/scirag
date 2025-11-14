import { ExternalLink, Calendar, Users, CheckSquare, Square } from 'lucide-react';
import { Paper } from '../api/client';

interface Props {
  paper: Paper;
  isSelected?: boolean;
  onToggleSelect?: (paper: Paper) => void;
}

export default function PaperCard({ paper, isSelected = false, onToggleSelect }: Props) {
  return (
    <div
      className={`card-brutal bg-white p-5 shadow-brutal hover:shadow-brutal-lg hover:-translate-y-1 transition-all duration-150 ${
        isSelected ? 'ring-4 ring-neo-pink' : ''
      }`}
    >
      <div className="space-y-3">
        {/* Selection Checkbox and Title */}
        <div className="flex items-start gap-3">
          {onToggleSelect && (
            <button
              onClick={() => onToggleSelect(paper)}
              className="flex-shrink-0 mt-1 hover:scale-110 transition-transform"
              aria-label={isSelected ? "Deselect paper" : "Select paper"}
            >
              {isSelected ? (
                <CheckSquare className="w-6 h-6 text-neo-pink" strokeWidth={3} />
              ) : (
                <Square className="w-6 h-6" strokeWidth={3} />
              )}
            </button>
          )}

          <h3 className="font-bold text-lg leading-tight flex-1">
            {paper.title}
          </h3>
        </div>

        {/* Meta Info */}
        <div className="flex flex-wrap gap-3 text-sm">
          <div className="flex items-center gap-1 bg-neo-peach border-2 border-black px-2 py-1">
            <Users className="w-4 h-4" />
            <span className="font-semibold">
              {paper.authors[0]}
              {paper.authors.length > 1 && ` +${paper.authors.length - 1}`}
            </span>
          </div>
          
          <div className="flex items-center gap-1 bg-neo-green border-2 border-black px-2 py-1">
            <Calendar className="w-4 h-4" />
            <span className="font-semibold">{paper.published}</span>
          </div>
        </div>

        {/* Summary */}
        <p className="text-sm leading-relaxed line-clamp-3">
          {paper.summary}
        </p>

        {/* Categories */}
        <div className="flex flex-wrap gap-2">
          {paper.categories.slice(0, 3).map((cat) => (
            <span
              key={cat}
              className="text-xs font-bold bg-neo-cyan border-2 border-black px-2 py-1"
            >
              {cat}
            </span>
          ))}
        </div>

        {/* Link */}
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 font-bold text-sm hover:underline"
        >
          <ExternalLink className="w-4 h-4" />
          View on arXiv
        </a>
      </div>
    </div>
  );
}
