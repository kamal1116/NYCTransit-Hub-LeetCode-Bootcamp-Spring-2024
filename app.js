function selectLine(lineCode) {
    fetch(`/api/updates/${lineCode}`)
        .then(response => response.json())
        .then(data => displayUpdates(data))
        .catch(error => console.error('Error fetching data:', error));
}

function displayUpdates(data) {
    const table = `<table>
        <tr>
            <th>Train</th>
            <th>Subway Station</th>
            <th>Arrival Time</th>
        </tr>
        ${data.map(update => `
        <tr>
            <td>${update.train}</td>
            <td>${update.stop_name}</td>
            <td>${update.arrival ? new Date(update.arrival * 1000).toLocaleTimeString() : 'N/A'}</td>
        </tr>
        `).join('')}
    </table>`;
    document.getElementById('updates').innerHTML = table;
}
