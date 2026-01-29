import { useState, useMemo, useRef, useEffect } from 'react';
import type { Sector, SectorInput } from '../types';
import './SectorForm.css';

interface Props {
  sectors: Sector[];
  inputs: SectorInput[];
  onInputsChange: (inputs: SectorInput[]) => void;
  onCalculate: () => void;
  onReset: () => void;
  calculating: boolean;
}

export function SectorForm({
  sectors,
  inputs,
  onInputsChange,
  onCalculate,
  onReset,
  calculating,
}: Props) {
  const [selectedSector, setSelectedSector] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Sort sectors alphabetically
  const sortedSectors = useMemo(() => {
    return [...sectors].sort((a, b) => a.name.localeCompare(b.name));
  }, [sectors]);

  // Fuzzy search filter
  const filteredSectors = useMemo(() => {
    if (!searchQuery.trim()) return sortedSectors;

    const query = searchQuery.toLowerCase();
    return sortedSectors.filter(sector => {
      const name = sector.name.toLowerCase();
      const code = sector.code.toLowerCase();

      // Simple fuzzy matching: check if all characters appear in order
      let nameIndex = 0;
      for (const char of query) {
        nameIndex = name.indexOf(char, nameIndex);
        if (nameIndex === -1) break;
        nameIndex++;
      }

      // Match by name (fuzzy) or code (exact)
      return nameIndex !== -1 || code.includes(query);
    });
  }, [sortedSectors, searchQuery]);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectSector = (code: string, name: string) => {
    setSelectedSector(code);
    setSearchQuery(name);
    setIsDropdownOpen(false);
  };

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
    setSelectedSector('');
    setIsDropdownOpen(true);
  };

  const handleAddSector = () => {
    if (!selectedSector || !amount || parseFloat(amount) <= 0) {
      alert('Please select a sector and enter a valid amount');
      return;
    }

    const sector = sectors.find((s) => s.code === selectedSector);
    if (!sector) return;

    const newInput: SectorInput = {
      sectorCode: sector.code,
      sectorName: sector.name,
      amount: parseFloat(amount),
    };

    onInputsChange([...inputs, newInput]);
    setSelectedSector('');
    setSearchQuery('');
    setAmount('');
  };

  const handleRemoveSector = (index: number) => {
    onInputsChange(inputs.filter((_, i) => i !== index));
  };

  const handleCSVUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const lines = text.split('\n').filter(line => line.trim());

        if (lines.length < 2) {
          alert('CSV file must have at least a header row and one data row');
          return;
        }

        // Parse header
        const header = lines[0].toLowerCase().split(',').map(h => h.trim());
        const codeIndex = header.findIndex(h => h.includes('code') || h.includes('sector'));
        const amountIndex = header.findIndex(h => h.includes('amount') || h.includes('spending') || h.includes('dollar'));

        if (codeIndex === -1 || amountIndex === -1) {
          alert('CSV must have columns for sector code and amount\nExpected: code, amount\nOr: sector_code, spending_amount');
          return;
        }

        // Parse data rows
        const newInputs: SectorInput[] = [];
        const errors: string[] = [];

        for (let i = 1; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line) continue;

          const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
          const code = values[codeIndex];
          const amountStr = values[amountIndex];

          if (!code || !amountStr) continue;

          // Find sector
          const sector = sectors.find(s => s.code === code);
          if (!sector) {
            errors.push(`Line ${i + 1}: Unknown sector code "${code}"`);
            continue;
          }

          // Parse amount
          const amount = parseFloat(amountStr.replace(/[,$]/g, ''));
          if (isNaN(amount) || amount <= 0) {
            errors.push(`Line ${i + 1}: Invalid amount "${amountStr}"`);
            continue;
          }

          newInputs.push({
            sectorCode: sector.code,
            sectorName: sector.name,
            amount: amount
          });
        }

        if (newInputs.length === 0) {
          alert('No valid data found in CSV file\n\n' + errors.join('\n'));
          return;
        }

        // Add to existing inputs
        onInputsChange([...inputs, ...newInputs]);

        // Show summary
        let message = `Successfully imported ${newInputs.length} sector(s)`;
        if (errors.length > 0) {
          message += `\n\n${errors.length} error(s):\n${errors.slice(0, 5).join('\n')}`;
          if (errors.length > 5) {
            message += `\n... and ${errors.length - 5} more`;
          }
        }
        alert(message);

        // Reset file input
        event.target.value = '';
      } catch (error) {
        console.error('CSV parsing error:', error);
        alert('Error parsing CSV file. Please check the format.');
      }
    };

    reader.readAsText(file);
  };

  const downloadCSVTemplate = () => {
    const template = 'sector_code,amount,description\n336411,80000000000,F-35 Program\n336414,12000000000,Guided Missiles\n541330,500000000,Engineering Services';
    const blob = new Blob([template], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dio_template.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const totalSpending = inputs.reduce((sum, input) => sum + input.amount, 0);

  return (
    <div className="sector-form">
      <h2>Input Defense Spending</h2>
      <p className="form-description">
        Select defense sectors and enter spending amounts to calculate environmental impacts.
      </p>

      <div className="input-section">
        <div className="input-method-tabs">
          <h3>Add Sectors</h3>
        </div>

        <div className="form-row">
          <div className="form-group" ref={dropdownRef}>
            <label htmlFor="sector-search">Defense Sector</label>
            <input
              id="sector-search"
              type="text"
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              onFocus={() => setIsDropdownOpen(true)}
              placeholder="Search sectors..."
              className="sector-search-input"
              autoComplete="off"
            />
            {isDropdownOpen && filteredSectors.length > 0 && (
              <div className="sector-dropdown">
                {filteredSectors.slice(0, 100).map((sector) => (
                  <div
                    key={sector.code}
                    className={`sector-option ${selectedSector === sector.code ? 'selected' : ''}`}
                    onClick={() => handleSelectSector(sector.code, sector.name)}
                  >
                    <div className="sector-option-name">{sector.name}</div>
                    <div className="sector-option-code">{sector.code}</div>
                  </div>
                ))}
                {filteredSectors.length > 100 && (
                  <div className="sector-option-info">
                    Showing first 100 of {filteredSectors.length} matches. Refine your search.
                  </div>
                )}
              </div>
            )}
            {isDropdownOpen && filteredSectors.length === 0 && searchQuery && (
              <div className="sector-dropdown">
                <div className="sector-option-info">No sectors found matching "{searchQuery}"</div>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="amount-input">Spending Amount (USD)</label>
            <input
              id="amount-input"
              type="number"
              min="0"
              step="1000000"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="e.g., 1000000000"
              className="amount-input"
            />
          </div>

          <button
            onClick={handleAddSector}
            className="btn btn-add"
            disabled={!selectedSector || !amount}
          >
            Add Sector
          </button>
        </div>

        <div className="csv-upload-section">
          <div className="divider">
            <span>or</span>
          </div>
          <div className="csv-upload-box">
            <label htmlFor="csv-upload" className="csv-upload-label">
              <span className="csv-icon">📄</span>
              <span className="csv-text">Upload CSV File</span>
              <span className="csv-hint">Bulk import sectors and amounts</span>
            </label>
            <input
              id="csv-upload"
              type="file"
              accept=".csv"
              onChange={handleCSVUpload}
              style={{ display: 'none' }}
            />
            <button onClick={downloadCSVTemplate} className="btn btn-link">
              Download Template
            </button>
          </div>
        </div>

        {inputs.length > 0 && (
          <div className="inputs-list">
            <h3>Added Sectors ({inputs.length})</h3>
            <div className="inputs-table">
              {inputs.map((input, index) => (
                <div key={index} className="input-row">
                  <div className="input-info">
                    <span className="input-name">{input.sectorName}</span>
                    <span className="input-amount">
                      ${input.amount.toLocaleString()}
                    </span>
                  </div>
                  <button
                    onClick={() => handleRemoveSector(index)}
                    className="btn-remove"
                    title="Remove"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>

            <div className="total-spending">
              <strong>Total Spending:</strong> ${totalSpending.toLocaleString()}
            </div>
          </div>
        )}

        <div className="action-buttons">
          <button
            onClick={onCalculate}
            disabled={inputs.length === 0 || calculating}
            className="btn btn-primary btn-lg"
          >
            {calculating ? 'Calculating...' : 'Calculate Impacts'}
          </button>

          {inputs.length > 0 && (
            <button onClick={onReset} className="btn btn-secondary">
              Clear All
            </button>
          )}
        </div>
      </div>

      <div className="example-box">
        <h4>Example Scenarios</h4>
        <p>Try these example spending amounts:</p>
        <ul>
          <li>F-35 Fighter Jet Program: $80,000,000,000</li>
          <li>Aircraft Carrier: $13,000,000,000</li>
          <li>Cybersecurity Contract: $500,000,000</li>
          <li>Base Construction: $1,000,000,000</li>
        </ul>
      </div>
    </div>
  );
}
