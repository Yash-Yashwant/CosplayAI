import React, { useCallback, useState } from 'react';

interface PhotoUploadProps {
  onImageUpload: (imageData: string) => void;
  disabled?: boolean;
}

const PhotoUpload: React.FC<PhotoUploadProps> = ({ onImageUpload, disabled = false }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files || files.length === 0) return;

    const file = files[0];
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (JPEG, PNG, WebP)');
      return;
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setError(null);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      setPreview(result);
      onImageUpload(result);
    };
    reader.readAsDataURL(file);
  }, [onImageUpload]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (disabled) return;
    
    handleFiles(e.dataTransfer.files);
  }, [disabled, handleFiles]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (disabled) return;
    
    handleFiles(e.target.files);
  }, [disabled, handleFiles]);

  const handleClick = useCallback(() => {
    if (disabled) return;
    document.getElementById('file-upload')?.click();
  }, [disabled]);

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
          dragActive
            ? 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          id="file-upload"
          type="file"
          className="hidden"
          accept="image/*"
          onChange={handleChange}
          disabled={disabled}
        />
        
        <div className="text-center">
          {preview ? (
            <div className="space-y-4">
              <img
                src={preview}
                alt="Preview"
                className="mx-auto h-32 w-32 object-cover rounded-lg shadow-md"
              />
              <p className="text-sm text-gray-600">
                Click to change photo
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="mx-auto h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center">
                <svg className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {disabled ? 'Upload disabled' : 'Click to upload or drag and drop'}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  PNG, JPG, WebP up to 10MB
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Upload Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">Tips for best results:</h3>
            <ul className="mt-1 text-sm text-blue-700 list-disc list-inside">
              <li>Use clear, well-lit photos</li>
              <li>Face should be clearly visible</li>
              <li>Avoid heavily filtered or edited images</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoUpload;