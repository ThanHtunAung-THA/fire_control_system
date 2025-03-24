// Utility Functions
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function updateBadgeColor(badge, status) {
    const colors = {
        'active': 'success',
        'inactive': 'secondary',
        'warning': 'warning',
        'danger': 'danger',
        'info': 'info'
    };
    
    badge.className = `badge bg-${colors[status.toLowerCase()] || 'secondary'}`;
}

// Real-time Updates
function initializeWebSocket() {
    const ws = new WebSocket(`ws://${window.location.host}/ws/fire_control/`);
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onclose = function() {
        console.log('WebSocket connection closed. Reconnecting...');
        setTimeout(initializeWebSocket, 5000);
    };
}

function handleWebSocketMessage(data) {
    switch(data.type) {
        case 'alert_update':
            updateAlert(data.alert);
            break;
        case 'device_status':
            updateDeviceStatus(data.device);
            break;
        case 'team_status':
            updateTeamStatus(data.team);
            break;
        case 'new_message':
            handleNewMessage(data.message);
            break;
    }
}

// Alert Updates
function updateAlert(alert) {
    const alertRow = document.querySelector(`[data-alert-id="${alert.id}"]`);
    if (alertRow) {
        alertRow.querySelector('.alert-status').textContent = alert.status;
        alertRow.querySelector('.alert-time').textContent = formatDateTime(alert.timestamp);
        updateBadgeColor(alertRow.querySelector('.badge'), alert.status);
    }
}

// Device Status Updates
function updateDeviceStatus(device) {
    const deviceCard = document.querySelector(`[data-device-id="${device.id}"]`);
    if (deviceCard) {
        deviceCard.querySelector('.device-status').textContent = device.status;
        deviceCard.querySelector('.last-checked').textContent = `Last checked: ${formatDateTime(device.last_checked)}`;
        updateBadgeColor(deviceCard.querySelector('.badge'), device.status);
    }
}

// Team Status Updates
function updateTeamStatus(team) {
    const teamMember = document.querySelector(`[data-team-member-id="${team.id}"]`);
    if (teamMember) {
        teamMember.querySelector('.member-status').textContent = team.status;
        teamMember.querySelector('.member-location').textContent = team.location;
        updateBadgeColor(teamMember.querySelector('.badge'), team.status);
    }
}

// Message Handling
function handleNewMessage(message) {
    const messageContainer = document.querySelector('.message-container');
    if (messageContainer) {
        const messageElement = createMessageElement(message);
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message ${message.is_sender ? 'sent' : 'received'}`;
    div.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="sender">${message.sender}</span>
                <span class="time">${formatDateTime(message.timestamp)}</span>
            </div>
            <div class="message-text">${message.text}</div>
        </div>
    `;
    return div;
}

// Form Handling
function handleFormSubmit(form, successCallback) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (successCallback) successCallback(data);
                showNotification('Success!', 'success');
            } else {
                showNotification(data.error || 'An error occurred', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        });
    });
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket if we're on a page that needs real-time updates
    if (document.querySelector('[data-needs-websocket]')) {
        initializeWebSocket();
    }
    
    // Initialize all forms with data-form-handler attribute
    document.querySelectorAll('[data-form-handler]').forEach(form => {
        handleFormSubmit(form);
    });
}); 