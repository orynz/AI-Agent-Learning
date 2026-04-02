const agents = [
    { name: "GPT", skill: "대화", version: "5.3" },
    { name: "VisionAI", skill: "이미지 분석", version: "2.1" },
    { name: "CodeBot", skill: "코드 생성", version: "1.8" }
]

const printAgent = ({name, skill, version}) => {
    console.log(`${version} 버전의 ${name} 주특기는 ${skill}입니다`)
}

agents.forEach(printAgent)


const printAgent1 = ({name, skill, version = "unknown"}) => {
    console.log(`${version} 버전의 ${name} 주특기는 ${skill}입니다`)
}

printAgent1({ name: "MiniBot", skill: "요약" })
