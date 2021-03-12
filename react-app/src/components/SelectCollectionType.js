import React, {  } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';


function SelectCollectionType(props) {
    let setCollectionType = props.setCollectionType
//   const [activeOperator, setActiveOperator] = useState('GET');
  return (
      <div>
        <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                book or author
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.Item onClick={()=>setCollectionType('book')}>Book</Dropdown.Item>
                <Dropdown.Item onClick={()=>setCollectionType('author')}>Author</Dropdown.Item>
            </Dropdown.Menu>
        </Dropdown>

        {/* <InputWrapper operator={activeOperator}/> */}
    </div>
  );
}

export default SelectCollectionType;
