window.onload = function() {
    document.getElementById('nosmoke').onclick = function() {
        document.getElementById('justification').disabled = document.getElementById('nosmoke').checked;
    };
};
