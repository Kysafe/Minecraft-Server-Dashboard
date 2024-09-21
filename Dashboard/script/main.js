function startServer(serverName) {
    fetch(`http://EnterDomain:5000/start-server/${serverName}`)
    .then(response => {
        if (response.ok) {
            alert(`${serverName} został uruchomiony!`);
            updateServerStatus(serverName, 'online');
            location.reload();
        } else {
            response.json().then(data => {
                alert(`Błąd: ${data.error}`);
            });
        }
    })
    .catch(error => {
        console.error('Błąd podczas uruchamiania serwera:', error);
        alert('Nie udało się uruchomić serwera.');
    });
}

function stopServer() {
    fetch(`http://EnterDomain:5000/stop-server`)
    .then(response => {
        if (response.ok) {
            alert('Serwer został wyłączony!');
            updateServerStatus('serwermc', 'offline');
            updateServerStatus('serwermc2', 'offline');
        } else {
            response.json().then(data => {
                alert(`Błąd: ${data.error}`);
            });
        }
    })
    .catch(error => {
        console.error('Błąd podczas zatrzymywania serwera:', error);
        alert('Nie udało się wyłączyć serwera.');
    });
}

function updateServerStatus(serverName, status) {
    const statusElement = document.getElementById(`status-${serverName}`);
    if (status === 'online') {
        statusElement.classList.remove('text-warning');
        statusElement.classList.add('text-success');
        statusElement.innerHTML = '<i class="fas fa-check-circle"></i> Online';
    } else {
        statusElement.classList.remove('text-success');
        statusElement.classList.add('text-danger');
        statusElement.innerHTML = '<i class="fas fa-times-circle"></i> Offline';
    }
}

function checkServerStatus() {
    fetch('http://EnterDomain:5000/server-status')
    .then(response => response.json())
    .then(data => {
        updateServerStatus('serwermc', data.serwermc);
        updateServerStatus('serwermc2', data.serwermc2);
    })
    .catch(error => {
        console.error('Błąd podczas sprawdzania statusu serwera:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    checkServerStatus();
});
