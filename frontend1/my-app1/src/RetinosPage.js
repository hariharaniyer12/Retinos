import React from 'react';
import { FaEye } from 'react-icons/fa';
import './styles.css';

function RetinosPage() {
  return (
    <div className="retinos-container">
      <div className="retinos-header">
        <FaEye />
        <h1>RETINOS</h1>
      </div>
      <div className="retinos-content">
        {/* Add content here */}
      </div>
    </div>
  );
}

export default RetinosPage;