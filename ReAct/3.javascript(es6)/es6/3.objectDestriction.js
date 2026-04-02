const agent = {
    name:"금융봇",
    version:"2.0",
    skill:"재부분석",
}

// 객체명.변수명
console.log(agent.name)

const {name, skill}  = agent
console.log(`${name}의 주특기는 ${skill}입니다`)


const printAgent = ({name, skill, version}) => {
    console.log(`${version} 버전의 ${name} 주특기는 ${skill}입니다`)
}

printAgent(agent)

