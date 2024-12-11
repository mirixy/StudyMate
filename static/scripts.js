document.addEventListener('DOMContentLoaded', () => {
    // Elemente für das Hinzufügen-Modal
    const modal = document.getElementById('todo-modal');
    const addTodoButton = document.getElementById('add-todo-button');
    const closeButton = document.querySelector('.close-button');

    // Initial hide modals
    modal.style.display = 'none';
    
    // Modal öffnen für Hinzufügen
    addTodoButton.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    // Modal schließen für Hinzufügen
    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Modal schließen, wenn außerhalb des Modals geklickt wird
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Elemente für das Bearbeiten-Modal
    const editModal = document.getElementById('edit-modal');
    const editCloseButton = document.querySelector('.edit-close-button');
    const editForm = document.getElementById('edit-form');
    const editTitle = document.getElementById('edit-title');
    const editDescription = document.getElementById('edit-description');

    // Initial hide edit modal
    editModal.style.display = 'none';

    // Modal öffnen für Bearbeiten
    document.querySelectorAll('.actions a[href^="/edit/"]').forEach((editLink) => {
        editLink.addEventListener('click', (event) => {
            event.preventDefault(); // Standard-Linkverhalten verhindern

            // ToDo-ID aus dem Link extrahieren
            const todoId = editLink.getAttribute('href').split('/edit/')[1];

            // Abrufen von ToDo-Daten über API
            fetch(`/api/todos/${todoId}`)
                .then((response) => response.json())
                .then((data) => {
                    // Formular mit ToDo-Daten füllen
                    editForm.action = `/edit/${todoId}`;
                    editTitle.value = data.title;
                    editDescription.value = data.description || '';

                    // Modal anzeigen
                    editModal.style.display = 'block';
                })
                .catch((error) => {
                    console.error('Fehler beim Abrufen der ToDo-Daten:', error);
                });
        });
    });

    // Modal schließen für Bearbeiten
    editCloseButton.addEventListener('click', () => {
        editModal.style.display = 'none';
    });

    // Modal schließen, wenn außerhalb des Modals geklickt wird
    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });

    // Add form submission handler
    const addForm = document.getElementById('add-form');
    addForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const formData = new FormData(addForm);
        fetch('/add', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload page to show new todo
            } else {
                console.error('Error adding todo');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
        modal.style.display = 'none';
    });

    // Edit form submission handler
    editForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const formData = new FormData(editForm);
        fetch(editForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload page to show updated todo
            } else {
                console.error('Error updating todo');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
        editModal.style.display = 'none';
    });
});