// flashcards.js
const flashcardContainer = document.getElementById('flashcard-container');
const flashcardForm = document.getElementById('flashcard-form');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

let flashcards = [];
let currentIndex = 0;

function createFlashcard(question, answer) {
    const flashcardElement = document.createElement('div');
    flashcardElement.classList.add('flashcard');
    flashcardElement.innerHTML = `
        <div class="flashcard-inner">
            <div class="flashcard-front">
                <p>${question}</p>
            </div>
            <div class="flashcard-back">
                <p>${answer}</p>
            </div>
        </div>
    `;
    flashcardElement.addEventListener('click', () => {
        flashcardElement.classList.toggle('flipped');
    });
    return flashcardElement;
}

function displayFlashcard(index) {
    flashcardContainer.innerHTML = '';
    flashcardContainer.appendChild(flashcards[index]);
}

function nextFlashcard() {
    currentIndex = (currentIndex + 1) % flashcards.length;
    displayFlashcard(currentIndex);
}

function prevFlashcard() {
    currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
    displayFlashcard(currentIndex);
}

flashcardForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    const flashcard = createFlashcard(question, answer);
    flashcards.push(flashcard);
    flashcardForm.reset();
});

nextBtn.addEventListener('click', nextFlashcard);
prevBtn.addEventListener('click', prevFlashcard);
