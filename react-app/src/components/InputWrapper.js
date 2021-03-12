import React, {useState } from 'react';
import { Form, Checkbox } from 'semantic-ui-react'
import SelectCollectionType from './SelectCollectionType'


function InputWrapper(props) {
  const [collectionType, setCollectionType] = useState('book');
  const [dataId, setDataId] = useState('-1');
  const operator = props.operator

  function executeGet() {

  }
  // updateID(event) {

  // }
  if (operator === 'GET'){
    return (
      <Form onSubmit={executeGet}>
        <Form.Field>
          <SelectCollectionType setCollectionType={setCollectionType}/>
          <h1>selected: {collectionType}</h1>
        </Form.Field>
        <Form.Field>
          <input type='number' onChange={(e) => setDataId(e.target.value)}></input>
          <h1>id is: {dataId}</h1>
        </Form.Field>
        <Form.Button content='Submit' />
       
      </Form>
    )
  }
  return (
    <h1>Other</h1>
  );
}

export default InputWrapper;

