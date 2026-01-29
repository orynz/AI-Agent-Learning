// 전역 변수 선언
let itemCounter = 0; // 고유 ID 생성용 카운터
let todoItems = [];  // 할 일 데이터 저장소
const inputItem = document.getElementById("inputItem"); // 입력 필드
const addBtn = document.getElementById("addBtn");       // 추가 버튼
const todoList = document.getElementById("todo-list");  // 할 일 목록 컨테이너

// 로컬 스토리지에서 데이터 복원
window.addEventListener('load', () => {
    const savedItems = localStorage.getItem('todoItems');
    if (savedItems) {
        todoItems = JSON.parse(savedItems);
        todoItems.forEach(item => {
            addItemToDOM(item);
        });
        itemCounter = todoItems.length;
    }
});

// 할 일 추가 함수
function addItem() {
    const value = inputItem.value.trim();
    if (!value) return alert("할 일을 입력하세요.");
    
    // 데이터 배열에 추가
    todoItems.push({
        id: itemCounter, // 고유 ID 할당
        title: value,
        done: false        // 완료 상태
    });
    
    // DOM에 추가
    addItemToDOM(todoItems[itemCounter++]);
    
    // 입력 필드 초기화
    inputItem.value = '';
    inputItem.focus();
    saveData(); // 데이터 저장
}

// DOM에 항목 추가하는 함수
function addItemToDOM(item) {
    const li = document.createElement('li');
    li.className = 'todo-item';
    
    const checkBox = document.createElement('input');
    checkBox.type = 'checkbox';
    checkBox.id = `item-${item.id}`;
    checkBox.checked = item.done;
    
    const itemLabel = document.createElement('label');
    itemLabel.setAttribute('for', checkBox.id);
    itemLabel.textContent = item.title;
    itemLabel.className = 'label-item';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = '삭제';
    deleteBtn.dataset.id = item.id;
    deleteBtn.className = "delete-btn";
    
    li.appendChild(checkBox);
    li.appendChild(itemLabel);
    li.appendChild(deleteBtn);
    todoList.appendChild(li);
}

// 추가 버튼 클릭 이벤트
addBtn.addEventListener('click', addItem);

// 엔터 키로 추가 기능
inputItem.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') addItem();
});

// 체크박스 상태 변경 이벤트
todoList.addEventListener('change', function(e) {
    if (e.target.type === 'checkbox') {
        const index = parseInt(e.target.id.split('-')[1]);
        todoItems[index].done = e.target.checked;
        saveData();
    }
});

// 삭제 기능 이벤트 리스너
todoList.addEventListener('click', function(e) {
    if (e.target.className === 'delete-btn') {
        const id = parseInt(e.target.dataset.id);

        // 배열에서 해당 ID를 가진 아이템의 '진짜 인덱스' 찾기
        const idx = todoItems.findIndex(item => item.id === id);

        if (idx > -1 && idx < todoItems.length) {
            // 배열에서 항목 제거
            todoItems.splice(idx, 1);
            itemCounter--;
            
            // DOM에서 항목 제거
            e.target.parentElement.remove();
            
            saveData();
        }
    }
});

// 데이터 저장 함수
function saveData() {
    localStorage.setItem('todoItems', JSON.stringify(todoItems));
}


