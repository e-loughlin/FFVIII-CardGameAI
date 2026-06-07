document.addEventListener('DOMContentLoaded', () => {
    const setupView = document.getElementById('setup-view');
    const gameView = document.getElementById('game-view');
    const playerInputs = document.getElementById('player-card-inputs');
    const opponentInputs = document.getElementById('opponent-card-inputs');
    const statusBar = document.getElementById('status-bar');
    const turnIndicator = document.getElementById('turn-indicator');
    const scoreIndicator = document.getElementById('score-indicator');
    const boardCells = document.querySelectorAll('.board-cell');
    const playerHand = document.getElementById('player-hand');
    const opponentHand = document.getElementById('opponent-hand');
    const askAiBtn = document.getElementById('ask-ai-btn');
    const applyAiBtn = document.getElementById('apply-ai-btn');
    const aiRecommendation = document.getElementById('ai-recommendation');
    const gameOverControls = document.getElementById('game-over-controls');
    const winnerText = document.getElementById('winner-text');
    const aiControls = document.getElementById('ai-controls');

    let selectedCard = null;
    let recommendedMove = null;

    // Populate Setup Inputs
    function createInputRow(owner, index) {
        const cardDiv = document.createElement('div');
        cardDiv.className = `setup-card-input ${owner}`;
        cardDiv.innerHTML = `
            <div class="setup-card-inner">
                <input type="text" class="sym" value="${owner}${index+1}" placeholder="Sym">
                <div class="setup-values">
                    <input type="text" class="top" value="5" maxlength="1">
                    <input type="text" class="left" value="5" maxlength="1">
                    <input type="text" class="right" value="5" maxlength="1">
                    <input type="text" class="bottom" value="5" maxlength="1">
                </div>
                <div class="setup-label">${owner === 'P' ? 'Player' : 'Opponent'} ${index+1}</div>
            </div>
        `;

        // Add validation and auto-select to inputs
        cardDiv.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', () => input.select());
            
            if (input.classList.contains('sym')) return;

            // Auto-tab and validation
            input.addEventListener('input', (e) => {
                let val = input.value.toUpperCase();
                if (val === 'A' || (parseInt(val) >= 1 && parseInt(val) <= 9)) {
                    input.value = val;
                    
                    // Find next input in sequence
                    const allValueInputs = Array.from(document.querySelectorAll('.setup-values input'));
                    const currentIndex = allValueInputs.indexOf(input);
                    if (currentIndex < allValueInputs.length - 1) {
                        allValueInputs[currentIndex + 1].focus();
                    }
                } else if (val !== '') {
                    input.value = ''; // Clear invalid immediately
                }
            });
        });

        return cardDiv;
    }

    for (let i = 0; i < 5; i++) {
        playerInputs.appendChild(createInputRow('P', i));
        opponentInputs.appendChild(createInputRow('O', i));
    }

    // API Helpers
    async function apiPost(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    }

    async function apiGet(url) {
        const res = await fetch(url);
        return res.json();
    }

    // State Rendering
    function renderCard(cardData) {
        if (!cardData) return '';
        const formatVal = (v) => v === 10 ? 'A' : v;
        const icon = cardData.symbol.charAt(0); // Use first letter as a simple icon
        return `
            <div class="card ${cardData.owner}" data-symbol="${cardData.symbol}">
                <div class="card-image">${icon}</div>
                <div class="card-values">
                    <div class="val-top">${formatVal(cardData.top)}</div>
                    <div class="val-left">${formatVal(cardData.left)}</div>
                    <div class="val-right">${formatVal(cardData.right)}</div>
                    <div class="val-bottom">${formatVal(cardData.bottom)}</div>
                </div>
                <div class="card-symbol">${cardData.symbol}</div>
            </div>
        `;
    }

    function updateUI(state) {
        // Board
        boardCells.forEach(cell => {
            const pos = cell.dataset.pos;
            cell.innerHTML = renderCard(state.board[pos]);
            cell.classList.remove('highlight');
        });

        // Hands
        playerHand.innerHTML = state.hands.P.map(renderCard).join('');
        opponentHand.innerHTML = state.hands.O.map(renderCard).join('');

        // Status
        statusBar.classList.remove('hidden');
        turnIndicator.textContent = `Turn: ${state.current_player === 'P' ? 'Player (Blue)' : 'Opponent (Red)'}`;
        scoreIndicator.textContent = `Score: P=${state.points.P} O=${state.points.O}`;

        // Game Over
        if (state.game_over) {
            gameView.classList.add('game-over');
            aiControls.classList.add('hidden');
            gameOverControls.classList.remove('hidden');
            winnerText.textContent = state.points.P > state.points.O ? 'Player Wins!' : (state.points.P < state.points.O ? 'Opponent Wins!' : 'Draw!');
        } else {
            aiControls.classList.remove('hidden');
            gameOverControls.classList.add('hidden');
        }

        // Reset Selection & AI
        selectedCard = null;
        recommendedMove = null;
        aiRecommendation.textContent = '';
        applyAiBtn.classList.add('hidden');
        document.getElementById('ai-all-moves').classList.add('hidden');
        document.getElementById('moves-list').innerHTML = '';
        
        // Remove selection glow from all cards
        document.querySelectorAll('.card').forEach(c => c.classList.remove('selected', 'recommended'));
    }

    // Event Delegation for Hands
    [playerHand, opponentHand].forEach(hand => {
        hand.addEventListener('click', (e) => {
            const cardEl = e.target.closest('.card');
            if (cardEl) {
                document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
                cardEl.classList.add('selected');
                selectedCard = {
                    symbol: cardEl.dataset.symbol,
                    owner: cardEl.classList.contains('P') ? 'P' : 'O'
                };
            }
        });
    });

    // Event Delegation for Board
    document.getElementById('board').addEventListener('click', async (e) => {
        const cell = e.target.closest('.board-cell');
        if (cell && selectedCard && !cell.querySelector('.card')) {
            const pos = cell.dataset.pos;
            const newState = await apiPost('/api/move', {
                symbol: selectedCard.symbol,
                position: pos
            });
            updateUI(newState);
        }
    });

    async function startGame(isDefault = false) {
        let payload;
        if (isDefault) {
            payload = { load_default: true };
        } else {
            const cards = [];
            const parseVal = (v) => v.toUpperCase() === 'A' ? 10 : parseInt(v);
            
            const getInputs = (container, owner) => {
                container.querySelectorAll('.setup-card-input').forEach(cardEl => {
                    cards.push({
                        symbol: cardEl.querySelector('.sym').value,
                        top: parseVal(cardEl.querySelector('.top').value),
                        left: parseVal(cardEl.querySelector('.left').value),
                        right: parseVal(cardEl.querySelector('.right').value),
                        bottom: parseVal(cardEl.querySelector('.bottom').value),
                        owner: owner
                    });
                });
            };
            getInputs(playerInputs, 'P');
            getInputs(opponentInputs, 'O');

            payload = {
                load_default: false,
                current_player: document.getElementById('start-player').value,
                cards: cards
            };
        }

        const state = await apiPost('/api/init', payload);
        setupView.classList.add('hidden');
        gameView.classList.remove('hidden');
        updateUI(state);
    }

    function getSetupData() {
        const cards = [];
        const getInputs = (container, owner) => {
            container.querySelectorAll('.setup-card-input').forEach(cardEl => {
                cards.push({
                    symbol: cardEl.querySelector('.sym').value,
                    top: cardEl.querySelector('.top').value,
                    left: cardEl.querySelector('.left').value,
                    right: cardEl.querySelector('.right').value,
                    bottom: cardEl.querySelector('.bottom').value,
                    owner: owner
                });
            });
        };
        getInputs(playerInputs, 'P');
        getInputs(opponentInputs, 'O');
        return {
            cards: cards,
            startPlayer: document.getElementById('start-player').value
        };
    }

    function applySetupData(data) {
        if (!data || !data.cards) return;
        
        const setInputs = (container, ownerCards) => {
            container.querySelectorAll('.setup-card-input').forEach((cardEl, i) => {
                const card = ownerCards[i];
                if (card) {
                    cardEl.querySelector('.sym').value = card.symbol;
                    cardEl.querySelector('.top').value = card.top;
                    cardEl.querySelector('.left').value = card.left;
                    cardEl.querySelector('.right').value = card.right;
                    cardEl.querySelector('.bottom').value = card.bottom;
                }
            });
        };

        const pCards = data.cards.filter(c => c.owner === 'P');
        const oCards = data.cards.filter(c => c.owner === 'O');
        setInputs(playerInputs, pCards);
        setInputs(opponentInputs, oCards);
        document.getElementById('start-player').value = data.startPlayer;
    }

    // Event Listeners
    document.getElementById('export-setup-btn').addEventListener('click', () => {
        const data = getSetupData();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `tt_setup_${new Date().getTime()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    });

    document.getElementById('import-setup-btn').addEventListener('click', () => {
        document.getElementById('import-file-input').click();
    });

    document.getElementById('import-file-input').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                applySetupData(data);
                e.target.value = ''; // Reset input
            } catch (err) {
                alert('Error parsing setup file.');
            }
        };
        reader.readAsText(file);
    });

    document.getElementById('load-default-btn').addEventListener('click', () => startGame(true));

    document.getElementById('start-game-btn').addEventListener('click', () => startGame(false));

    document.getElementById('reset-game-btn').addEventListener('click', () => startGame(false));

    document.getElementById('undo-btn').addEventListener('click', async () => {
        const state = await apiPost('/api/undo', {});
        updateUI(state);
    });

    document.getElementById('redo-btn').addEventListener('click', async () => {
        const state = await apiPost('/api/redo', {});
        updateUI(state);
    });

    document.getElementById('back-home-btn').addEventListener('click', () => {
        gameView.classList.add('hidden');
        setupView.classList.remove('hidden');
        statusBar.classList.add('hidden');
    });

    document.getElementById('new-game-btn').addEventListener('click', () => {
        gameView.classList.add('hidden');
        setupView.classList.remove('hidden');
        statusBar.classList.add('hidden');
    });

    askAiBtn.addEventListener('click', async () => {
        const depth = document.getElementById('search-depth').value;
        aiRecommendation.textContent = `Thinking (Depth ${depth})...`;
        document.getElementById('ai-all-moves').classList.add('hidden');
        
        const res = await apiGet(`/api/recommend?depth=${depth}`);
        recommendedMove = res.move;
        aiRecommendation.textContent = `Best: Card ${recommendedMove.symbol} at Position ${recommendedMove.position} (Score: ${res.score})`;
        
        // Populate all moves
        const list = document.getElementById('moves-list');
        list.innerHTML = res.all_evals.map(m => 
            `<li>Card <strong>${m.symbol}</strong> at <strong>${m.position}</strong>: Score ${m.score}</li>`
        ).join('');
        document.getElementById('ai-all-moves').classList.remove('hidden');

        // Highlight recommendation
        document.querySelectorAll('.board-cell').forEach(c => c.classList.remove('highlight'));
        const targetCell = document.querySelector(`.board-cell[data-pos="${recommendedMove.position}"]`);
        if (targetCell) targetCell.classList.add('highlight');

        document.querySelectorAll('.hand .card').forEach(c => c.classList.remove('selected', 'recommended'));
        const targetCard = document.querySelector(`.card[data-symbol="${recommendedMove.symbol}"]`);
        if (targetCard) {
            targetCard.classList.add('selected');
            targetCard.classList.add('recommended');
        }

        applyAiBtn.classList.remove('hidden');
    });

    applyAiBtn.addEventListener('click', async () => {
        if (recommendedMove) {
            const newState = await apiPost('/api/move', {
                symbol: recommendedMove.symbol,
                position: recommendedMove.position
            });
            updateUI(newState);
        }
    });

    document.getElementById('new-game-btn').addEventListener('click', () => {
        gameView.classList.add('hidden');
        setupView.classList.remove('hidden');
        statusBar.classList.add('hidden');
    });
});
