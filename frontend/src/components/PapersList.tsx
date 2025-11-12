import { FileText, CheckCircle2 } from 'lucide-react';
import { Paper } from '../api/client';

interface Props {
  selectedPapers: Paper[];
  processedPaperIds: string[];
}

export default function PapersList({ selectedPapers, processedPaperIds }: Props) {
  return (
    <div className="sticky top-4">
      <div className="card-brutal bg-neo-pink p-5 shadow-brutal-lg">
        <h3 className="font-display text-2xl font-black mb-4 flex items-center gap-2">
          <FileText className="w-6 h-6" />
          Papers
        </h3>

        {selectedPapers.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p className="font-bold text-sm opacity-50">
              No papers selected yet
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {selectedPapers.map((paper) => {
              const isProcessed = processedPaperIds.includes(paper.paper_id);
              
              return (
                <div
                  key={paper.paper_id}
                  className={`card-brutal p-3 transition-all duration-150 ${
                    isProcessed
                      ? 'bg-neo-green shadow-brutal-sm'
                      : 'bg-white shadow-brutal-sm'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {isProcessed && (
                      <CheckCircle2 className="w-5 h-5 flex-shrink-0 text-green-700 mt-0.5" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-sm leading-tight line-clamp-2">
                        {paper.title}
                      </p>
                      <p className="text-xs mt-1 opacity-75">
                        {paper.authors[0].split(' ').slice(-1)[0]} et al.
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}

            {/* Status */}
            <div className="border-t-2 border-black pt-3 mt-3">
              <p className="text-sm font-bold">
                {processedPaperIds.length > 0 ? (
                  <span className="text-green-700">
                    ✓ {processedPaperIds.length} paper{processedPaperIds.length !== 1 ? 's' : ''} processed
                  </span>
                ) : (
                  <span className="opacity-50">
                    Not processed yet
                  </span>
                )}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
