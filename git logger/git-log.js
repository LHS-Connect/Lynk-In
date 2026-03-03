document.addEventListener('DOMContentLoaded', () => {
    const logContainer = document.getElementById('git-log-list');

    // Fetch both the user configuration and the git log text file
    Promise.all([
        fetch('users.json').then(res => res.json()),
        fetch('git logger/git-log-box.txt').then(res => {
            if (!res.ok) throw new Error('Log file not found');
            return res.text();
        })
    ])
    .then(([userData, logData]) => {
        const lines = logData.trim().split('\n');
        logContainer.innerHTML = ''; 

        lines.forEach(line => {
            const parts = line.split('|||');
            
            if (parts.length >= 5) {
                const [author, profileUrl, message, files, commitUrl] = parts;
                const hash = commitUrl.split('/').pop();
                
                // Retrieve user color from JSON; default to a neutral grey if not found
                const userColor = userData[author]?.color || '#888';

                const scrollItem = document.createElement('div');
                scrollItem.className = 'scroll-item';
                
                // Apply the colored outline specifically to this scroll item
                scrollItem.style.border = `2px solid ${userColor}`;
                scrollItem.style.borderRadius = '8px';
                scrollItem.style.marginBottom = '10px';
                scrollItem.style.padding = '10px';
                scrollItem.style.background = 'rgba(255, 255, 255, 0.02)';

                const p = document.createElement('p');
                // Style: Author (User Color) | Message --- Files (Faded) | #Hash (Original Blue)
                p.innerHTML = `
                    <a href="${profileUrl}" target="_blank" style="color: ${userColor}; font-weight: bold; text-decoration: none;">${author}</a> | 
                    ${message} --- <span style="opacity: 0.7; font-size: 0.9em;">${files}</span> | 
                    <a href="${commitUrl}" target="_blank" style="color: #3498db; font-weight: bold; text-decoration: none;">#${hash}</a>
                `;
                
                scrollItem.appendChild(p);
                logContainer.appendChild(scrollItem);
            }
        });
    })
    .catch(err => {
        console.error('Log Error:', err);
        logContainer.innerHTML = `<div class="scroll-item"><p style="color: red;">Error: ${err.message}</p></div>`;
    });
});