
async function getHTML() {
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const response = await chrome.tabs.sendMessage(activeTab.id, { type: "getHTML" });
    return response.html;
}


async function search(event) {
    const searchQuery = document.getElementById('searchQuery').value;

    const html = await getHTML();

    const data = {
        'query': searchQuery,
        'html': html
    };

    try {
        const response = await fetch('http://127.0.0.1:9999/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const results = await response.json();
        // Update popup content with results
        updatePopupContent(results);
    } catch (error) {
        console.error('Error sending data:', error);
    }
};

document.getElementById('searchQuery').addEventListener('keydown', async (event) => {
    if (event.key == "Enter") {

        const searchQuery = document.getElementById('searchQuery').value;
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });

        const data = {
            'query': searchQuery,
            'url': activeTab.url
        };

        try {
            const response = await fetch('http://127.0.0.1:9999/search/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }

            const results = await response.json();
            // Update popup content with results
            updatePopupContent(results);
        } catch (error) {
            console.error('Error sending data:', error);
        }
    }
});

document.getElementById('searchButton').addEventListener('click', async () => {
    const searchQuery = document.getElementById('searchQuery').value;
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const data = {
        'query': searchQuery,
        'url': activeTab.url
    };

    try {
        const response = await fetch('http://127.0.0.1:9999/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const results = await response.json();
        // Update popup content with results
        updatePopupContent(results);
    } catch (error) {
        console.error('Error sending data:', error);
    }
});

function updatePopupContent(results) {
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = ''; // Clear previous results

    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.classList.add('result-item'); // Add class for styling

        const text = document.createElement('p');
        text.textContent = result.text;
        resultElement.appendChild(text);

        resultsContainer.appendChild(resultElement);
    });
}