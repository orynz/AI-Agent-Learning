const getStockAI= (price) => {
    return price > 100000 ? "매수알림" : "관망";
}


const addTax0 = (price) => {
    return price * 1.0;
}

// 중괄호 및 return 도 생략 가능
const addTax1 = price => price * 1.1;
const addTax2 = (price) => price * 1.2;

let price = 120000
console.log(getStockAI(price))
console.log(addTax0(price))
console.log(addTax1(price))
console.log(addTax2(price))