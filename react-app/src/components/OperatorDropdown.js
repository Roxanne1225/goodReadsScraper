import React, { useState } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import InputWrapper from './InputWrapper'
import "./InContainer.css"

function OperatorDropdown() {

  const [activeOperator, setActiveOperator] = useState('GET');
  return (
      <div class='in'>
        <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                Dropdown Button
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.Item onClick={()=>setActiveOperator('GET')}>GET</Dropdown.Item>
                <Dropdown.Item onClick={()=>setActiveOperator('SEARCH')}>SEARCH</Dropdown.Item>
            </Dropdown.Menu>
        </Dropdown>

        <InputWrapper operator={activeOperator}/>
    </div>
  );
}

export default OperatorDropdown;
