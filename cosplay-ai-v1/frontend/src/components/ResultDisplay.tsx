import React, { useState } from 'react';

interface ResultDisplayProps {
  result: string;
  originalImage: string | null;
  character: string;
  onReset: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({
  result,
  originalImage,
  character,
  onReset
}) => {
  const [activeTab, setActiveTab] = useState<'result' | 'comparison'>('result');
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    try {
      setDownloading(true);
      
      // Create a temporary link to download the image
      const link = document.createElement('a');
      link.href = result;
      link.download = `cosplay-${character}-${Date.now()}.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setDownloading(false);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Cosplay AI Generation',
          text: `Check out my cosplay transformation as ${character}!`,
          url: window.location.href
        });
      } catch (error) {
        console.error('Share failed:', error);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  const getCharacterName = (characterId: string) => {
    const names: { [key: string]: string } = {
      'sailor-moon': 'Sailor Moon',
      'wonder-woman': 'Wonder Woman',
      'dva': 'D.Va',
      'harley-quinn': 'Harley Quinn',
      'zelda': 'Princess Zelda',
      'power-girl': 'Power Girl',
      '2b': '2B',
      'mikasa': 'Mikasa Ackerman',
      'catwoman': 'Catwoman',
      'ahri': 'Ahri'
    };
    return names[characterId] || characterId;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="space-y-6">
        {/* Header */}
        <div className="text-center">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-green-100 text-green-800 text-sm font-medium mb-4">
            <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Generation Complete!
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Your {getCharacterName(character)} Cosplay
          </h3>
          <p className="text-gray-600">
            Your photo has been transformed into an amazing cosplay image
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setActiveTab('result')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'result'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Result
          </button>
          {originalImage && (
            <button
              onClick={() => setActiveTab('comparison')}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'comparison'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Comparison
            </button>
          )}
        </div>

        {/* Content */}
        {activeTab === 'result' ? (
          <div className="space-y-4">
            <div className="relative group">
              <img
                src={result}
                alt="Generated cosplay"
                className="w-full h-auto rounded-lg shadow-md"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div className="flex space-x-2">
                  <button
                    onClick={handleDownload}
                    disabled={downloading}
                    className="bg-white text-gray-900 px-4 py-2 rounded-lg shadow-lg hover:bg-gray-100 transition-colors disabled:opacity-50"
                  >
                    {downloading ? (
                      <svg className="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : (
                      <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    )}
                  </button>
                  <button
                    onClick={handleShare}
                    className="bg-white text-gray-900 px-4 py-2 rounded-lg shadow-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="text-center">
                <h4 className="text-sm font-medium text-gray-900 mb-2">Original</h4>
                <img
                  src={originalImage || ''}
                  alt="Original photo"
                  className="w-full h-auto rounded-lg shadow-md"
                />
              </div>
              <div className="text-center">
                <h4 className="text-sm font-medium text-gray-900 mb-2">Cosplay Result</h4>
                <img
                  src={result}
                  alt="Generated cosplay"
                  className="w-full h-auto rounded-lg shadow-md"
                />
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {downloading ? (
              <>
                <svg className="h-4 w-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Downloading...
              </>
            ) : (
              <>
                <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Image
              </>
            )}
          </button>
          
          <button
            onClick={handleShare}
            className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
            Share Result
          </button>
          
          <button
            onClick={onReset}
            className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Generate Another
          </button>
        </div>

        {/* Quality Info */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Generation Details</h4>
          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
            <div>
              <span className="font-medium">Character:</span> {getCharacterName(character)}
            </div>
            <div>
              <span className="font-medium">Quality:</span> High
            </div>
            <div>
              <span className="font-medium">Style:</span> AI Enhanced
            </div>
            <div>
              <span className="font-medium">Generated:</span> {new Date().toLocaleString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;