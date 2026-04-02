import { useState } from 'react'
import './App.css'
import Test from './components/Test'

// 컴포넌트는 App 바깥에 잘 두셨습니다!
function Button() {
  const handleClick = () => {
    alert('Button clicked!');
  };
  return <button onClick={handleClick}>Click me</button>;
}

function App() {
  const [count, setCount] = useState(0)

  let pStyle = {
    color: 'red',
    backgroundColor: 'black',
  }

  const isTest = true
  let msg;
  if (isTest) {
    msg = <p>"테스트 중입니다."</p>
  } else {
    msg = <p>"서비스 중입니다." </p>
  }
  const   num = 1
  return (
    <div>
      <h2 className='App-color'>첫 번째 방식으로 react 작성중</h2>
      <Test />
      <p style={pStyle}>스타일 적용 예제 1</p>
      <p className='App-title'>스타일 적용 예제 2</p>
      <p>1 = 1 ? {num === 1 ? '참' : '거짓'}</p>
      <button onClick={() => setCount(count + 1)}>클릭 횟수: {count}</button>
      {msg}
      <Button />
    </div>
  )
}

export default App
