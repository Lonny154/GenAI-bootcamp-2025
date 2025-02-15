// Fetch and display vocabulary
async function loadVocabulary() {
    const response = await fetch('/vocabulary');
    const vocabulary = await response.json();
    const vocabularyList = document.getElementById('vocabularyList');
    vocabularyList.innerHTML = '';
    
    vocabulary.forEach(word => {
        const item = document.createElement('a');
        item.className = 'list-group-item list-group-item-action';
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${word.word}</h6>
                <small>${word.language}</small>
            </div>
            <p class="mb-1 meaning" style="display: none;">${word.meaning}</p>
            <div class="d-flex justify-content-between align-items-center">
                <small>Difficulty Level: ${word.difficulty_level}</small>
                <button class="btn btn-sm btn-outline-primary show-meaning-btn">Show Meaning</button>
            </div>
        `;
        
        // Add click handler for the show meaning button
        const showMeaningBtn = item.querySelector('.show-meaning-btn');
        const meaningText = item.querySelector('.meaning');
        showMeaningBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const isHidden = meaningText.style.display === 'none';
            meaningText.style.display = isHidden ? 'block' : 'none';
            showMeaningBtn.textContent = isHidden ? 'Hide Meaning' : 'Show Meaning';
        });
        
        vocabularyList.appendChild(item);
    });
}

// Fetch and display learning apps
async function loadApps() {
    const response = await fetch('/apps');
    const apps = await response.json();
    const appsContainer = document.getElementById('appsContainer');
    appsContainer.innerHTML = '';
    
    apps.forEach(app => {
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-4';
        col.innerHTML = `
            <div class="card app-card h-100">
                <div class="card-body text-center">
                    <img src="${app.icon || 'https://via.placeholder.com/64'}" alt="${app.name}" style="width: 64px; height: 64px;">
                    <h5 class="card-title mt-3">${app.name}</h5>
                    <p class="card-text">${app.description}</p>
                    <a href="${app.url}" class="btn btn-primary" target="_blank">Launch App</a>
                </div>
            </div>
        `;
        appsContainer.appendChild(col);
    });
}

// Update learning statistics
async function updateStats() {
    // This would typically fetch from the server
    const response = await fetch('/stats');
    const stats = await response.json();
    
    document.getElementById('correctCount').textContent = stats.correct || 0;
    document.getElementById('wrongCount').textContent = stats.wrong || 0;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadVocabulary();
    loadApps();
    updateStats();
    
    // Search functionality
    const searchInput = document.getElementById('vocabularySearch');
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const items = document.querySelectorAll('#vocabularyList .list-group-item');
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
});
