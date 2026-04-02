// async 기본구조
const getData = async () => {
    return "데이터"
}

getData().then(res => console.log(res))

// await 기본구
const delay = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms))
}

const run = async() => {
    console.log("시작")
    await delay(1000)
    console.log("1초후 실행")
}

run()


const analyeStock = new Promise((resolve, reject) => {
    const success = true
    if (success) {
        resolve("분석이 잘 처리되었습니다.")
        return "100"
    } else {
        resolve("서버 연결 실패...")
    }
})

analyeStock.then(res => console.log(res))


