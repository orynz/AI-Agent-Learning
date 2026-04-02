const stocks = [
    {name:"삼성", price:70000},
    {name:"LG", price:800000},
    {name:"기아", price:260580},
]

const expensiveStocks = stocks.filter(stock => stock.price >= 150000)
console.log(expensiveStocks)

const result = stocks.filter(stock => stock.price >= 150000).map(stock => stock.name)
console.log(result)