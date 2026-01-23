import { useState, useEffect } from 'react';
import './App.css';
import { calculator } from './utils/calculator';
import type { SectorInput, CalculationResult, Sector } from './types';
import { SectorForm } from './components/SectorForm';
import { ResultsDashboard } from './components/ResultsDashboard';

function App() {
  const [sectors, setSectors] = useState<Sector[]>([]);
  const [inputs, setInputs] = useState<SectorInput[]>([]);
  const [results, setResults] = useState<CalculationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);

  // Load data on mount
  useEffect(() => {
    async function loadData() {
      try {
        // Load sectors
        const sectorsResponse = await fetch('/data/sectors.json');
        const sectorsData = await sectorsResponse.json();
        setSectors(sectorsData);

        // Load multipliers
        await calculator.loadMultipliers();

        setLoading(false);
      } catch (error) {
        console.error('Failed to load data:', error);
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const handleCalculate = () => {
    if (inputs.length === 0) {
      alert('Please add at least one sector with spending amount');
      return;
    }

    setCalculating(true);

    try {
      const result = calculator.calculate(inputs);
      setResults(result);
    } catch (error) {
      console.error('Calculation failed:', error);
      alert('Calculation failed. Please check your inputs.');
    } finally {
      setCalculating(false);
    }
  };

  const handleReset = () => {
    setInputs([]);
    setResults(null);
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading Open DIO...</h2>
          <p>Initializing calculation engine</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🌍 Open DIO</h1>
        <p className="tagline">
          Calculate the environmental impact of defense spending
        </p>
        <p className="subtitle">
          Using the Defense Input-Output Model v2.0
        </p>
      </header>

      <main className="main">
        <div className="container">
          <SectorForm
            sectors={sectors}
            inputs={inputs}
            onInputsChange={setInputs}
            onCalculate={handleCalculate}
            onReset={handleReset}
            calculating={calculating}
          />

          {results && (
            <ResultsDashboard
              results={results}
              calculator={calculator}
            />
          )}

          <footer className="footer">
            <p>
              <strong>About</strong>: Open DIO makes military environmental
              impact analysis accessible to researchers, journalists, and the public.
            </p>
            <p>
              <strong>Data</strong>: Based on EPA's Defense Input-Output Model v2.0
              | <strong>Method</strong>: Environmentally-Extended Input-Output Analysis
            </p>
            <p className="credit">
              Built with ❤️ for transparency | Open Source |{' '}
              <a href="https://github.com/kelaxten/DIO-v3" target="_blank" rel="noopener noreferrer">
                View on GitHub
              </a>
            </p>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
