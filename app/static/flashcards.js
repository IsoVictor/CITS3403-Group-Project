// flashcards.js
const flashcardSetList = document.getElementById('flashcard-set-list');
const flashcardSetForm = document.getElementById('flashcard-set-form');
const flashcardForm = document.getElementById('flashcard-form');
const flashcard = document.getElementById('flashcard');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

let flashcardSets = [];
let currentSetIndex = 0;
let currentFlashcardIndex = 0;

function renderFlashcardSetList() {
    flashcardSetList.innerHTML = '';
    flashcardSets.forEach((set, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = set.name;
        listItem.addEventListener('click', () => {
            currentSetIndex = index;
            currentFlashcardIndex = 0;
            renderFlashcard();
        });
        flashcardSetList.appendChild(listItem);
    });
}

function renderFlashcard() {
    const set = flashcardSets[currentSetIndex];
    if (set && set.flashcards.length > 0) {
        const card = set.flashcards[currentFlashcardIndex];
        flashcard.innerHTML = `
            <div class="flashcard-front">
                <p>${card.question}</p>
            </div>
            <div class="flashcard-back">
                <p>${card.answer}</p>
            </div>
        `;
    } else {
        flashcard.innerHTML = '';
    }
}

function nextFlashcard() {
    const set = flashcardSets[currentSetIndex];
    if (set) {
        currentFlashcardIndex = (currentFlashcardIndex + 1) % set.flashcards.length;
        renderFlashcard();
    }
}

function prevFlashcard() {
    const set = flashcardSets[currentSetIndex];
    if (set) {
        currentFlashcardIndex = (currentFlashcardIndex - 1 + set.flashcards.length) % set.flashcards.length;
        renderFlashcard();
    }
}

async function fetchFlashcardSets() {
    try {
        const response = await fetch('/flashcard-sets');
        const data = await response.json();
        flashcardSets = data.flashcard_sets;
        renderFlashcardSetList();
    } catch (error) {
        console.error('Error fetching flashcard sets:', error);
    }
}

async function createFlashcardSet(name) {
    try {
        const response = await fetch('/flashcard-sets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating flashcard set:', error);
    }
}

async function createFlashcard(setId, question, answer) {
    try {
        const response = await fetch('/flashcards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ setId, question, answer })
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating flashcard:', error);
    }
}

flashcardSetForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const setName = document.getElementById('set-name').value;
    const set = await createFlashcardSet(setName);
    if (set) {
        flashcardSets.push(set);
        flashcardSetForm.reset();
        renderFlashcardSetList();
    }
});

flashcardForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const setId = flashcardSets[currentSetIndex].id;
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const flashcard = await createFlashcard(setId, question, answer);
    if (flashcard) {
        flashcardSets[currentSetIndex].flashcards.push(flashcard);
        flashcardForm.reset();
    }
});

flashcard.addEventListener('click', () => {
    flashcard.classList.toggle('flipped');
});

nextBtn.addEventListener('click', nextFlashcard);
prevBtn.addEventListener('click', prevFlashcard);

fetchFlashcardSets();
