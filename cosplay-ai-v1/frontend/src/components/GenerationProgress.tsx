import React, { useEffect, useState } from 'react';

interface GenerationProgressProps {
  status: 'uploading' | 'processing';
  progress: number;
  generationId: string | null;
  onComplete: (result: string) => void;
  onError: (error: string) => void;
}

const GenerationProgress: React.FC<GenerationProgressProps> = ({
  status,
  progress,
  generationId,
  onComplete,
  onError
}) => {
  const [currentProgress, setCurrentProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');

  useEffect(() => {
    if (status === 'uploading') {
      setStatusMessage('Uploading your photo...');
      setCurrentProgress(10);
    } else if (status === 'processing') {
      setStatusMessage('Generating your cosplay image...');
      setCurrentProgress(20);
      
      // Simulate progress updates
      const interval = setInterval(() => {
        setCurrentProgress(prev => {
          if (prev >= 90) {
            clearInterval(interval);
            return prev;
          }
          return prev + Math.random() * 10;
        });
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [status]);

  useEffect(() => {
    if (generationId && status === 'processing') {
      // Poll for generation status
      const pollInterval = setInterval(async () => {
        try {
          const response = await fetch(`http://localhost:8003/generation/${generationId}`);
          if (!response.ok) {
            throw new Error('Failed to check generation status');
          }
          
          const data = await response.json();
          
          if (data.status === 'completed') {
            setCurrentProgress(100);
            setStatusMessage('Generation complete!');
            onComplete(data.result_url || 'https://via.placeholder.com/512x512/3b82f6/ffffff?text=Cosplay+Image');
            clearInterval(pollInterval);
          } else if (data.status === 'failed') {
            onError('Generation failed. Please try again.');
            clearInterval(pollInterval);
          }
        } catch (error) {
          console.error('Error polling generation status:', error);
          // Don't clear interval on network errors, keep trying
        }
      }, 2000);

      // Cleanup after 5 minutes
      const timeout = setTimeout(() => {
        clearInterval(pollInterval);
        onError('Generation timed out. Please try again.');
      }, 300000);

      return () => {
        clearInterval(pollInterval);
        clearTimeout(timeout);
      };
    }
  }, [generationId, status, onComplete, onError]);

  const getProgressColor = () => {
    if (currentProgress < 30) return 'bg-blue-500';
    if (currentProgress < 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getStatusIcon = () => {
    if (status === 'uploading') {
      return (
        <svg className="h-8 w-8 text-blue-500 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      );
    }
    
    return (
      <svg className="h-8 w-8 text-purple-500 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="text-center space-y-6">
        {/* Status Icon */}
        <div className="flex justify-center">
          {getStatusIcon()}
        </div>

        {/* Status Message */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {statusMessage}
          </h3>
          <p className="text-sm text-gray-600">
            {status === 'uploading' 
              ? 'Please wait while we upload your photo...'
              : 'Our AI is working its magic to create your cosplay image...'
            }
          </p>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Progress</span>
            <span>{Math.round(currentProgress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ease-out ${getProgressColor()}`}
              style={{ width: `${currentProgress}%` }}
            ></div>
          </div>
        </div>

        {/* Generation ID */}
        {generationId && (
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs text-gray-600">
              Generation ID: <span className="font-mono">{generationId}</span>
            </p>
          </div>
        )}

        {/* Tips */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h4 className="text-sm font-medium text-blue-800">What's happening?</h4>
              <ul className="mt-1 text-sm text-blue-700 list-disc list-inside space-y-1">
                <li>Analyzing your photo for facial features and pose</li>
                <li>Building optimized prompts for the character</li>
                <li>Generating high-quality cosplay image with AI</li>
                <li>Processing and optimizing the final result</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Estimated Time */}
        <div className="text-sm text-gray-600">
          <span className="inline-flex items-center">
            <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Estimated time: {status === 'uploading' ? '30 seconds' : '2-3 minutes'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default GenerationProgress;