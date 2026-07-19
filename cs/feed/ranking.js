document.addEventListener('DOMContentLoaded', () => {
    obtenerRanking();
});

async function obtenerRanking() {
    const contenedor = document.getElementById('podio-ganadores');
    const token = localStorage.getItem('access_token');

    try {
        const respuesta = await fetch('https://catsup.servemp3.com/api/ranking/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (respuesta.ok) {
            const topGatos = await respuesta.json();
            dibujarPodio(topGatos);
        } else {
            contenedor.innerHTML = "<p style='color: #a87b66;'>Hubo un problema al obtener el top felino.</p>";
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        contenedor.innerHTML = "<p style='color: red;'>No se pudo conectar con el servidor de ranking.</p>";
    }
}

function dibujarPodio(listaDeGatos) {
    const contenedor = document.getElementById('podio-ganadores');
    contenedor.innerHTML = "";

    if (listaDeGatos.length === 0) {
        contenedor.innerHTML = "<p>¡Aún no hay suficientes votos para armar el podio! ᓚᘏᗢ</p>";
        return;
    }

    const medallas = ["🥇", "🥈", "🥉"];

    listaDeGatos.forEach((gato, indice) => {
        const itemHTML = `
            <div class="podio-item puesto-${indice + 1}">
                <div class="medalla">${medallas[indice] || "⋆"}</div>
                <div class="podio-info">
                    <h4>Usuario ${gato.ID_usuario || "Gatuno"}</h4>
                    <p>${gato.titulo ? gato.titulo.substring(0, 50) + "..." : "Sin descripción"}</p>
                </div>
                <div class="podio-likes">♡ ${gato.likes || gato.total_puntos || 0}</div>
            </div>
        `;
        contenedor.innerHTML += itemHTML;
    });
}