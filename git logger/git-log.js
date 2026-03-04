document.addEventListener('DOMContentLoaded', () => {
    const logContainer = document.getElementById('git-log-list');

    Promise.all([
        fetch('git logger/users.json').then(res => res.json()),
        fetch('git logger/git-log-box.txt').then(res => res.text())
    ])
    .then(([userData, logData]) => {
        // Create a lookup map for colors based on display_name
        const colorLookup = {};
        Object.values(userData).forEach(u => {
            colorLookup[u.display_name] = u.color;
        });

        const lines = logData.trim().split('\n');
        logContainer.innerHTML = ''; 

        lines.forEach(line => {
            const parts = line.split('|||');
            if (parts.length < 5) return;

            const [displayName, profileUrl, message, files, commitUrl] = parts;
            const hash = commitUrl.split('/').pop();
            
            // Match color by display name
            const userColor = colorLookup[displayName] || '#888';

            const scrollItem = document.createElement('div');
            scrollItem.className = 'scroll-item';
            scrollItem.style.cssText = `
                border: 2px solid ${userColor};
                border-radius: 8px;
                margin-bottom: 10px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.02);
                width: 100%;
            `;

            scrollItem.innerHTML = `
                <p style="margin: 0; color: #fff; font-family: sans-serif;">
                    <a href="${profileUrl}" target="_blank" style="color: ${userColor}; font-weight: bold; text-decoration: none;">${displayName}</a> | 
                    ${message} <br>
                    <span style="opacity: 0.5; font-size: 0.8em;">Files: ${files}</span> | 
                    <a href="${commitUrl}" target="_blank" style="color: #0FBF3E; font-weight: bold; text-decoration: none; font-family: monospace;">#${hash}</a>
                </p>
            `;
            
            logContainer.appendChild(scrollItem);
        });
    })
    .catch(err => {
        console.error('Git Log Error:', err);
    });
});