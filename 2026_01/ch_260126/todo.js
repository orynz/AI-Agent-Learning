// 요소 참조
const input = document.getElementById('newTask');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');

// 할 일 추가 함수
function addTask() {
    const taskText = input.value.trim();
    if (taskText === '') return;

    // li 요소 생성
    const li = document.createElement('li');
    li.textContent = taskText;

    // 삭제 버튼 생성
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = '삭제';
    deleteBtn.className = 'delete-btn';

    // li에 버튼 추가
    li.appendChild(deleteBtn);

    // todoList에 추가
    todoList.appendChild(li);

    // 입력 필드 초기화
    input.value = '';
    input.focus();
}

// 엔터 키로 추가 기능
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTask();
    }
});

// 버튼 클릭 이벤트
addBtn.addEventListener('click', addTask);

// 이벤트 위임을 통한 삭제 기능
todoList.addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn')) {
        e.target.parentElement.remove();
    }
});
