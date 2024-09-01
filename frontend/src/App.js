import React, { useState, useEffect } from 'react';
import { Box, Input, Button, Textarea, VStack } from '@chakra-ui/react';

function App() {
  const [playerNames, setPlayerNames] = useState([]);
  const [inputs, setInputs] = useState(Array(22).fill(''));
  const [suggestions, setSuggestions] = useState(Array(22).fill([]));
  const [pitchReport, setPitchReport] = useState('');

  useEffect(() => {
    fetch('/home/ubuntu/attachments/PlayerNamess.txt')
      .then(response => response.text())
      .then(data => {
        const names = data.split('\n').map(name => name.trim()).filter(name => name);
        setPlayerNames(names);
      })
      .catch(error => console.error('Error fetching player names:', error));
  }, []);

  const handleInputChange = (index, value) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);

    const newSuggestions = [...suggestions];
    newSuggestions[index] = playerNames.filter(name =>
      name.toLowerCase().includes(value.toLowerCase())
    );
    setSuggestions(newSuggestions);
  };

  const handleSubmit = () => {
    const selectedPlayerNames = inputs.filter(input => input.trim() !== '');
    fetch('http://127.0.0.1:8000/analyze_pitch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pitch_report: pitchReport,
        player_names: selectedPlayerNames,
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Selected players:', data.selected_players);
        console.log('Captain:', data.captain);
        console.log('Vice-Captain:', data.vice_captain);
      })
      .catch(error => console.error('Error analyzing pitch:', error));
  };

  return (
    <Box p={5}>
      <VStack spacing={4}>
        {inputs.map((input, index) => (
          <Box key={index} position="relative" width="100%">
            <Input
              value={input}
              onChange={(e) => handleInputChange(index, e.target.value)}
              placeholder={`Player ${index + 1}`}
            />
            {suggestions[index].length > 0 && (
              <Box position="absolute" bg="white" border="1px" borderColor="gray.200" zIndex="1" width="100%">
                {suggestions[index].map((suggestion, sIndex) => (
                  <Box
                    key={sIndex}
                    p={2}
                    cursor="pointer"
                    _hover={{ bg: 'gray.100' }}
                    onClick={() => handleInputChange(index, suggestion)}
                  >
                    {suggestion}
                  </Box>
                ))}
              </Box>
            )}
          </Box>
        ))}
        <Textarea
          value={pitchReport}
          onChange={(e) => setPitchReport(e.target.value)}
          placeholder="Enter pitch report"
        />
        <Button colorScheme="teal" onClick={handleSubmit}>
          Submit
        </Button>
      </VStack>
    </Box>
  );
}

export default App;
