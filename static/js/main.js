// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Profile image preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-preview').src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Like functionality
function likeProfile(profileId) {
    fetch('/like/' + profileId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likeBtn = document.querySelector(`#like-btn-${profileId}`);
            likeBtn.classList.toggle('liked');
            likeBtn.querySelector('i').classList.toggle('fas');
            likeBtn.querySelector('i').classList.toggle('far');
            
            if (data.match) {
                showMatchModal(data.matchedUser);
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// Show match modal
function showMatchModal(matchedUser) {
    const modal = new bootstrap.Modal(document.getElementById('matchModal'));
    document.getElementById('matched-user-name').textContent = matchedUser.name;
    document.getElementById('matched-user-image').src = matchedUser.image;
    modal.show();
}

// Real-time messaging
let messageSocket = null;

function connectMessageSocket() {
    if (messageSocket === null || messageSocket.readyState !== WebSocket.OPEN) {
        messageSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/messages/'
        );

        messageSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            appendMessage(data);
        };

        messageSocket.onclose = function(e) {
            console.log('Message socket closed unexpectedly');
            setTimeout(connectMessageSocket, 3000);
        };
    }
}

function appendMessage(data) {
    const chatContainer = document.querySelector('.chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', data.sent_by_user ? 'message-sent' : 'message-received');
    messageDiv.innerHTML = `
        <div class="message-content">
            ${data.message}
        </div>
        <div class="message-time">
            ${new Date(data.timestamp).toLocaleTimeString()}
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Send message
function sendMessage(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (message) {
        const recipientId = document.getElementById('recipient-id').value;
        
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                recipient_id: recipientId,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageInput.value = '';
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Infinite scroll for matches
let page = 1;
let loading = false;
const matchesContainer = document.querySelector('.matches-container');

if (matchesContainer) {
    window.addEventListener('scroll', () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            loadMoreMatches();
        }
    });
}

function loadMoreMatches() {
    if (loading) return;
    loading = true;
    
    fetch(`/matches?page=${page + 1}`)
        .then(response => response.json())
        .then(data => {
            if (data.matches.length > 0) {
                page++;
                data.matches.forEach(match => {
                    const matchCard = createMatchCard(match);
                    matchesContainer.appendChild(matchCard);
                });
            }
            loading = false;
        })
        .catch(error => {
            console.error('Error:', error);
            loading = false;
        });
}

function createMatchCard(match) {
    const div = document.createElement('div');
    div.className = 'col-md-4 mb-4 animate-fade-in';
    div.innerHTML = `
        <div class="card profile-card">
            <div class="match-percentage">${match.compatibility}% Match</div>
            <img src="${match.photo}" class="card-img-top" alt="${match.name}">
            <div class="card-body">
                <h5 class="card-title">${match.name}, ${match.age}</h5>
                <p class="card-text text-muted">${match.location}</p>
                <p class="card-text">${match.bio}</p>
                <button onclick="likeProfile(${match.id})" class="btn btn-primary w-100" id="like-btn-${match.id}">
                    <i class="far fa-heart"></i> Like
                </button>
            </div>
        </div>
    `;
    return div;
}

// Form validation
function validateForm() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', function() {
    validateForm();
    
    // Initialize message socket if on messages page
    if (document.querySelector('.chat-container')) {
        connectMessageSocket();
    }
    
    // Initialize message form
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', sendMessage);
    }
});
