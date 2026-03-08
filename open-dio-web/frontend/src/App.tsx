import { useState, useEffect } from 'react';
import './App.css';
import { apiClient } from './services/api';
import type { SectorInput, CalculationResult, Sector } from './types';
import { SectorForm } from './components/SectorForm';
import { ResultsDashboard } from './components/ResultsDashboard';
import Methodology from './components/Methodology';
import Glossary from './components/Glossary';
import ResearchContext from './components/ResearchContext';

type View = 'calculator' | 'research' | 'methodology' | 'glossary';

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
        // Set loading false to show app, but with degraded state
        setLoading(false);
        // Note: Sectors may be empty, calculator will show appropriate message
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
          Full Supply Chain Environmental Assessment of U.S. Military Spending
        </p>
        <p className="subtitle">
          Revealing that procurement emissions are 2.5× larger than operational estimates
        </p>

        <nav className="nav-tabs">
          <button
            className={view === 'calculator' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => setView('calculator')}
          >
            Calculator
          </button>
          <button
            className={view === 'research' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => setView('research')}
          >
            Research Context
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
                  <strong>About:</strong> Open DIO is an open-source research tool for full supply chain
                  environmental assessment of military spending. First publicly accessible defense IO-LCA
                  calculator, revealing procurement emissions are 2.5× operational estimates.
                </p>
                <p>
                  <strong>Research:</strong> Methodological proof-of-concept demonstrating feasibility
                  of environmentally-extended input-output analysis for defense sector. See Research Context
                  tab for limitations, validation, and dissertation vision.
                </p>
                <p>
                  <strong>Data:</strong> USAspending.gov, Cornerstone v1.4.0 (GHG), EIA MECS 2018 (Energy),
                  EPA USEEIO v2.0 (Water, Land) | <strong>BEA Data:</strong> 2012 Input-Output tables
                </p>
                <p className="credit">
                  Open Source |{' '}
                  <a href="https://github.com/kelaxten/DIO-v3" target="_blank" rel="noopener noreferrer">
                    View on GitHub
                  </a>{' '}
                  | <a href="/data/fy2024_dod_line_by_line.csv" download>
                    Download Dataset
                  </a>
                </p>
              </footer>
            </>
          ) : view === 'research' ? (
            <ResearchContext />
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
