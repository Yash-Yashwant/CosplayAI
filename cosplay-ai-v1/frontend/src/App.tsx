import React, { useState } from 'react';
import PhotoUpload from './components/PhotoUpload';
import CharacterSelection from './components/CharacterSelection';
import GenerationProgress from './components/GenerationProgress';
import ResultDisplay from './components/ResultDisplay';

interface GenerationState {
  id: string | null;
  status: 'idle' | 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  result?: string;
  error?: string;
}

function App() {
  const [generationState, setGenerationState] = useState<GenerationState>({
    id: null,
    status: 'idle',
    progress: 0
  });

  const [selectedCharacter, setSelectedCharacter] = useState<string>('sailor-moon');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const handleImageUpload = async (imageData: string) => {
    setUploadedImage(imageData);
    setGenerationState(prev => ({ ...prev, status: 'uploading' }));

    try {
      // Convert data URL to blob
      const response = await fetch(imageData);
      const blob = await response.blob();

      // Create FormData
      const formData = new FormData();
      formData.append('photo', blob, 'photo.jpg');
      formData.append('character', selectedCharacter);
      formData.append('style', 'anime');
      formData.append('quality', 'high');

      console.log('Sending character:', selectedCharacter);

      // Call generation API
      const apiResponse = await fetch('http://localhost:8003/generate-cosplay', {
        method: 'POST',
        body: formData,
      });

      if (!apiResponse.ok) {
        throw new Error('Generation failed');
      }

      const result = await apiResponse.json();
      handleGenerationStart(result.generation_id);
    } catch (error) {
      console.error('Generation error:', error);
      setGenerationState(prev => ({ ...prev, status: 'error', error: 'Failed to start generation' }));
    }
  };

  const handleGenerationStart = (generationId: string) => {
    setGenerationState(prev => ({
      ...prev,
      id: generationId,
      status: 'processing',
      progress: 0
    }));
  };

  const handleGenerationComplete = (result: string) => {
    setGenerationState(prev => ({
      ...prev,
      status: 'completed',
      progress: 100,
      result
    }));
  };

  const handleGenerationError = (error: string) => {
    setGenerationState(prev => ({
      ...prev,
      status: 'error',
      error
    }));
  };

  const resetGeneration = () => {
    setGenerationState({
      id: null,
      status: 'idle',
      progress: 0
    });
    setUploadedImage(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-3xl font-bold text-gray-900">
                  Cosplay AI
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Transform your photos into amazing cosplay images
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                V1 Beta
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload and Character Selection */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Upload Your Photo
              </h2>
              <PhotoUpload
                onImageUpload={handleImageUpload}
                disabled={generationState.status === 'processing'}
              />
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Choose Character
              </h2>
              <CharacterSelection
                selectedCharacter={selectedCharacter}
                onCharacterSelect={setSelectedCharacter}
                disabled={generationState.status === 'processing'}
              />
            </div>
          </div>

          {/* Right Column - Generation and Results */}
          <div className="space-y-6">
            {generationState.status === 'idle' && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-center py-12">
                  <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <svg className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Ready to Generate
                  </h3>
                  <p className="text-gray-600">
                    Upload a photo and select a character to get started
                  </p>
                </div>
              </div>
            )}

            {(generationState.status === 'uploading' || generationState.status === 'processing') && (
              <GenerationProgress
                status={generationState.status}
                progress={generationState.progress}
                generationId={generationState.id}
                onComplete={handleGenerationComplete}
                onError={handleGenerationError}
              />
            )}

            {generationState.status === 'completed' && generationState.result && (
              <ResultDisplay
                result={generationState.result}
                originalImage={uploadedImage}
                character={selectedCharacter}
                onReset={resetGeneration}
              />
            )}

            {generationState.status === 'error' && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-center py-12">
                  <div className="mx-auto h-24 w-24 bg-red-100 rounded-full flex items-center justify-center mb-4">
                    <svg className="h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Generation Failed
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {generationState.error || 'An unexpected error occurred'}
                  </p>
                  <button
                    onClick={resetGeneration}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Cosplay AI. Built with FastAPI, React, and Google Imagen Pro.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
