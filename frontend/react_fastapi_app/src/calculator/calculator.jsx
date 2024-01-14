import React, { useState } from 'react';
import "./calculator.css"

const Calculator = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [detail, setDetail] = useState('');

  const handleButtonClick = (value) => {
    if (value === '=') {
      try {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: input.toString() })
        };
        fetch('http://localhost:8000/rpn_databse/', requestOptions)
            .then(response => response.json())
            .then(data => {setResult(data.response);setDetail(data.message)});
      } catch (error) {
        setResult('Error');
      }
    } else if (value === 'C') {
      setInput('');
      setResult('');
    }else if (value.toUpperCase() === 'CSV'){
        try {
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            };
            fetch('http://localhost:8000/csv/', requestOptions)
                .then(response => response.json())
                .then(data => {setDetail(data.message)});
          } catch (error) {
            setResult('Error');
          }
    } 
    else {
      setInput((prevInput) => prevInput + value);
    }
  };

  return (
    <div className="calculator">
      <div className="display">
        <div className="concept">you should seperate each value by space: "24 31 *"</div>
        <input type="text" value={input} readOnly />
        <div className="result">{result}</div>
      </div>
      <div className="buttons">
        <button onClick={() => handleButtonClick('1')}>1</button>
        <button onClick={() => handleButtonClick('2')}>2</button>
        <button onClick={() => handleButtonClick('3')}>3</button>
        <button onClick={() => handleButtonClick('+')}>+</button>

        <button onClick={() => handleButtonClick('4')}>4</button>
        <button onClick={() => handleButtonClick('5')}>5</button>
        <button onClick={() => handleButtonClick('6')}>6</button>
        <button onClick={() => handleButtonClick('-')}>-</button>

        <button onClick={() => handleButtonClick('7')}>7</button>
        <button onClick={() => handleButtonClick('8')}>8</button>
        <button onClick={() => handleButtonClick('9')}>9</button>
        <button onClick={() => handleButtonClick('*')}>*</button>

        <button onClick={() => handleButtonClick('0')}>0</button>
        <button onClick={() => handleButtonClick('.')}>.</button>
        <button onClick={() => handleButtonClick('=')}>=</button>
        <button onClick={() => handleButtonClick('/')}>/</button>

        <button onClick={() => handleButtonClick('C')}>C</button>
        <button onClick={() => handleButtonClick(' ')}>Space</button>
        <button onClick={() => handleButtonClick("csv")}>CSV</button>
      </div>
      <div className="display">
        <div className="detail">{detail}</div>
      </div>
    </div>
  );
};

export default Calculator;
