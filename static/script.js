document.getElementById('settings-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let settings = {
        detect_person: document.getElementById('detect_person').checked,
        detect_animal: document.getElementById('detect_animal').checked,
        detect_property: document.getElementById('detect_property').checked,
        sound_enabled: document.getElementById('sound_enabled').checked
    };

    fetch('/update_settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
    }).then(response => response.json())
      .then(data => console.log("Settings Updated:", data));
});
