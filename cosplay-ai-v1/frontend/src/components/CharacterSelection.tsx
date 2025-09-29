import React, { useState, useEffect } from 'react';

interface Character {
  id: string;
  name: string;
  style: string;
  description: string;
}

interface CharacterSelectionProps {
  selectedCharacter: string;
  onCharacterSelect: (characterId: string) => void;
  disabled?: boolean;
}

const CharacterSelection: React.FC<CharacterSelectionProps> = ({
  selectedCharacter,
  onCharacterSelect,
  disabled = false
}) => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCharacters();
  }, []);

  const fetchCharacters = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8003/characters');
      if (!response.ok) {
        throw new Error('Failed to fetch characters');
      }
      const data = await response.json();
      setCharacters(data.characters);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load characters');
      // Fallback to hardcoded characters if API fails
      setCharacters([
        { id: 'sailor-moon', name: 'Sailor Moon', style: 'anime', description: 'Classic anime magical girl' },
        { id: 'wonder-woman', name: 'Wonder Woman', style: 'superhero', description: 'Amazonian warrior princess' },
        { id: 'dva', name: 'D.Va', style: 'gaming', description: 'Professional gamer and mech pilot' },
        { id: 'harley-quinn', name: 'Harley Quinn', style: 'comic', description: 'Chaotic villain with jester costume' },
        { id: 'zelda', name: 'Princess Zelda', style: 'fantasy', description: 'Royal princess with magical powers' },
        { id: 'power-girl', name: 'Power Girl', style: 'superhero', description: 'Powerful superhero with classic costume' },
        { id: '2b', name: '2B', style: 'gaming', description: 'Android combat unit with elegant design' },
        { id: 'mikasa', name: 'Mikasa Ackerman', style: 'anime', description: 'Skilled soldier with military uniform' },
        { id: 'catwoman', name: 'Catwoman', style: 'comic', description: 'Feline-themed thief with sleek costume' },
        { id: 'ahri', name: 'Ahri', style: 'gaming', description: 'Nine-tailed fox spirit with magical attire' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getStyleColor = (style: string) => {
    const colors = {
      anime: 'bg-pink-100 text-pink-800',
      superhero: 'bg-blue-100 text-blue-800',
      gaming: 'bg-purple-100 text-purple-800',
      comic: 'bg-red-100 text-red-800',
      fantasy: 'bg-green-100 text-green-800'
    };
    return colors[style as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getCharacterImage = (characterId: string) => {
    // In a real app, these would be actual character images
    const images = {
      'sailor-moon': '🌙',
      'wonder-woman': '🦸‍♀️',
      'dva': '🎮',
      'harley-quinn': '🎭',
      'zelda': '👑',
      'power-girl': '⚡',
      '2b': '🤖',
      'mikasa': '⚔️',
      'catwoman': '🐱',
      'ahri': '🦊'
    };
    return images[characterId as keyof typeof images] || '👤';
  };

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-gray-200 rounded-lg p-4 animate-pulse">
              <div className="h-8 w-8 bg-gray-300 rounded-full mx-auto mb-2"></div>
              <div className="h-4 bg-gray-300 rounded mb-1"></div>
              <div className="h-3 bg-gray-300 rounded w-3/4 mx-auto"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-yellow-800">
              Using offline character list. {error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Character Grid */}
      <div className="grid grid-cols-2 gap-3">
        {characters.map((character) => (
          <button
            key={character.id}
            onClick={() => !disabled && onCharacterSelect(character.id)}
            disabled={disabled}
            className={`relative p-4 rounded-lg border-2 transition-all ${
              selectedCharacter === character.id
                ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-200'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <div className="text-center space-y-2">
              <div className="text-2xl mb-1">
                {getCharacterImage(character.id)}
              </div>
              <h3 className="text-sm font-medium text-gray-900 truncate">
                {character.name}
              </h3>
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStyleColor(character.style)}`}>
                {character.style}
              </span>
            </div>
            
            {/* Selection indicator */}
            {selectedCharacter === character.id && (
              <div className="absolute top-2 right-2">
                <div className="h-5 w-5 bg-primary-500 rounded-full flex items-center justify-center">
                  <svg className="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Selected Character Details */}
      {selectedCharacter && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <div className="text-2xl">
              {getCharacterImage(selectedCharacter)}
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-medium text-gray-900">
                {characters.find(c => c.id === selectedCharacter)?.name}
              </h4>
              <p className="text-xs text-gray-600 mt-1">
                {characters.find(c => c.id === selectedCharacter)?.description}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Style Filter */}
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-900">Filter by Style:</h4>
        <div className="flex flex-wrap gap-2">
          {['all', 'anime', 'superhero', 'gaming', 'comic', 'fantasy'].map((style) => (
            <button
              key={style}
              onClick={() => {
                // In a real app, this would filter the character list
                console.log(`Filter by ${style}`);
              }}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                style === 'all'
                  ? 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                  : getStyleColor(style)
              }`}
            >
              {style === 'all' ? 'All Styles' : style}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CharacterSelection;