import { useState } from 'react';
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
    setAmount('');
  };

  const handleRemoveSector = (index: number) => {
    onInputsChange(inputs.filter((_, i) => i !== index));
  };

  const totalSpending = inputs.reduce((sum, input) => sum + input.amount, 0);

  return (
    <div className="sector-form">
      <h2>📊 Input Defense Spending</h2>
      <p className="form-description">
        Select defense sectors and enter spending amounts to calculate environmental impacts.
      </p>

      <div className="input-section">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="sector-select">Defense Sector</label>
            <select
              id="sector-select"
              value={selectedSector}
              onChange={(e) => setSelectedSector(e.target.value)}
              className="sector-select"
            >
              <option value="">-- Select a sector --</option>
              {sectors.map((sector) => (
                <option key={sector.code} value={sector.code}>
                  {sector.name} ({sector.category})
                </option>
              ))}
            </select>
            {selectedSector && (
              <p className="sector-description">
                {sectors.find((s) => s.code === selectedSector)?.description}
              </p>
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
            + Add Sector
          </button>
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
                    ✕
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
            {calculating ? '⚙️ Calculating...' : '🔍 Calculate Impacts'}
          </button>

          {inputs.length > 0 && (
            <button onClick={onReset} className="btn btn-secondary">
              Clear All
            </button>
          )}
        </div>
      </div>

      <div className="example-box">
        <h4>💡 Example Scenarios</h4>
        <p>Try these example spending amounts:</p>
        <ul>
          <li>F-35 Fighter Jet Program: $80,000,000,000 (Aircraft Manufacturing)</li>
          <li>Aircraft Carrier: $13,000,000,000 (Ship Building)</li>
          <li>Cybersecurity Contract: $500,000,000 (Computer Systems Design)</li>
          <li>Base Construction: $1,000,000,000 (Heavy Construction)</li>
        </ul>
      </div>
    </div>
  );
}
