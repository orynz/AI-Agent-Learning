const fetchPost = async() => {
    // 서버에 데이터 요청 후 응답 대기
    const res = await fetch('http://jsonplaceholder.typicode.com/posts/1')
    const data = await res.json()
    console.log("가져온 데이터: ", data)
    console.log("제목: ", data.title)

}

fetchPost()


const fetchUser = () => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ name: "TOM", age: 20 })
        }, 1000)
    })
}

const run = async () => {
    const user = await fetchUser()
    console.log(user)
}

run()
