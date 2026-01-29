import { useState, useEffect } from 'react';
import './App.css';
import { apiClient } from './services/api';
import type { SectorInput, CalculationResult, Sector } from './types';
import { SectorForm } from './components/SectorForm';
import { ResultsDashboard } from './components/ResultsDashboard';
import Methodology from './components/Methodology';
import Glossary from './components/Glossary';

type View = 'calculator' | 'methodology' | 'glossary';

function App() {
  const [view, setView] = useState<View>('calculator');
  const [sectors, setSectors] = useState<Sector[]>([]);
  const [inputs, setInputs] = useState<SectorInput[]>([]);
  const [results, setResults] = useState<CalculationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);

  // Load data on mount
  useEffect(() => {
    async function loadData() {
      try {
        // Fetch sectors from API
        const sectorsData = await apiClient.getSectors();
        setSectors(sectorsData);

        // Check API health
        await apiClient.healthCheck();

        setLoading(false);
      } catch (error) {
        console.error('Failed to load data:', error);
        alert('Failed to connect to API. Make sure the backend server is running.');
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const handleCalculate = async () => {
    if (inputs.length === 0) {
      alert('Please add at least one sector with spending amount');
      return;
    }

    setCalculating(true);

    try {
      const result = await apiClient.calculate(inputs);
      setResults(result);
    } catch (error) {
      console.error('Calculation failed:', error);
      alert('Calculation failed. Please check your inputs and ensure the API is running.');
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
        <h1>Open DIO</h1>
        <p className="tagline">
          Defense Environmental Impact Analysis
        </p>
        <p className="subtitle">
          Using the Defense Input-Output Model v2.0
        </p>

        <nav className="nav-tabs">
          <button
            className={view === 'calculator' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => setView('calculator')}
          >
            Calculator
          </button>
          <button
            className={view === 'methodology' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => setView('methodology')}
          >
            Methodology
          </button>
          <button
            className={view === 'glossary' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => setView('glossary')}
          >
            Glossary
          </button>
        </nav>
      </header>

      <main className="main">
        <div className="container">
          {view === 'calculator' ? (
            <>
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
                />
              )}

              <footer className="footer">
                <p>
                  <strong>About:</strong> Open DIO makes military environmental
                  impact analysis accessible to researchers, journalists, and the public.
                </p>
                <p>
                  <strong>Data:</strong> Based on EPA's Defense Input-Output Model v2.0
                  | <strong>Method:</strong> Environmentally-Extended Input-Output Analysis
                </p>
                <p className="credit">
                  Open Source |{' '}
                  <a href="https://github.com/kelaxten/DIO-v3" target="_blank" rel="noopener noreferrer">
                    View on GitHub
                  </a>
                </p>
              </footer>
            </>
          ) : view === 'methodology' ? (
            <Methodology />
          ) : (
            <Glossary />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
