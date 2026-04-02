// 기존의 배열의 요소로 새로운 배열을 생성
const itemArray = [1, 2, 3]

const newItemArray = [...itemArray]
console.log(newItemArray)


const doubleItemArray = itemArray.map(price => price * 2)

console.log(doubleItemArray)

const users = [
    {name:"TOM", age:20},
    {name:"Jane", age:30}
]


const newUsers = users.map( (user) => ({
    ...user,
    isAdult: user.age >= 20,
    name: user.name==="TOM" ? "Tom": user.name
}));

console.log(newUsers)