document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            const input = searchForm.querySelector('input[name="q"]');
            if (!input.value.trim()) {
                e.preventDefault();
                alert('Please enter a search term.');
            }
        });

        const searchInput = searchForm.querySelector('input[name="q"]');
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchForm.submit();
            }
        });
    }

    const entries = document.querySelectorAll('.entries li, .directory-list li');
    entries.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.boxShadow = '0 0 10px #66fcf1, 0 0 20px #45a29e';
        });
        item.addEventListener('mouseout', () => {
            item.style.boxShadow = '';
        });
    });
});

